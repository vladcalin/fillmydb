try:
    import peewee

    from fillmydb.handlers.peewee import PeeweeHandler
except ImportError:
    peewee = None
    PeeweeHandler = None


class ModelWrapper:
    class _ProcessingQueue:

        def __init__(self, *handlers):
            self.handlers = list(handlers)

        def initial_order(self):
            self.handlers.sort(key=lambda model: len(model.ref_models), reverse=True)

        def get_next_item(self):
            item = self.handlers.pop()
            return item

        def put_item_back(self, item):
            self.handlers.insert(0, item)

        def __len__(self):
            return len(self.handlers)

    class _ModelSpecs(object):

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
        self._initial_order = models
        self._handlers = {
            model: self._get_model_handler(model) for model in models
            }
        self._specs = {
            model: self._ModelSpecs(self._handlers[model]) for model in models
            }
        self._processed = {
            model: False for model in models
            }

    def __getitem__(self, item):
        if item in self._specs:
            return self._specs[item]
        raise KeyError("No model {} found".format(item))

    def _get_model_handler(self, model):
        if peewee and issubclass(model, peewee.Model):
            return PeeweeHandler(model)

    def model_has_unresolved_reference(self, model):
        for ref_model in self._handlers[model].ref_models:
            if not self._processed[ref_model]:
                return True
        return False

    def generate(self, *counts):
        queue = self._ProcessingQueue(*self._handlers.values())
        queue.initial_order()
        while len(queue) != 0:
            item = queue.get_next_item()
            if self.model_has_unresolved_reference(item.model):
                queue.put_item_back(item)
                continue

            count = counts[self._initial_order.index(item.model)]
            print("Generating {} instances of {}".format(count, item.model.__name__))
            self.generate_instances(item, count)
            self._processed[item.model] = True

    def generate_instances(self, handler, count):
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

    wrapper[Post].title = FieldSpec(lambda _: "test", 1)
    wrapper[Post].text = FieldSpec(factory.text)

    wrapper.generate(10, 10, 10)
