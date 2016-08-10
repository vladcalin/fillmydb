import time

import peewee

from fillmydb.base import BaseWrapper

from tests.models import TestModel


class PeeweeWrapper(BaseWrapper):
    def __init__(self, peewee_model, data_model, generator="faker", localization=None):
        if not issubclass(peewee_model, peewee.Model):
            raise TypeError("Not a peewee model")

        self.model = peewee_model
        self.model.create_table(fail_silently=True)

        self.data_model = data_model

        self.fields = self.parse_fields(self.model)
        self.generator = self.get_generator(generator, localization)

    def parse_fields(self, model):
        field_list = []
        for attr_name in dir(self.model):
            attr = getattr(self.model, attr_name)
            if not isinstance(attr, peewee.Field):
                continue
            field_list.append(attr_name)
        return field_list

    def generate_instance(self):
        model_instance = self.model()
        for field in self.fields:
            to_generate = self.data_model.get(field, None)
            if not to_generate:
                continue
            generated_value = self.generator.get_value(self.data_model[field])
            setattr(model_instance, field, generated_value)
        model_instance.save()
        model_instance._meta.database.commit()

    def generate_batch(self, count):
        start = time.time()
        [self.generate_instance() for _ in range(count)]
        print("Generation finished in {} seconds".format(time.time() - start))


if __name__ == '__main__':
    wrapper = PeeweeWrapper(TestModel, {"username": "user_name", "password_hash": "md5", "email": "free_email",
                                        "phone_no": "phone_number", "ip": "ipv4"}, localization="de_DE")

    print(wrapper.generate_batch(1000))
