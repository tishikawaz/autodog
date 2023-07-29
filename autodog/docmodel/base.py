from abc import ABCMeta, abstractmethod

class DocModel(metaclass=ABCMeta):
    def __init__(self, **kwarg):
        pass

    @abstractmethod
    def function_format(self) -> str:
        raise NotImplementedError("DocModel is an abstract class.")

    @abstractmethod
    def class_format(self) -> str:
        raise NotImplementedError("DocModel is an abstract class.")

    @abstractmethod
    def module_format(self) -> str:
        raise NotImplementedError("DocModel is an abstract class.")