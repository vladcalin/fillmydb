try:
    import peewee

    from fillmydb.handlers.peewee import PeeweeHandler
except ImportError:
    peewee = None
    PeeweeHandler = None


class ModelWrapper:
    class _FieldsStates:

        def __init__(self, model):
            self._fields = []
            self._model_name = model.__name__

        def init_fields(self, *fields):
            """
            Initializes the fields of the instance.
            :param fields: a list of strings representing the field names
            :return: None
            """
            self._fields = fields
            for field in fields:
                setattr(self, field, None)

        def __repr__(self):
            return "<_FieldsStates({})\n\t{}>".format(
                self._model_name, "\n\t".join(["{}={}".format(field, getattr(self, field)) for field in
                                               self._fields]))

    def __init__(self, *models):
        self._models = [(model.__name__, model, self.get_model_handler(model), self._FieldsStates(model)) for model in
                        models]
        for model_name, model, model_handler, fields_specs in self._models:
            fields_specs.init_fields(*model_handler.get_field_names())
        self._priorities = None
        self.compute_priorities()

        self._has_been_processed = [False for _ in range(len(self._models))]

    def __getitem__(self, item):
        if isinstance(item, str):
            name = item
        else:
            name = item.__name__

        items = [x for x in self._models if x[0] == name]
        if not items:
            raise KeyError("Model {} not found".format(name))

        return items[0][3]

    def get_model_handler(self, model):
        if peewee and issubclass(model, peewee.Model):
            return PeeweeHandler(model)

    def generate_one_instance(self, model):
        items = [x for x in self._models if x[0] == model.__name__]
        if not items:
            raise ValueError("Model {} not registered in this wrapper".format(model.__name__))

        name, model, handler, fields_states = items[0]

        generated_values = {}
        for field_name in handler.get_field_names():
            spec = getattr(fields_states, field_name, None)
            if spec:
                generated_values[field_name] = spec.resolve()
            else:
                if not field_name == "id":
                    print("Attribute with no specification in {}: {}".format(name, field_name))
                generated_values[field_name] = None
        return handler.create_instance_and_persist(**generated_values)

    def compute_priorities(self):
        self._priorities = []
        for name, model, handler, fields_states in self._models:
            self._priorities.append((len(handler.get_model_dependencies()), model))
        self._priorities.sort(key=lambda x: x[0], reverse=True)

    def generate(self, *counts):
        if len(counts) != len(self._models):
            raise ValueError("Invalid number of items to generate, number of 'counts' must match the number of models")
        while not all(self._has_been_processed):
            to_process = self._priorities.pop()

            name, model, handler, specs = self._get_model_item(to_process[1].__name__)
            if self.model_has_unsolved_deps(model):
                self._priorities.insert(0, to_process)

    def model_has_unsolved_deps(self, model):
        name, model, handler, specs = self._get_model_item(model.__name__)
        deps = handler.get_model_dependencies()
        for dep in deps:
            if not self._has_been_processed[self._get_model_index(dep.__name__)]:
                print("Found unresolved dependency for {} : {}".format(name, dep.__name__))
                return True
        return False

    def _get_model_item(self, model_name):
        return [x for x in self._models if x[0] == model_name][0]

    def _get_model_index(self, model_name):
        for i, vals in enumerate(self._models):
            if vals[0] == model_name:
                return i
        raise KeyError("{} not found".format(model_name))

class FieldSpec:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def resolve(self):
        return self.func(*self.args, **self.kwargs)

    def __repr__(self):
        return "<FieldSpec func={} args={} kwargs={}>".format(
            self.func.__name__, self.args, self.kwargs
        )


if __name__ == '__main__':
    from tests.models import User, Post, Like

    import faker

    factory = faker.Factory.create()

    wrapper = ModelWrapper(User, Like, Post)

    wrapper[User].name = FieldSpec(factory.name)
    wrapper[User].username = FieldSpec(factory.user_name)
    wrapper[User].description = FieldSpec(factory.text)
    wrapper[User].password_hash = FieldSpec(factory.binary, length=25)
    wrapper[User].email = FieldSpec(factory.email)
    wrapper[User].visits = FieldSpec(factory.pyint)

    wrapper.generate(5, 5, 5)
