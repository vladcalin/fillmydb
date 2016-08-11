# fillmydb
Fill your database with mocked instances.


## Usage with [`fake-factory`](https://github.com/joke2k/faker)

```python

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

```
