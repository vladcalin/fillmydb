Usage
=====

Value generation consists in the following steps:

.. warning::

    If you plan on using wrapping Django models, you must call the :py:func:`fillmydb.initialize_django` function
    **before importing your models**.


1. Wrap your models in a :py:class:`fillmydb.ModelWrapper` like this::

    wrapper = ModelWrapper(MyFirstModel, MySecondModel, ...)

2. Specify how the fields should look like using :py:class:`fillmydb.FieldSpec` instances::

    wrapper[MyFirstModel].first_field = FieldSpec(generate_func1)
    wrapper[MyFirstModel].second_field = FieldSpec(generate_func2)
    ...

    wrapper[MySecondModel].first_field = FieldSpec(generate_for_model2)
    wrapper[MySecondModel].second_field = FieldSpec(generate_for_model2_again)
    ...

3. Generate how many instances you need directly into your database::

    wrapper.generate(1000, 2000, ...)


**A complete example**

Lets assume we have the following peewee models::

    class User(peewee.Model):
        name = peewee.CharField()
        username = peewee.CharField()
        password_hash = peewee.BlobField()
        email = peewee.CharField()
        visits = peewee.IntegerField()
        description = peewee.CharField()


    class Post(peewee.Model):
        title = peewee.CharField()
        text = peewee.CharField()
        by_user = peewee.ForeignKeyField(User)


    class Like(peewee.Model):
        by_user = peewee.ForeignKeyField(User)
        to_post = peewee.ForeignKeyField(Post)

Now let's generate our instances::

    wrapper = ModelWrapper(User, Post, Like)  # order doesn't matter
    factory = faker.Factory.create()  # we use the fake-factory module generate nice-looking data

    wrapper[User].name = FieldSpec(factory.name)
    wrapper[User].username = FieldSpec(factory.user_name)
    wrapper[User].description = FieldSpec(factory.text)
    wrapper[User].password_hash = FieldSpec(factory.binary, length=25)
    wrapper[User].email = FieldSpec(factory.email)
    wrapper[User].visits = FieldSpec(factory.pyint)

    wrapper[Post].title = FieldSpec(faker.sentence)
    wrapper[Post].text = FieldSpec(factory.text)

    wrapper.generate(100, 200, 300)

Now we have 100 fresh instances of ``User``, 200 instances of ``Post`` and 300 instances of ``Like``