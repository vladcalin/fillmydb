import random

from django.db.models import Field, ForeignKey, ManyToManyField, OneToOneField, ManyToOneRel
from django.db.models.aggregates import Count
from django.conf import settings
import django.core.exceptions

from fillmydb.handlers.base_handler import BaseHandler


class DjangoHandler(BaseHandler):
    DB_TYPE = "django"

    def __init__(self, model):
        super(DjangoHandler, self).__init__(model)

    def create_table_if_not_exists(self):
        # no need to handle table creation as django handles it
        pass

    def get_fields(self):
        field_names = []
        field_objs = []
        for field_obj in self.model._meta.get_fields():
            if field_obj.concrete:
                field_objs.append(field_obj)
                field_names.append(field_obj.name)
        print(field_names)
        print(field_objs)
        return field_objs, field_names

    def is_value_field(self, field_name):
        return not self.is_foreign_key_field(field_name)

    def is_foreign_key_field(self, field_name):
        if field_name not in self.fields_names:
            return False
        field_object = self.model._meta.get_field(field_name)
        if field_object.get_internal_type() == "ForeignKey":
            return True
        return False

    def get_referenced_models(self):
        models = []
        for field in self.fields_names:
            if self.is_foreign_key_field(field):
                models.append(self.get_referenced_model_by_field_name(field))
        print("{} : {}".format(self.model, models))
        return models

    def get_referenced_model_by_field_name(self, field_name):
        if self.is_foreign_key_field(field_name):
            ref_model = self.model._meta.get_field(field_name).rel.to
            if ref_model != self.model:
                return ref_model
        raise ValueError("Fied '{}' is not a foreign key".format(field_name))

    def create_instance_and_persist(self, **attrs):
        return self.model.objects.create(**attrs)

    def create_instance(self, **attrs):
        return self.model(**attrs)

    def __repr__(self):
        return "<DjangoHandler for {}>".format(self.model.__name__)

    def pick_random_instance(self):
        count = self.model.objects.all().count()
        random_index = random.randint(0, count - 1)
        return self.model.objects.all()[random_index]
