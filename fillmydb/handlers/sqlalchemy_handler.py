from fillmydb.handlers.base_handler import BaseHandler


class SqlalchemyHandler(BaseHandler):
    DB_TYPE = "sqlalchemy"

    def __init__(self, model):
        super(SqlalchemyHandler, self).__init__(model)

    def __repr__(self):
        "<SqlalchemyHandler for {}>".format(self.model.__name__)

    def get_referenced_model_by_field_name(self, field_name):
        pass

    def create_instance(self, **attrs):
        pass

    def pick_random_instance(self):
        pass

    def get_fields(self):
        field_names = []
        field_objs = []

        for field in self.model.__table__.columns:
            pass

    def create_table_if_not_exists(self):
        self.model.__table__.create(checkfirst=True)

    def is_value_field(self, field_name):
        return not self.is_foreign_key_field(field_name)

    def get_referenced_models(self):
        pass

    def create_instance_and_persist(self, **attrs):
        pass

    def is_foreign_key_field(self, field_name):
        pass