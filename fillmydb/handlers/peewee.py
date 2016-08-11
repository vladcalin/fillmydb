import peewee


class PeeweeHandler:
    def __init__(self, model):
        self.model = model

        self.model.create_table(fail_silently=True)

    def get_field_names(self):
        fields = []
        for field_name in dir(self.model):
            if isinstance(getattr(self.model, field_name), peewee.Field):
                fields.append(field_name)
        return fields

    def create_instance(self, **attrs):
        return self.model(**attrs)

    def create_instance_and_persist(self, **attrs):
        return self.model.create(**attrs)
