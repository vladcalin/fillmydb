import peewee

_db = peewee.SqliteDatabase("test.db")


class TestModel(peewee.Model):
    client_name = peewee.CharField()
    password_hash = peewee.BlobField()

    email = peewee.CharField()
    visits = peewee.IntegerField()

    description = peewee.CharField()

    class Meta:
        database = _db