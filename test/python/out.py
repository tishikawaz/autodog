"""
Module for working with Fortran code.
This module provides a class `FortranCode` that allows reading and
writing Fortran code files. It uses the `FortranAST` class from the
`ast.fortran` module to parse the code and generate an abstract syntax
tree.
Classes:
- FortranCode: Represents a Fortran code file.
Methods:
- __init__(self, filepath: str): Initializes a new instance of the
`FortranCode` class with the specified file path.
- to_str(self) -> str: Converts the abstract syntax tree to a string
representation.
- write(self, filepath) -> None: Writes the Fortran code to the
specified file path.
- write(self) -> None: Writes the Fortran code to the original file path
specified during initialization.
"""
from .ast.fortran import FortranAST, ModuleNode, TypeNode, FunctionNode, SubroutineNode, ProgramNode
from .docengine import DocEngine
from functools import singledispatchmethod

class FortranCode:
    """
    Represents a Fortran code file.
    Args:
        filepath (str): The path to the Fortran code file.
    Attributes:
        filepath (str): The path to the Fortran code file.
        tree (FortranAST): The abstract syntax tree of the Fortran code.
    Methods:
        to_str: Converts the Fortran code to a string representation.
        write: Writes the Fortran code to a file.
    """

    def __init__(self, filepath: str):
        """
        Initializes an instance of the class with the given filepath.
        Parameters:
        - filepath (str): The path to the file containing the Fortran code.
        Returns:
        - None
        Side Effects:
        - Sets the `filepath` attribute of the instance to the given filepath.
        - Reads the contents of the file and creates a `FortranAST` object
        representing the code.
        - Sets the `tree` attribute of the instance to the created `FortranAST`
        object.
        """
        self.filepath = filepath
        with open(filepath, 'r') as f:
            self.tree = FortranAST(f.read())

    def to_str(self) -> str:
        """
        Converts the tree object to a string representation.
        Returns:
            str: The string representation of the tree object.
        """
        return self.tree.to_str()

    @singledispatchmethod
    def write(self, filepath) -> None:
        """
        Write the string representation of the object to a file.
        Parameters:
        - filepath (str): The path to the file where the object will be written.
        Returns:
        None
        """
        with open(filepath, 'w') as f:
            f.write(self.to_str())

    @write.register
    def write(self) -> None:
        """
        Write the contents of the object to a file.
        This function opens the file specified by `self.filepath` in write mode
        and writes the string representation of the object using the `to_str()`
        method. The file is closed automatically after writing.
        Parameters:
            self: The object itself.
        Returns:
            None
        """
        with open(self.filepath, 'w') as f:
            f.write(self.to_str())