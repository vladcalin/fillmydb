import os
from unittest import TestCase

from peewee import Model, CharField, SqliteDatabase

from fillmydb import FieldSpec, ModelWrapper

TEST_DB = os.path.join(os.path.abspath("."), "test.db")

database = SqliteDatabase(TEST_DB)


# region Test models
class TestModel1(Model):
    field1 = CharField()
    field2 = CharField(null=True)
    field3 = CharField(default="test")

    class Meta:
        database = database


class TestModel2(Model):
    field1 = CharField()
    field2 = CharField(null=True)
    field3 = CharField(default="test")

    class Meta:
        database = database


class TestModel3(Model):
    field1 = CharField()
    field2 = CharField(null=True)
    field3 = CharField(default="test")

    class Meta:
        database = database


# endregion


def generate_mockup_field_spec(to_return=None):
    class MockupFieldSpec:
        def __init__(self, *args, **kwargs):
            pass

        def resolve(self):
            return to_return

    return MockupFieldSpec()


class PeeweeBasicFunctionalityTestCases(TestCase):
    @classmethod
    def setUpClass(cls):
        TestModel1.create_table(fail_silently=True)

    @classmethod
    def tearDownClass(cls):
        database.close()
        os.remove(TEST_DB)

    # actual tests

    def test_wrap_model(self):
        wrapper = ModelWrapper(TestModel1)

        self.assertIsInstance(wrapper[TestModel1], ModelWrapper._ModelSpecs)
        self.assertDictEqual(wrapper[TestModel1].get_field_specs(), {"field1": None, "field2": None,
                                                                     "field3": None, "id": None})

    def test_wrap_more_models(self):
        wrapper = ModelWrapper(TestModel1, TestModel2, TestModel3)

        self.assertIsInstance(wrapper[TestModel1], ModelWrapper._ModelSpecs)
        self.assertDictEqual(wrapper[TestModel1].get_field_specs(), {"field1": None, "field2": None,
                                                                     "field3": None, "id": None})

        self.assertIsInstance(wrapper[TestModel2], ModelWrapper._ModelSpecs)
        self.assertDictEqual(wrapper[TestModel2].get_field_specs(), {"field1": None, "field2": None,
                                                                     "field3": None, "id": None})
        self.assertIsInstance(wrapper[TestModel3], ModelWrapper._ModelSpecs)
        self.assertDictEqual(wrapper[TestModel3].get_field_specs(), {"field1": None, "field2": None,
                                                                     "field3": None, "id": None})

    def test_set_fields(self):
        wrapper = ModelWrapper(TestModel1)
        wrapper[TestModel1].field1 = "test"
        wrapper[TestModel1].field2 = "test2"
        self.assertDictEqual(wrapper[TestModel1].get_field_specs(), {"field1": "test", "field2": "test2",
                                                                     "field3": None, "id": None})

    def test_generate_for_single_model(self):
        wrapper = ModelWrapper(TestModel1)
        wrapper[TestModel1].field1 = generate_mockup_field_spec("test1")
        wrapper[TestModel1].field2 = generate_mockup_field_spec("test2")
        wrapper[TestModel1].field3 = generate_mockup_field_spec("test3")
        wrapper[TestModel1].field4 = generate_mockup_field_spec("test4")

        with self.assertRaises(ValueError):
            wrapper.generate()

        with self.assertRaises(ValueError):
            wrapper.generate(5, 10)

        wrapper.generate(10)
        self.assertEqual(TestModel1.select().count(), 10)

    def test_no_such_model(self):
        wrapper = ModelWrapper(TestModel1)
        with self.assertRaises(KeyError):
            x = wrapper[TestModel2]
