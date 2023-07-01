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
from autodog.code.fortran import FortranCode
from autodog.code.python import PyCode
from autodog.engine.chatgpt import ChatGPTEngine
from autodog.engine.dummy import DummyEngine
import os
import argparse
import glob

class UnknownEngineName(Exception):
    """The `UnknownEngineName` class is an exception that can be raised when an
    unknown engine name is encountered in the code. This exception can be
    used to handle cases where the engine name is not recognized or
    supported by the program.
    """
    pass

class UnknownFileExtension(Exception):
    """The `UnknownFileExtension` class is an exception that can be raised when
    encountering an unknown file extension. This exception can be used to
    handle cases where a program is unable to process a file due to an
    unsupported file extension. Attributes: None. Methods: None.
    """
    pass

def engine(name='chatgpt', **kwargs):
    """The `engine` function is a factory function that returns an instance of
    a chatbot engine based on the `name` parameter passed to it.
    Parameters:
    - `name` (str): A string representing the name of the engine to be
    returned. Default value is `'chatgpt'`.
    - `**kwargs` (dict): Any additional keyword arguments to be passed to
    the engine instance.
    Returns:
    - An instance of the engine class specified by the `name` parameter.
    Raises:
    - `UnknownEngineName`: If `name` is neither `'chatgpt'` nor `'dummy'`.
    Example:
    engine('chatgpt', model='gpt2', temperature=0.7)
    """
    if name == 'chatgpt':
        return ChatGPTEngine(**kwargs)
    elif name == 'dummy':
        return DummyEngine(**kwargs)
    raise UnknownEngineName

def code(filepath: str, **kwargs):
    """Determine the type of code file based on its extension and return an
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

def app():
    """
    AutoDog Application
    This function is the entry point for the AutoDog application. It
    generates documentation for a specific segment of code.
    Args:
        path (str): The path to the code segment to be documented.
        -e, --engine (str, optional): The documentation generation engine name.
        Defaults to 'chatgpt'.
        -k, --key (str, optional): The API key for the documentation generation
        engine. Defaults to an empty string.
        -r, --recursively (bool, optional): Flag to recursively generate
        documentation in the entire directory structure. Defaults to False.
        -o, --overwrite (bool, optional): Flag to overwrite existing
        documentation. Defaults to False.
    Returns:
        None
    """
    parser = argparse.ArgumentParser(prog='AutoDog', description='An automatic documentation generator to document a specific segment of code')
    parser.add_argument('path')
    parser.add_argument('-e', '--engine', help='Documentation generation engin name.', default='chatgpt')
    parser.add_argument('-k', '--key', help='API key.', default='')
    parser.add_argument('-r', '--recursively', help='Recursively generate documentation in the entire directory structure.', default=False)
    parser.add_argument('-o', '--overwrite', help='Overwrite documentation.', default=False)
    args = parser.parse_args()
    e = engine(name=args.engine, api_key=args.key)
    if args.recursively:
        for dir in glob.glob(f'{args.path}/**/', recursive=True):
            for file in glob.glob(f'{dir}/*.py'):
                c = code(file)
                print('Insert documentation in', file)
                c.insert_docs(e, overwrite=args.overwrite)
                c.write()
    else:
        c = code(args.path)
        c.insert_docs(e, overwrite=args.overwrite)
        c.write()