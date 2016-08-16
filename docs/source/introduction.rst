Introduction
============


Description
^^^^^^^^^^^

The ``fillmydb`` library aims to help you with quickly populating your database with
nice-looking data with as few lines of code as possible. Basically, all you have to do is
to wrap your models in a :py:class:`fillmydb.ModelWrapper`, assign to each field an instance of :py:class:`fillmydb.FieldSpec`
in order to determine how each filed should look like and then generate instances. The foreign keys are handled automatically.

The supported model types so far are:

- `peewee <http://docs.peewee-orm.com/en/latest/>`_
- `django <https://www.djangoproject.com/>`_

.. warning::

    At this moment, circular dependencies are not treated and may break the generation algorithm.


The generation algorithm simplified is the following::

    initially orderes the queue
    marks all models as unresovled
    while queue not empty:
        picks the next model with no unresolved dependencies
        for each instance:
            resolves each field in the model:
                if foreign key, picks a random instance of the referenced model
                otherwise, resolves as usual
            saves to database
        marks model as processed


In the next section will be described how to use the module


References
^^^^^^^^^^

- `fake-factory <https://github.com/joke2k/faker>`_ - generates good-looking test data
- `peewee <http://docs.peewee-orm.com/en/latest/>`_ - a nice ORM for SQLite, PostgreSQL, MySQL and others.
- `django <https://www.djangoproject.com/>`_ - a full-stack web framework.