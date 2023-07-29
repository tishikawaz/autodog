"""FortranCode module
This module provides a class for working with Fortran code files. It
allows parsing and manipulating Fortran code using the FortranAST class
from the ast.fortran module. The parsed code can be converted to a
string representation and written to a file.
Todo: None
"""
from .ast.fortran import FortranAST, ModuleNode, TypeNode, FunctionNode, SubroutineNode, ProgramNode
from .docengine import DocEngine
from functools import singledispatchmethod

class FortranCode:
    """FortranCode
    This class represents a Fortran code file.
    Attributes:
        filepath (str): The path to the Fortran code file.
        tree (FortranAST): The abstract syntax tree representation of the
        Fortran code.
    Methods:
        __init__(self, filepath: str): Initializes a FortranCode object with
        the given filepath. It also reads the file and creates the abstract
        syntax tree.
        to_str(self) -> str: Converts the abstract syntax tree to a string
        representation.
        write(self, filepath) -> None: Writes the string representation of
        the abstract syntax tree to the specified filepath.
        write(self) -> None: Writes the string representation of the
        abstract syntax tree to the original filepath.
    """

    def __init__(self, filepath: str):
        """__init__
        This function initializes an instance of a class.
        Args:
            filepath (str): The path to the file that will be used to initialize
            the instance.
        Returns:
            None
        Raises:
            None
        Yields:
            None
        Examples:
            ```
            obj = ClassName(filepath)
            ```
        Note:
            None
        """
        self.filepath = filepath
        with open(filepath, 'r') as f:
            self.tree = FortranAST(f.read())

    def to_str(self) -> str:
        """to_str
        This function converts the tree object to a string representation.
        Args:
            None
        Returns:
            str : The string representation of the tree.
        Raises:
            None
        Yields:
            None
        Examples:
            ```
            tree = BinaryTree()
            tree.insert(5)
            tree.insert(3)
            tree.insert(7)
            print(tree.to_str())  # Output: "5, 3, 7"
            ```
        Note:
            None
        """
        return self.tree.to_str()

    @singledispatchmethod
    def write(self, filepath) -> None:
        """Writes the content of an object to a file.
        This function takes a filepath as an argument and writes the string
        representation of the object to the file specified by the filepath. The
        file is opened in write mode, and if the file already exists, its
        contents will be overwritten.
        Args:
            filepath (str): The path to the file where the object will be
            written.
        Returns:
            None: This function does not return any value.
        Raises:
            None: This function does not raise any exceptions.
        Examples:
            ```
            obj = MyClass()
            obj.write('output.txt')
            ```
        Note:
            This function assumes that the object has a `to_str()` method that
            returns a string representation of the object.
        """
        with open(filepath, 'w') as f:
            f.write(self.to_str())

    @write.register
    def write(self) -> None:
        """Writes the content of the object to a file.
        This function opens the file specified by `self.filepath` in write mode
        and writes the string representation of the object to the file.
        Args:
            None.
        Returns:
            None.
        Raises:
            None.
        Yields:
            None.
        Examples:
            ```
            obj = MyClass()
            obj.write()
            ```
        Note:
            This function will overwrite the contents of the file if it already
            exists.
        """
        with open(self.filepath, 'w') as f:
            f.write(self.to_str())