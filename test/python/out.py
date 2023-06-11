"""This module provides a class `FortranCode` that represents a Fortran
code file. It uses the `FortranAST` class from the `ast.fortran` module
to parse the code and generate an abstract syntax tree. The class
provides methods to convert the AST to a string representation and to
write the code to a file.

Attributes:
    filepath (str): The path to the Fortran code file.

Methods:
    __init__(self, filepath: str): Initializes the `FortranCode` object
    by parsing the code file and generating an AST.
    to_str(self) -> str: Returns a string representation of the AST.
    write(self, filepath) -> None: Writes the code to the specified file
    path.
    write(self) -> None: Writes the code to the original file path
    specified during initialization.
"""
from .ast.fortran import FortranAST, ModuleNode, TypeNode, FunctionNode, SubroutineNode, ProgramNode
from .docengine import DocEngine
from functools import singledispatchmethod

class FortranCode:
    """The FortranCode class represents a Fortran code file. It takes a
    filepath as input and initializes an instance of the FortranAST class,
    which is used to parse the code. The class has a method to_str() that
    returns the parsed code as a string.

    The class also has a write() method that writes the parsed code to a
    file. This method is implemented using the singledispatchmethod
    decorator, which allows for different implementations of the method
    based on the type of argument passed.

    If a filepath is passed as an argument to the write() method, the parsed
    code is written to that file. If no argument is passed, the parsed code
    is written to the original filepath used to initialize the instance.
    """

    def __init__(self, filepath: str):
        """The `__init__` method initializes an instance of a class with a
        `filepath` parameter, which is a string representing the path to a
        Fortran file. The method reads the contents of the file using the `open`
        function and creates a `FortranAST` object from the file contents. The
        `FortranAST` object is stored as an attribute of the instance with the
        name `tree`.
        """
        self.filepath = filepath
        with open(filepath, 'r') as f:
            self.tree = FortranAST(f.read())

    def to_str(self) -> str:
        """Converts the tree structure to a string representation.

        Returns:
            A string representation of the tree structure.


        """
        return self.tree.to_str()

    @singledispatchmethod
    def write(self, filepath) -> None:
        """Writes the object to a file at the given file path.

        Args:
            filepath (str): The path of the file to write the object to.

        Returns:
            None: This method does not return anything.

        Raises:
            TypeError: If the object cannot be converted to a string.

        Example:
            >>> obj = MyClass()
            >>> obj.write('output.txt')
        """
        with open(filepath, 'w') as f:
            f.write(self.to_str())

    @write.register
    def write(self) -> None:
        """The `write` function is a method of a class that has been decorated with
        `@write.register`. It takes no arguments and returns `None`.

        When called, it opens a file specified by the `filepath` attribute of
        the class instance in write mode and writes the string representation of
        the instance (returned by the `to_str` method) to the file.

        This function is likely part of a larger system for writing data to
        files, with different methods registered for different data types.
        """
        with open(self.filepath, 'w') as f:
            f.write(self.to_str())