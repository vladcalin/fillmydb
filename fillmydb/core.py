try:
    import peewee

    from fillmydb.orm_wrappers.peewee_wrapper import PeeweeWrapper
except ImportError:
    peewee = None
    PeeweeWrapper = None

try:
    import django
except ImportError:
    django = None

try:
    import sqlalchemy
except ImportError:
    sqlalchemy = None

from tests.models import TestModel


class DataModel:
    def __init__(self, **model_specs):
        self.dict = model_specs

    def to_dict(self):
        return self.dict

    def get(self, key, default=None):
        return self.dict.get(key, default)


class ModelWrapper:
    def __init__(self, model, data_model, localization="en_GB"):
        self.model = model
        self.data_model = data_model
        self.localization = localization
        self.model_wrapper = self.get_model_framework(self.model)

    def get_model_framework(self, model):
        if peewee:
            if issubclass(model, peewee.Model):
                return PeeweeWrapper(peewee_model=model,
                                     data_model=self.data_model.to_dict(),
                                     localization=self.localization)

    def generate(self, count):
        self.model_wrapper.generate_batch(count=count)


if __name__ == '__main__':
    wrapper = ModelWrapper(TestModel, DataModel(
        username="user_name",
        password_hash="md5",
        email="free_email",
        phone_no="phone_number",
        ip="ipv4"
    ))
    wrapper.generate(100)
