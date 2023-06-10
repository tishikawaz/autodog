"""This module provides a class `FortranCode` that represents a Fortran code file. It uses
the `FortranAST` class from the `ast.fortran` module to parse the code and generate an
abstract syntax tree. The class provides methods to convert the AST to a string, insert
documentation using a `DocEngine` object, and write the modified code back to the
original file or a new file.

The `FortranCode` class has the following methods:

- `__init__(self, filepath: str)`: Initializes a `FortranCode` object with the path to a
Fortran code file. It reads the file and generates an AST using `FortranAST`.

- `to_str(self) -> str`: Returns a string representation of the AST.

- `insert_docs(self, engine: any, overwrite=False) -> None`: Inserts documentation for
each node in the AST using a `DocEngine` object. If `overwrite` is True, the original
code file is modified with the documentation. Otherwise, the modified code is written to
a new file.

- `write(self, filepath='') -> None`: Writes the modified code to the original file or a
new file specified by `filepath`. If `filepath` is not provided, the original file is
overwritten.

- `_write_to_original(self) -> None`: Helper method that writes the modified code to the
"""
from .ast.fortran import FortranAST, ModuleNode, TypeNode, FunctionNode, SubroutineNode, ProgramNode
from .docengine import DocEngine
from functools import singledispatchmethod

class FortranCode:
    """class FortranCode:
        A class to represent Fortran code and provide methods to manipulate it.

        Attributes
        ----------
        filepath : str
            The path to the Fortran code file.
        tree : FortranAST
            The abstract syntax tree of the Fortran code.

        Methods
        -------
        to_str() -> str:
            Returns the Fortran code as a string.
        insert_docs(engine: any, overwrite=False) -> None:
            Inserts documentation strings into the Fortran code using the specified
    documentation engine.
        write(filepath='') -> None:
            Writes the Fortran code to a file. If no filepath is provided, overwrites the
    original file.
        _write_to_original() -> None:
    """

    def __init__(self, filepath: str):
        """Initializes an instance of the class with the given filepath. The filepath should be a
        string representing the path to a Fortran file. The method reads the contents of the
        file and creates a Fortran Abstract Syntax Tree (AST) using the FortranAST library. The
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

    def insert_docs(self, engine: any, overwrite=False) -> None:
        """Inserts documents into a database engine for each node in the tree.

        Args:
            engine (any): The database engine to insert documents into.
            overwrite (bool, optional): Whether to overwrite existing documents. Defaults to
        False.

        Returns:
        """
        for node in self.tree.walk():
            self._insert_docs(node, engine, overwrite)

    def write(self, filepath='') -> None:
        """Writes the contents of the current object to a file.

        Args:
            filepath (str): The path of the file to write to. If not provided, the contents will
        be written to the original file.

        Returns:
        """
        if filepath == '':
            return self._write_to_original()
        with open(filepath, 'w') as f:
            f.write(self.to_str())

    def _write_to_original(self) -> None:
        """Writes the string representation of the object to the original file.

        Args:
            self: The object instance.

        Returns:
            None.

        Raises:
        """
        with open(self.filepath, 'w') as f:
            f.write(self.to_str())