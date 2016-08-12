import peewee


class PeeweeHandler:
    def __init__(self, model):
        self.model = model

        self.model.create_table(fail_silently=True)
        self.fields, self.fields_names = self.get_fields()
        self.ref_models = self.get_referenced_models()

    def get_fields(self):
        fields = []
        fields_names = []
        for field_name in dir(self.model):
            field = getattr(self.model, field_name)
            if isinstance(field, peewee.Field):
                fields.append(field)
                fields_names.append(field_name)
        return fields, fields_names

    def create_instance(self, **attrs):
        return self.model(**attrs)

    def create_instance_and_persist(self, **attrs):
        return self.model.create(**attrs)

    def get_referenced_models(self):
        dependencies = []
        for field in self.fields:
            if isinstance(field, peewee.ForeignKeyField):
                dependencies.append(field.rel_model)
        return dependencies

    def is_value_field(self, field_name):
        return not self.is_foreign_key_field(field_name)

    def is_foreign_key_field(self, field_name):
        field = getattr(self.model, field_name)
        if isinstance(field, peewee.ForeignKeyField):
            return True

    def get_referenced_model_by_field_name(self, field_name):
        return getattr(self.model, field_name).rel_model

    def pick_random_instance(self):
        query = self.model.select().order_by(peewee.fn.Random()).limit(1).execute()
        for item in query:
            return item

    def __repr__(self):
        return "<PeeweeHandler for {}>".format(self.model.__name__)
