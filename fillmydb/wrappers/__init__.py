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
                print("Attribute with no specification in {}: {}".format(name, field_name))
                generated_values[field_name] = None
        return handler.create_instance_and_persist(**generated_values)

    def generate(self, *counts):
        for index, count in enumerate(counts):
            for _ in range(count):
                self.generate_one_instance(self._models[index][1])


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
    from tests.models import TestModel

    import faker

    factory = faker.Factory.create()

    wrapper = ModelWrapper(TestModel)

    wrapper[TestModel].client_name = FieldSpec(factory.name)
    wrapper[TestModel].description = FieldSpec(factory.text)
    wrapper[TestModel].password_hash = FieldSpec(factory.binary, length=25)
    wrapper[TestModel].email = FieldSpec(factory.email)
    wrapper[TestModel].visits = FieldSpec(factory.pyint)

    item = wrapper.generate(100)
