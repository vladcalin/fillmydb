import faker


class FakeFactoryProvider:
    _field_ids = {
        0: "name",
        1: "name_female",
        2: "name_male",
        3: "last_name"
    }

    def __init__(self, localisation="en_GB"):
        self.instance = faker.Factory.create(localisation)

    def resolve_field(self, field_spec):
        if not field_spec:
            return None
        return getattr(self.instance, self._field_ids[field_spec.field])(*field_spec.args, **field_spec.kwargs)
