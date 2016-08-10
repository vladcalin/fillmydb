import importlib
import abc


class BaseWrapper(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def parse_fields(self, model):
        pass

    def get_generator(self, generator_name, localization=None):

        class Generator:

            def __init__(self, gen_class):
                self.gen_class = gen_class

            def get_value(self, value_id):
                return getattr(self.gen_class, value_id)()

        if generator_name == "faker":
            module = importlib.import_module("faker")
            if localization:
                return Generator(module.Factory.create(localization))
            else:
                return Generator(module.Factory.create())
