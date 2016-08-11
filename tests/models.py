import peewee

_db = peewee.SqliteDatabase("test.db")


class User(peewee.Model):
    name = peewee.CharField()
    username = peewee.CharField()
    password_hash = peewee.BlobField()

    email = peewee.CharField()
    visits = peewee.IntegerField()

    description = peewee.CharField()

    class Meta:
        database = _db


class Post(peewee.Model):
    title = peewee.CharField()
    text = peewee.CharField()

    by_user = peewee.ForeignKeyField(User)


class Like(peewee.Model):
    by_user = peewee.ForeignKeyField(User)
    to_post = peewee.ForeignKeyField(Post)
