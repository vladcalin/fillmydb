import peewee


class PeeweeModelWrapper:

    def __init__(self, model):
        self.model = model

    def get_fields(self):
        fields = []
        for field in dir(self.model):
            attr = getattr(self.model, field)
            if isinstance(attr, peewee.Field):
                fields.append(field)
        return fields