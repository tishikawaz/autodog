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
    functions.
    It cannot be instantiated directly and must be subclassed to provide
    concrete implementations for the abstract methods `generate_code_doc`,
    `generate_module_doc`, `generate_class_doc`, and `generate_func_doc`.
    Each of these methods takes a `code` parameter, which is the code to be
    documented, and an optional `lang` parameter, which specifies the
    programming language of the code. The methods return a string containing
    the generated documentation.
    If the `lang` parameter is not specified, the default language is
    assumed to be Python. If any of the abstract methods are called on an
    instance of `DocEngine`, a `NotImplementedError` will be raised.
    Attributes:
        None
    Methods:
        __init__(): The `__init__` method of the `DocEngine` class raises a
        `NotImplementedError` with a message indicating that `DocEngine` is
        an abstract class. This method is typically called when an instance
        of the class is created. Since `DocEngine` is an abstract class, it
        cannot be instantiated directly and must be subclassed instead.
        generate_doc(code: str, lang: str, statement_kind: str, context='')
        -> str: The `generate_code_doc` method is an abstract method of the
        `DocEngine` class. It takes in two parameters: `code`, which is the
        code to be documented, and `lang`, which is an optional parameter
        specifying the language of the code. The method returns a string
        that represents the documentation of the given code. If the method
        is called directly, it will raise a `NotImplementedError` since
        `DocEngine` is an abstract class and this method must be implemented
        by its subclasses.
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
    def generate_doc(self, code: str, lang: str, statement_kind: str, context='') -> str:
        """The `generate_doc` method is an abstract method of the `DocEngine`
        class. It takes in two parameters: `code`, which is the code to be
        documented, and `lang`, which is an optional parameter specifying the
        language of the code. The method returns a string that represents the
        documentation of the given code. If the method is called directly, it
        will raise a `NotImplementedError` since `DocEngine` is an abstract
        class and this method must be implemented by its subclasses.
        """
        raise NotImplementedError('DocEngine is an abstract class.')