try:
    import peewee

    from fillmydb.orm_wrappers.peewee import PeeweeModelWrapper
except ImportError:
    print("Unable to import peewee. Not checking for peewee models")
    peewee = None
    PeeweeModelWrapper = None

try:
    import django
except ImportError:
    print("Unable to import django. Not checking for django models")
    django = None

try:
    import sqlalchemy
except ImportError:
    print("Unable to import sqlalchemy. Not checking for sqlalchemy models")
    sqlalchemy = None

from fillmydb.consts import ModelType, Fields, FieldSpec, Provider
from fillmydb.errors import InvalidModelError
from fillmydb.providers import FakeFactoryProvider


class _ModelDelegator(object):
    def __init__(self, fields, class_name):
        self._fields = fields
        self._class_name = class_name
        for field in self._fields:
            setattr(self, field, None)

    def get_fields(self):
        return {field: getattr(self, field) for field in self._fields}

    def __repr__(self):
        return "<_ModelDelegator for {}, fields=({})>".format(self._class_name,
                                                              ", ".join(
                                                                  ["{}={}".format(field, getattr(self, field)) for field
                                                                   in self._fields]))


class ModelWrapper:
    def __init__(self, model, provider=Provider.FAKE_FACTORY, localization="en_GB"):
        self.model = model
        self._internal_wrapper = self.detect_model_type(self.model)
        self._fields = self._internal_wrapper.get_fields()
        setattr(self, self.model.__name__, _ModelDelegator(self._fields, self.model.__name__))

        if provider == Provider.FAKE_FACTORY:
            self.provider = FakeFactoryProvider(localization)

    def detect_model_type(self, model):
        if peewee and issubclass(model, peewee.Model):
            return PeeweeModelWrapper(self.model)

        raise InvalidModelError("The model {} is not peewee, django, or sqlalchemy".format(model))

    def resolve_field(self, field_spec):
        return self.provider.resolve_field(field_spec)

    def generate_one_instance(self):
        fields_vals = {}
        for field in self._fields:
            fields_vals[field] = self.resolve_field(getattr(getattr(self, self.model.__name__), field))
        return self.model(**fields_vals)


if __name__ == '__main__':
    from tests.models import TestModel

    wrapper = ModelWrapper(TestModel)

    print(wrapper.TestModel)

    wrapper.TestModel.username = FieldSpec(Fields.name)

    print(wrapper.generate_one_instance())
