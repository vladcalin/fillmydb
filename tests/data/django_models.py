from django.db.models import Model, CharField, IntegerField, ForeignKey


class User(Model):
    name = CharField()
    username = CharField()
    password_hash = BlobField()
    email = CharField()
    visits = IntegerField()
    description = CharField()


class Post(Model):
    title = CharField()
    text = CharField()
    by_user = ForeignKey(User)


class Like(Model):
    by_user = ForeignKey(User)
    to_post = ForeignKey(Post)
