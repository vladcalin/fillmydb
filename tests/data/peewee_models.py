import peewee


DB_NAME = "test2.db"
database_obj = peewee.SqliteDatabase("test2.db")


class User(peewee.Model):
    name = peewee.CharField()
    username = peewee.CharField()
    password_hash = peewee.BlobField()

    email = peewee.CharField()
    visits = peewee.IntegerField()

    description = peewee.CharField()

    class Meta:
        database = database_obj


class Post(peewee.Model):
    title = peewee.CharField()
    text = peewee.CharField()

    by_user = peewee.ForeignKeyField(User)

    class Meta:
        database = database_obj


class Like(peewee.Model):
    by_user = peewee.ForeignKeyField(User)
    to_post = peewee.ForeignKeyField(Post)

    class Meta:
        database = database_obj
