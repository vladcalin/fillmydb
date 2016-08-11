import peewee


class PeeweeHandler:
    def __init__(self, model):
        self.model = model

        self.model.create_table(fail_silently=True)
        self._fields = []

    def get_field_names(self):
        if self._fields:
            return self._fields
        for field_name in dir(self.model):
            if isinstance(getattr(self.model, field_name), peewee.Field):
                self._fields.append(field_name)
        return self._fields

    def create_instance(self, **attrs):
        return self.model(**attrs)

    def create_instance_and_persist(self, **attrs):
        return self.model.create(**attrs)

    def get_model_dependencies(self):
        dependencies = []
        for field_name in self.get_field_names():
            field = getattr(self.model, field_name)
            if isinstance(field, peewee.ForeignKeyField):
                dependencies.append((field_name, field.rel_model))
        return dependencies