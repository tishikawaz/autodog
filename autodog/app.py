"""The following code defines functions for selecting an engine and code
based on file extension. It also includes custom exceptions for unknown
engine names and file extensions.
The `engine` function takes an optional argument `name` which defaults
to `'chatgpt'`. It returns an instance of either `ChatGPTEngine` or
`DummyEngine` based on the value of `name`. Additional keyword arguments
can be passed to the engine constructor.
The `code` function takes a file path as input and returns an instance
of either `FortranCode` or `PyCode` based on the file extension. It
raises an `UnknownFileExtension` exception if the file extension is not
recognized.
Note that the `FortranCode` and `PyCode` classes are imported from other
modules, and the `ChatGPTEngine` and `DummyEngine` classes are imported
from submodules of the `engine` module.
"""
from .code.fortran import FortranCode
from .code.python import PyCode
from .engine.chatgpt import ChatGPTEngine
from .engine.dummy import DummyEngine
import os

class UnknownEngineName(Exception):
    """The `UnknownEngineName` class is an exception that can be raised when an
    unknown engine name is encountered in the code. This exception can be
    used to handle cases where the engine name is not recognized or
    supported by the program.
    """
    pass

class UnknownFileExtension(Exception):
    """The `UnknownFileExtension` class is an exception that can be raised when
    encountering an unknown file extension. This can be used to handle cases
    where a program is unable to process a file due to an unsupported file
    extension.
    """
    pass

def engine(name='chatgpt', **kwargs):
    """The `engine` function is a factory function that returns an instance of
    a chatbot engine based on the `name` parameter passed to it. If `name`
    is `'chatgpt'`, it returns an instance of `ChatGPTEngine` class with any
    additional keyword arguments passed to it. If `name` is `'dummy'`, it
    returns an instance of `DummyEngine` class with any additional keyword
    arguments passed to it. If `name` is neither `'chatgpt'` nor `'dummy'`,
    it raises an `UnknownEngineName` exception.
    The function takes the following parameters:
    - `name`: a string representing the name of the engine to be returned.
    Default value is `'chatgpt'`.
    - `**kwargs`: any additional keyword arguments to be passed to the
    engine instance.
    The function returns an instance of the engine class specified by the
    `name` parameter.
    """
    if name == 'chatgpt':
        return ChatGPTEngine(**kwargs)
    elif name == 'dummy':
        return DummyEngine(**kwargs)
    raise UnknownEngineName

def code(filepath: str, **kwargs):
    """The `code` function takes a file path as input and returns an instance
    of either `FortranCode` or `PyCode` class based on the file extension.
    If the file extension is not recognized, it raises an
    `UnknownFileExtension` exception. The function also accepts additional
    keyword arguments.
    The function's docstring could be:
    Determine the type of code file based on its extension and return an
    instance of the corresponding class.
    :param filepath: A string representing the path to the code file.
    :type filepath: str
    :return: An instance of either FortranCode or PyCode class.
    :raises UnknownFileExtension: If the file extension is not recognized.
    """
    extension = os.path.splitext(filepath)[1][1:]
    if any((s in extension.lower() for s in ['f', 'f90'])):
        return FortranCode(filepath)
    elif 'py' in extension.lower():
        return PyCode(filepath)
    raise UnknownFileExtension