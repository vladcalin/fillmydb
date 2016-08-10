import peewee

_db = peewee.SqliteDatabase("test.db")


class TestModel(peewee.Model):
    username = peewee.CharField()
    password_hash = peewee.CharField()

    email = peewee.CharField()
    phone_no = peewee.CharField()

    ip = peewee.CharField()
    visits = peewee.IntegerField(default=0)

    class Meta:
        database = _db