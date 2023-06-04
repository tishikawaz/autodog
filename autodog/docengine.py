from abc import ABCMeta, abstractmethod

class DocEngine(metaclass=ABCMeta):
    def __init__(self, *args, **kwargs):
        raise NotImplementedError('DocEngine is an abstract class.')

    @abstractmethod
    def generate_code_doc(self, code) -> str:
        raise NotImplementedError('DocEngine is an abstract class.')

    @abstractmethod
    def generate_module_doc(self, code) -> str:
        raise NotImplementedError('DocEngine is an abstract class.')

    @abstractmethod
    def generate_class_doc(self, code) -> str:
        raise NotImplementedError('DocEngine is an abstract class.')

    @abstractmethod
    def generate_func_doc(self, code) -> str:
        raise NotImplementedError('DocEngine is an abstract class.')