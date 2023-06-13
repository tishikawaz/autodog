"""The `DocEngine` class is an abstract base class that defines the
interface for generating documentation for code, modules, classes, and
functions. It cannot be instantiated directly and must be subclassed to
provide concrete implementations for the abstract methods. The
`generate_code_doc`, `generate_module_doc`, `generate_class_doc`, and
`generate_func_doc` methods take in a `code` parameter, which is the
code to be documented, and an optional `lang` parameter, which specifies
the programming language of the code. These methods return a string that
represents the documentation for the corresponding code element. If the
`lang` parameter is not specified, the default language is assumed to be
Python. If any of the abstract methods are called on an instance of a
subclass that has not implemented them, a `NotImplementedError` will be
raised. Each of the abstract methods is documented with its own
docstring, specifying its parameters, return type, and any exceptions
that may be raised. The `__init__` method of the `DocEngine` class
raises a `NotImplementedError` with a message indicating that
`DocEngine` is an abstract class. This method is typically called when
an instance of the class is created. Since `DocEngine` is an abstract
class, it cannot be instantiated directly and must be subclassed
instead.
"""
from abc import ABCMeta, abstractmethod

class DocEngine(metaclass=ABCMeta):
    """The `DocEngine` class is an abstract base class that defines the
    interface for generating documentation for code, modules, classes, and
    functions. It cannot be instantiated directly and must be subclassed to
    provide concrete implementations for the abstract methods
    `generate_code_doc`, `generate_module_doc`, `generate_class_doc`, and
    `generate_func_doc`. Each of these methods takes a `code` parameter,
    which is the code to be documented, and an optional `lang` parameter,
    which specifies the programming language of the code. The methods return
    a string containing the generated documentation. If the `lang` parameter
    is not specified, the default language is assumed to be Python. If any
    of the abstract methods are called on an instance of `DocEngine`, a
    `NotImplementedError` will be raised.
    """

    def __init__(self):
        """The `__init__` method of the `DocEngine` class raises a
        `NotImplementedError` with a message indicating that `DocEngine` is an
        abstract class. This method is typically called when an instance of the
        class is created. Since `DocEngine` is an abstract class, it cannot be
        instantiated directly and must be subclassed instead.
        """
        raise NotImplementedError('DocEngine is an abstract class.')

    @abstractmethod
    def generate_code_doc(self, code: str, lang='') -> str:
        """The `generate_code_doc` method is an abstract method of the `DocEngine`
        class. It takes in two parameters: `code`, which is the code to be
        documented, and `lang`, which is an optional parameter specifying the
        language of the code. The method returns a string that represents the
        documentation of the given code. If the method is called directly, it
        will raise a `NotImplementedError` since `DocEngine` is an abstract
        class and this method must be implemented by its subclasses.
        """
        raise NotImplementedError('DocEngine is an abstract class.')

    @abstractmethod
    def generate_module_doc(self, code: str, lang='') -> str:
        """The `generate_module_doc` method is an abstract method of the
        `DocEngine` class. It takes in two parameters: `code`, which is a string
        representing the code to be documented, and `lang`, which is an optional
        string representing the language of the code. The method returns a
        string representing the generated documentation.
        Since this is an abstract method, it must be implemented by any subclass
        of `DocEngine`. If it is called on an instance of `DocEngine`, it will
        raise a `NotImplementedError`.
        """
        raise NotImplementedError('DocEngine is an abstract class.')

    @abstractmethod
    def generate_class_doc(self, code: str, lang='') -> str:
        """The `generate_class_doc` method is an abstract method of the `DocEngine`
        class. It takes two parameters: `code`, which is a string representing
        the code of a class, and `lang`, which is an optional string
        representing the language of the code. The method returns a string
        representing the documentation of the class. Since this is an abstract
        method, it must be implemented by any subclass of `DocEngine`. If it is
        called on an instance of `DocEngine`, it will raise a
        `NotImplementedError`.
        """
        raise NotImplementedError('DocEngine is an abstract class.')

    @abstractmethod
    def generate_func_doc(self, code: str, lang='') -> str:
        """The `generate_func_doc` method is an abstract method that generates
        documentation for a given code snippet in a specified language. It takes
        in two parameters: `code` which is the code snippet for which
        documentation needs to be generated and `lang` which is the language in
        which the documentation needs to be generated. The default value for
        `lang` is an empty string. The method returns the generated
        documentation as a string. If the method is called directly, it raises a
        `NotImplementedError` since it is an abstract method and needs to be
        implemented in the child class.
        """
        raise NotImplementedError('DocEngine is an abstract class.')