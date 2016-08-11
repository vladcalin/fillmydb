# fillmydb
Fill your database with mocked instances.


## Usage with [`fake-factory`](https://github.com/joke2k/faker)

```python

    import faker

    factory = faker.Factory.create()

    wrapper = ModelWrapper(TestModel)

    wrapper[TestModel].client_name = FieldSpec(factory.name)
    wrapper[TestModel].description = FieldSpec(factory.text)
    wrapper[TestModel].password_hash = FieldSpec(factory.binary, length=25)
    wrapper[TestModel].email = FieldSpec(factory.email)
    wrapper[TestModel].visits = FieldSpec(factory.pyint)

    item = wrapper.generate(100)

```

## General workflow

```python
initial_to_order_queue()
while models_to_process():
	model = process_next_model()
		if model.has_unresolved_dependency():
			push_back_to_queue(model)
		for _ in range(number_of_instances):
			for field in model.fields():
				# resolve_field(field)
			    if field == ForeignKey:
					field = get_random_ref_model_instance()
				else:
				    field = resolve_normal()
	mark_as_processed(model)
```
