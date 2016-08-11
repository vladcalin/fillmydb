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

import time


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
    def __init__(self, model):
        self.model = model
        self._internal_wrapper = self.detect_model_type(self.model)
        self._fields = self._internal_wrapper.get_fields()
        setattr(self, self.model.__name__, _ModelDelegator(self._fields, self.model.__name__))

    def detect_model_type(self, model):
        if peewee and issubclass(model, peewee.Model):
            return PeeweeModelWrapper(self.model)

        raise InvalidModelError("The model {} is not peewee, django, or sqlalchemy".format(model))


    def generate_field_values(self):
        fields_vals = {}
        for field in self._fields:
            field_spec = getattr(getattr(self, self.model.__name__), field)
            if not field_spec:
                fields_vals[field] = None
            else:
                fields_vals[field] = field_spec.call()
        return fields_vals

    def generate(self, count):
        _start = time.time()
        for _ in range(count):
            self._internal_wrapper.create_instance(**self.generate_field_values())
        print("Generation complete in {} seconds".format(time.time() - _start))



if __name__ == '__main__':
    from tests.models import TestModel
    import faker

    factory = faker.Factory.create()
    if not TestModel.table_exists():
        TestModel.create_table()

    wrapper = ModelWrapper(TestModel)

    wrapper.TestModel.client_name = FieldSpec(factory.name)
    wrapper.TestModel.password_hash = FieldSpec(factory.binary, length=75)
    wrapper.TestModel.email = FieldSpec(factory.email)
    wrapper.TestModel.description = FieldSpec(factory.text)
    wrapper.TestModel.visits = FieldSpec(factory.pyint)

    wrapper.generate(1000)
