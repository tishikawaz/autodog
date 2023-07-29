"""The following is a docstring for the given Python code:
This module defines a class DummyEngine that inherits from DocEngine. It
provides methods to generate dummy documentation for code, modules,
classes, and functions.

Attributes
----------
    dummy_doc (str): A string representing the dummy document.

Methods
-------
    generate_code_doc(code: str, lang: str='') -> str:
        Returns the dummy document.
    generate_module_doc(code: str, lang: str='') -> str:
        Returns the dummy document.
    generate_class_doc(code: str, lang: str='') -> str:
        Returns the dummy document.
    generate_func_doc(code: str, lang: str='') -> str:
        Returns the dummy document.

"""
from autodog.engine.base import Engine


class DummyEngine(Engine):
    """The `DummyEngine` class is a subclass of `DocEngine` and provides dummy
    documentation for code, modules, classes, and functions.
    The class has four methods, `generate_code_doc`, `generate_module_doc`,
    `generate_class_doc`, and `generate_func_doc`, which take in a `code`
    string and an optional `lang` string and return the same dummy document
    for all of them.
    The `__init__` method initializes the `dummy_doc` attribute with a
    default value of "This is a dummy document."
    Attributes:
        dummy_doc (str): A string representing the dummy document.

    Methods
    -------
        __init__(self, dummy_doc='This is a dummy document.'):
            Initialize the class with a dummy document.
        generate_doc(self, code: str, lang: str, statement_kind: str,
        context='') -> str:
            Generate documentation for a given code snippet.
    """

    def __init__(self, dummy_doc="This is a dummy document.") -> None:
        """Initialize the class with a dummy document.

        Args:
        ----
            dummy_doc (str): A string representing the dummy document. Default
            is 'This is a dummy document.'.

        Attributes:
        ----------
            dummy_doc (str): A string representing the dummy document.

        Returns:
        -------
            None.
        """
        self.dummy_doc = dummy_doc

    def generate_doc(
        self, code: str, lang: str, statement_kind: str, context="",
    ) -> str:
        """Generate documentation for a given code snippet.

        Args:
        ----
            self: The object instance.
            code (str): The code snippet for which documentation is to be
            generated.
            lang (str): The programming language of the code snippet. Default is
            an empty string.
            statement_kind (str): The kind of statement in the code snippet.
            context (str): Additional context information. Default is an empty
            string.

        Returns:
        -------
            str: The generated documentation for the code snippet.
        """
        return self.dummy_doc
