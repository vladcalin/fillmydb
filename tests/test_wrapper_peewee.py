import os
from unittest import TestCase

from peewee import Field, CharField, BlobField, IntegerField

from tests.data.peewee_models import User, Post, Like, database_obj, DB_NAME
from fillmydb.handlers.peewee_handler import PeeweeHandler


class PeeweeBasicFunctionalityTestCases(TestCase):
    @classmethod
    def setUpClass(cls):
        for model in [User, Post, Like]:
            model.create_table(fail_silently=True)

    @classmethod
    def tearDownClass(cls):
        database_obj.close()
        os.remove(DB_NAME)

    # actual tests

    def test_create_table_if_not_exists(self):
        handler = PeeweeHandler(Like)

        handler.create_table_if_not_exists()
        self.assertTrue(Like.table_exists())

        Like.drop_table()
        handler.create_table_if_not_exists()
        self.assertTrue(Like.table_exists())

    def test_get_fields(self):
        handler = PeeweeHandler(User)

        fields_objs, fields_names = handler.get_fields()
        self.assertIsInstance(fields_objs, list)
        self.assertIsInstance(fields_names, list)

        expected_fields = ["id", "name", "username", "password_hash", "email", "visits", "description"]
        self.assertCountEqual(fields_names, expected_fields)

        for field in fields_objs:
            self.assertIsInstance(field, Field)

        self.assertIsInstance(fields_objs[fields_names.index("id")], IntegerField)
        self.assertIsInstance(fields_objs[fields_names.index("name")], CharField)
        self.assertIsInstance(fields_objs[fields_names.index("username")], CharField)
        self.assertIsInstance(fields_objs[fields_names.index("password_hash")], BlobField)
        self.assertIsInstance(fields_objs[fields_names.index("email")], CharField)
        self.assertIsInstance(fields_objs[fields_names.index("visits")], IntegerField)
        self.assertIsInstance(fields_objs[fields_names.index("description")], CharField)

    def test_create_instance(self):
        handler = PeeweeHandler(User)

        instance = handler.create_instance(
            name="test_name",
            username="test_username",
            password_hash="test_hash",
            email="email_email",
            visits=10,
            description="test_description"
        )

        self.assertEqual(instance.name, "test_name")
        self.assertEqual(instance.username, "test_username")
        self.assertEqual(instance.password_hash, "test_hash")
        self.assertEqual(instance.email, "email_email")
        self.assertEqual(instance.visits, 10)
        self.assertEqual(instance.description, "test_description")

        self.assertEqual(User.select(User.username == "test_name").count(), 0)

    def test_create_instance_and_persist(self):
        handler = PeeweeHandler(User)

        instance = handler.create_instance_and_persist(
            name="test_name",
            username="test_username",
            password_hash="test_hash",
            email="email_email",
            visits=10,
            description="test_description"
        )

        self.assertEqual(instance.name, "test_name")
        self.assertEqual(instance.username, "test_username")
        self.assertEqual(instance.password_hash, "test_hash")
        self.assertEqual(instance.email, "email_email")
        self.assertEqual(instance.visits, 10)
        self.assertEqual(instance.description, "test_description")

        self.assertEqual(User.select(User.username == "test_name").count(), 1)

    def test_get_referenced_models(self):
        handler_like = PeeweeHandler(Like)
        handler_user = PeeweeHandler(User)
        handler_post = PeeweeHandler(Post)

        self.assertCountEqual(list(set(handler_user.get_referenced_models())), list(set()))
        self.assertCountEqual(list(set(handler_post.get_referenced_models())), list((User,)))
        self.assertCountEqual(list(set(handler_like.get_referenced_models())), list((User, Post)))

    def test_is_value_field(self):
        user_handler = PeeweeHandler(User)

        self.assertTrue(user_handler.is_value_field("name"))
        self.assertTrue(user_handler.is_value_field("username"))
        self.assertTrue(user_handler.is_value_field("email"))
        self.assertTrue(user_handler.is_value_field("password_hash"))
        self.assertTrue(user_handler.is_value_field("description"))
        self.assertTrue(user_handler.is_value_field("visits"))

        post_handler = PeeweeHandler(Post)

        self.assertTrue(post_handler.is_value_field("title"))
        self.assertTrue(post_handler.is_value_field("text"))
        self.assertFalse(post_handler.is_value_field("by_user"))

        like_handler = PeeweeHandler(Like)

        self.assertFalse(like_handler.is_value_field("by_user"))
        self.assertFalse(like_handler.is_value_field("to_post"))

        with self.assertRaises(AttributeError):
            like_handler.is_value_field("non_existing")

    def test_is_foreign_key_field(self):
        user_handler = PeeweeHandler(User)

        self.assertFalse(user_handler.is_foreign_key_field("name"))
        self.assertFalse(user_handler.is_foreign_key_field("username"))
        self.assertFalse(user_handler.is_foreign_key_field("email"))
        self.assertFalse(user_handler.is_foreign_key_field("password_hash"))
        self.assertFalse(user_handler.is_foreign_key_field("description"))
        self.assertFalse(user_handler.is_foreign_key_field("visits"))

        post_handler = PeeweeHandler(Post)

        self.assertFalse(post_handler.is_foreign_key_field("title"))
        self.assertFalse(post_handler.is_foreign_key_field("text"))
        self.assertTrue(post_handler.is_foreign_key_field("by_user"))

        like_handler = PeeweeHandler(Like)

        self.assertTrue(like_handler.is_foreign_key_field("by_user"))
        self.assertTrue(like_handler.is_foreign_key_field("to_post"))

        with self.assertRaises(AttributeError):
            like_handler.is_foreign_key_field("non_existing")

    def test_get_referenced_model_by_field_name(self):
        handler_like = PeeweeHandler(Like)
        handler_post = PeeweeHandler(Post)

        self.assertEqual(handler_post.get_referenced_model_by_field_name("by_user"), User)

        self.assertEqual(handler_like.get_referenced_model_by_field_name("by_user"), User)
        self.assertEqual(handler_like.get_referenced_model_by_field_name("to_post"), Post)

        with self.assertRaises(AttributeError):
            handler_like.get_referenced_model_by_field_name("non_existing_field")

        with self.assertRaises(AttributeError):
            handler_post.get_referenced_model_by_field_name("text")

    def test_get_random_instance(self):
        User.drop_table()
        User.create_table()

        for i in range(20):
            User.create(
                name="name{}".format(i),
                username="username{}".format(i),
                password_hash="password{}".format(i),
                email="email{}".format(i),
                description="description{}".format(i),
                visits=i
            )

        handler = PeeweeHandler(User)
        for _ in range(20):
            instance = handler.pick_random_instance()
            self.assertRegex(instance.name, "name\d+")
            self.assertRegex(instance.username, "username\d+")
            self.assertRegex(instance.password_hash, b"password\d+")
            self.assertRegex(instance.email, "email\d+")
            self.assertRegex(instance.description, "description\d+")
            self.assertRegex(str(instance.visits), "\d+")
