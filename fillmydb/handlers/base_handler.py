import abc


class BaseHandler(metaclass=abc.ABCMeta):
    """
    Base class for database model handlers.
    """

    def __init__(self, model):
        self.model = model

        self.create_table_if_not_exists()
        self.fields, self.fields_names = self.get_fields()
        self.ref_models = self.get_referenced_models()

    @abc.abstractmethod
    def create_table_if_not_exists(self):
        pass

    @abc.abstractmethod
    def get_fields(self):
        """
        Returns a tuple(list, list) where the first list is the list of field objects, and the second list is the
        list of field names
        :return:
        """
        pass

    @abc.abstractmethod
    def create_instance(self, **attrs):
        """
        Creates an instance having the *attrs* attributes without saving it to database. For testing purposes
        :param attrs:
        :return:
        """
        pass

    @abc.abstractmethod
    def create_instance_and_persist(self, **attrs):
        """
        Same as BaseHandler.create_instance but saves the instance to database.
        :param attrs:
        :return:
        """
        pass

    @abc.abstractmethod
    def get_referenced_models(self):
        """
        Returns a list of models referenced by this model.
        :return:
        """
        pass

    @abc.abstractmethod
    def is_value_field(self, field_name):
        """
        Indicates if the *field_name* field has a normal value and not a database dependent one (such as ForeignKey)
        :param field_name:
        :return: True or False
        """
        pass

    @abc.abstractmethod
    def is_foreign_key_field(self, field_name):
        """
        Indicates if the *field_name* field is a foreign key or not.
        :param field_name:
        :return: True or False
        """
        pass

    @abc.abstractmethod
    def get_referenced_model_by_field_name(self, field_name):
        """
        If *field_name* is a foreign key, returns the referenced model
        :param field_name:
        :return:
        """
        pass

    @abc.abstractmethod
    def pick_random_instance(self):
        """
        Returns a random instance from the table.
        :return:
        """
        pass

    @abc.abstractmethod
    def __repr__(self):
        pass
