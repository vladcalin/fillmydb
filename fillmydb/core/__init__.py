try:
    import peewee

    from fillmydb.handlers.peewee_handler import PeeweeHandler
except ImportError:
    peewee = None
    PeeweeHandler = None

try:
    import django
    from django.db.models import Model as DjangoModel
    from fillmydb.handlers.django_handler import DjangoHandler
except ImportError:
    django = None
    DjangoHandler = None

import os
import sys
import importlib.machinery
import importlib.util

IS_PY35 = sys.version_info >= (3, 5)


def initialize_django(settings_py_path):
    """
    Initializes the environment required by Django. Must be called **before** importing your models::

        import fillmydb
        fillmydb.initialize_django("path/to/settings.py")

        from mydjangoproject.myapp.models import MyModel, MyOtherModel

        ...

    :param settings_py_path: Path to the ``settings.py`` file from your Django project.
    """
    if not django:
        raise RuntimeError("Module 'django' could not be imported")

    if IS_PY35:
        spec = importlib.util.spec_from_file_location("django_settings", settings_py_path)
        django_settings = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(django_settings)
    else:
        django_settings = importlib.machinery.SourceFileLoader("django_settings", settings_py_path).load_module()

    os.environ["DJANGO_SETTINGS_MODULE"] = "django_settings"
    django.setup()


class ModelWrapper:
    class _ProcessingQueue:
        """
        The processing queue class that manages the processing order of the models.
        """

        def __init__(self, *handlers):
            self.handlers = list(handlers)

        def initial_order(self):
            """
            Orders the queue so that the first processed are the models with fewest dependencies. Expected to be
            processed first the models with no dependencies.
            :return:
            """
            self.handlers.sort(key=lambda model: len(model.ref_models), reverse=True)

        def get_next_item(self):
            item = self.handlers.pop()
            return item

        def put_item_back(self, item):
            """
            Inserts the item to the end of the queue.
            :param item: an ModelHandler instance
            """
            self.handlers.insert(0, item)

        def __len__(self):
            return len(self.handlers)

    class _ModelSpecs(object):
        """
        A class that encapsulates the specifications of the fields of the model.
        """

        def __init__(self, handler):
            self._model = handler.model
            self._fields = handler.fields_names

            for field in self._fields:
                setattr(self, field, None)

        def get_field_specs(self):
            return {field: getattr(self, field) for field in self._fields}

        def __repr__(self):
            return "<ModelSpecs({}) {}>".format(self._model.__name__, ", ".join(
                ["{}={}".format(field, getattr(self, field)) for field in self._fields]))

    def __init__(self, *models):
        """
        Creates a wrapper around the *models* models that must be of the same type.

        :param models: The models to be wrapped and used afterwards for generating instances.
        :raises ValueError: when the models are not of the same type (belong to different ORMs)
        """

        # used for determining how many instances of each model should generate
        self._initial_order = models

        # the wrapped model instances in specific handlers
        self._handlers = {
            model: self._get_model_handler(model) for model in models
            }

        # the model specifications
        self._specs = {
            model: self._ModelSpecs(self._handlers[model]) for model in models
            }

        # flags that shows if a specific model was processed or not
        self._processed = {
            model: False for model in models
            }

        self._validate_models()

    def _validate_models(self):
        handler_types = set()
        for model in self._handlers:
            handler_types.add(self._handlers[model].DB_TYPE)
        if len(handler_types) != 1:
            raise ValueError(
                "Inconsistent model configuration. Expected just one type of models, but got {}: {}".format(
                    len(handler_types), handler_types))

    def __getitem__(self, item):
        """
        Returns the model specification
        :param item:
        :return:
        """
        if item in self._specs:
            return self._specs[item]
        raise KeyError("No model {} found".format(item))

    def _get_model_handler(self, model):
        if peewee and issubclass(model, peewee.Model):
            return PeeweeHandler(model)

        if django and issubclass(model, DjangoModel):
            return DjangoHandler(model)

    def _model_has_unresolved_reference(self, model):
        """
        Determines if the model has unresolved referenced models. This is needed because in order to generate
        instances of a model, first we must generate instances of the models that are referenced through foreign keys.
        """
        for ref_model in self._handlers[model].ref_models:
            if not self._processed[ref_model]:
                return True
        return False

    def generate(self, *counts):
        """
        Generates and persists items. *counts* is a list of integers that indicate how many instances of each model
        should generate. The order is preserved from the models specified in constructor.

        For example, if ``wrapper`` was declared as ``ModelWrapper(Model1, Model2, Model3)`` the following code

        .. code-block:: python

            wrapper.generate(10, 20, 15)

        will generate 10 instances of ``Model1``, 20 instances of ``Model2`` and 15 instances of ``Model3``.

        :param counts: the quantity of each item to be generated.
        :return: None
        """
        if len(counts) != len(self._initial_order):
            raise ValueError("The number of count items does not match the model count")

        queue = self._ProcessingQueue(*self._handlers.values())
        queue.initial_order()
        while len(queue) != 0:
            item = queue.get_next_item()
            if self._model_has_unresolved_reference(item.model):
                queue.put_item_back(item)
                continue

            count = counts[self._initial_order.index(item.model)]
            print("Generating {} instances of {}".format(count, item.model.__name__))
            self._generate_instances(item, count)
            self._processed[item.model] = True

    def _generate_instances(self, handler, count):
        """
        Generates *count* instances of the model wrapped in *handler*. Only for internal use.
        :param handler:
        :param count:
        :return:
        """
        for _ in range(count):
            generated = {}
            for field_name in handler.fields_names:
                if handler.is_value_field(field_name):
                    # resolving normal field
                    field_spec = getattr(self._specs[handler.model], field_name)
                    if not field_spec:
                        generated[field_name] = None
                    else:
                        generated[field_name] = field_spec.resolve()
                else:
                    # resolving foreign key field
                    generated[field_name] = self._handlers[
                        handler.get_referenced_model_by_field_name(field_name)].pick_random_instance()
            handler.create_instance_and_persist(**generated)


class FieldSpec:
    """
    The generation logic for mock values for fields.
    """

    def __init__(self, func, *args, **kwargs):
        """
        The mocked values of the fields will be generated as ``func(*args, **kwargs)``.

        :param func: a callable object.
        :param args: the ordinal parameters ``func`` will be called with.
        :param kwargs: the named parameters ``func`` will be called with.
        """
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def resolve(self):
        """
        Method that returns the generated value.

        :return: an object that will be directly assigned to the field when instantiating a model.
        """
        return self.func(*self.args, **self.kwargs)

    def __repr__(self):
        return "<FieldSpec func={} args={} kwargs={}>".format(
            self.func.__name__, self.args, self.kwargs
        )


if __name__ == '__main__':
    from tests.data.peewee_models import User, Post, Like

    import faker

    factory = faker.Factory.create()

    wrapper = ModelWrapper(User, Like, Post)

    wrapper[User].name = FieldSpec(factory.name)
    wrapper[User].username = FieldSpec(factory.user_name)
    wrapper[User].description = FieldSpec(factory.text)
    wrapper[User].password_hash = FieldSpec(factory.binary, length=25)
    wrapper[User].email = FieldSpec(factory.email)
    wrapper[User].visits = FieldSpec(factory.pyint)

    wrapper[Post].title = FieldSpec(factory.sentence)
    wrapper[Post].text = FieldSpec(factory.text)

    wrapper.generate(10, 10, 10)
