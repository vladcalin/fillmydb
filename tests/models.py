import peewee

_db = peewee.SqliteDatabase("test.db")


class TestModel(peewee.Model):
    username = peewee.CharField()
    password_hash = peewee.CharField()

    class Meta:
        database = _db