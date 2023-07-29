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
The module also defines two custom exceptions: `UnknownEngineName` and
`UnknownFileExtension`. These exceptions can be raised when encountering
unknown engine names or file extensions, respectively.
"""
import os

from autodog.code.fortran import FortranCode
from autodog.code.python import PyCode
from autodog.engine.chatgpt import ChatGPTEngine
from autodog.engine.dummy import DummyEngine
from autodog.docmodel.docstring import Docstring
from autodog.docmodel.google import GoogleStyleDocstring
from autodog.docmodel.javadoc import Javadoc
from autodog.docmodel.numpy import NumpyStyleDocstring
from autodog.docmodel.restructuredtext import ReStructuredText

class UnknownEngineName(Exception):
    pass



class UnknownFileExtension(Exception):
    pass

class UnknownDocType(Exception):
    pass

def engine(name:str="chatgpt", **kwargs):
    """The `engine` function is a factory function that returns an instance of
    a chatbot engine based on the `name` parameter passed to it.

    Parameters
    ----------
    - `name` (str): A string representing the name of the engine to be
    returned. Default value is `'chatgpt'`.
    - `**kwargs` (dict): Any additional keyword arguments to be passed to
    the engine instance.

    Returns
    -------
    - An instance of the engine class specified by the `name` parameter.

    Raises
    ------
    - `UnknownEngineName`: If `name` is neither `'chatgpt'` nor `'dummy'`.
    Example:
    engine('chatgpt', model='gpt2', temperature=0.7).
    """
    if name == "chatgpt":
        return ChatGPTEngine(**kwargs)
    elif name == "dummy":
        return DummyEngine(**kwargs)
    raise UnknownEngineName(f"{name} is not supported.")


def code(filepath:str, **kwargs):
    """Determine the type of code file based on its extension and return an
    instance of the corresponding class.
    :param filepath: A string representing the path to the code file.
    :type filepath: str
    :return: An instance of either FortranCode or PyCode class.
    :raises UnknownFileExtension: If the file extension is not recognized.
    """
    extension = os.path.splitext(filepath)[1][1:]
    if any(s in extension.lower() for s in ["f", "f90"]):
        return FortranCode(filepath)
    elif "py" in extension.lower():
        return PyCode(filepath)
    raise UnknownFileExtension(f"{extension} is not supported.")

def doc_model(model_name:str="docstring", **kwarg):
    if model_name == "docstring":
        return Docstring(**kwarg)
    elif model_name == "google style docstring":
        return GoogleStyleDocstring(**kwarg)
    elif model_name == "numpy style docstring":
        return NumpyStyleDocstring(**kwarg)
    elif model_name == "reStructuredText":
        return ReStructuredText(**kwarg)
    elif model_name == "javadoc":
        return Javadoc(**kwarg)
    raise UnknownDocType(f"{model_name} is not supported.")