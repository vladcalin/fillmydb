# fillmydb

[![Build Status](https://travis-ci.org/vladcalin/fillmydb.svg?branch=master)](https://travis-ci.org/vladcalin/fillmydb)
[![Coverage Status](https://coveralls.io/repos/github/vladcalin/fillmydb/badge.svg?branch=master)](https://coveralls.io/github/vladcalin/fillmydb?branch=master)
[![Documentation Status](https://readthedocs.org/projects/fillmydb/badge/?version=latest)](http://fillmydb.readthedocs.io/en/latest/?badge=latest)
[![PyPI version](https://badge.fury.io/py/fillmydb.svg)](https://badge.fury.io/py/fillmydb)


Fill your database with mocked instances.

Wrap you ORM model into a `ModelWrapper`, specify how your fields should look
like and then generate how many instances you want of each model.


## Installation

- `pip install fillmydb[peewee]` if you plan to use it with peewee models
- `pip install fillmydb[django]` if you plan to use it with djanog models **(not implemented yet)**
- `pip install fillmydb[sqlalchemy]` if you plan to use it with sqlalchemy models **(not implemented yet)**


## Usage with [`fake-factory`](https://github.com/joke2k/faker)


Generating instances for a single model:

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

Generating instances for multipe models:

```python

	from tests.models import User, Post, Like

    import faker

    factory = faker.Factory.create()

    wrapper = ModelWrapper(User, Like, Post)

    wrapper[User].name = FieldSpec(factory.name)
    wrapper[User].username = FieldSpec(factory.user_name)
    wrapper[User].description = FieldSpec(factory.text)
    wrapper[User].password_hash = FieldSpec(factory.binary, length=25)
    wrapper[User].email = FieldSpec(factory.email)
    wrapper[User].visits = FieldSpec(factory.pyint)

    wrapper[Post].title = FieldSpec(lambda _: "test", 1)
    wrapper[Post].text = FieldSpec(factory.text)

    # generating 10 users, 100 likes and 20 posts 
    wrapper.generate(10, 100, 20)

```

## General workflow

Pseudo-code:

```python
initial_to_order_queue()
while models_to_process():
	model = get_next_model()
	
	if model.has_unresolved_dependency():
		push_back_to_queue(model)
		
	# process model
	for _ in range(number_of_instances):
		for field in model.fields():
			# resolve_field(field)
			if field == ForeignKey:
				field = get_random_ref_model_instance()
			else:
				field = resolve_normal()
	mark_as_processed(model)
```
