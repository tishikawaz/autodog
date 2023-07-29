"""Python module for working with Fortran code
This module provides a class `FortranCode` that allows you to read and manipulate Fortran code files. It uses the `FortranAST` class from the `ast.fortran` module to parse the code and create an abstract syntax tree (AST). The AST can then be converted back to a string representation of the code.
Todo:
- None
"""
from .ast.fortran import FortranAST, ModuleNode, TypeNode, FunctionNode, SubroutineNode, ProgramNode
from .docengine import DocEngine
from functools import singledispatchmethod

class FortranCode:
    """FortranCode
    This class represents a Fortran code file.
    Attributes:
        filepath (str): The path to the Fortran code file.
        tree (FortranAST): The abstract syntax tree of the Fortran code.
    Methods:
        - __init__(self, filepath: str): Initializes the FortranCode object with the given filepath. It also reads the file and creates the abstract syntax tree.
        - to_str(self) -> str: Converts the abstract syntax tree to a string representation.
        - write(self, filepath) -> None: Writes the string representation of the abstract syntax tree to the specified filepath.
        - write(self) -> None: Writes the string representation of the abstract syntax tree to the original filepath.
    """

    def __init__(self, filepath: str):
        """__init__
        This function initializes an instance of a class and reads a Fortran file to create an abstract syntax tree.
        Args:
            filepath (str): The path to the Fortran file.
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
        """one-line description:
        Converts the tree to a string representation.
        Description:
        This function converts the tree object to a string representation using the `to_str()` method of the tree.
        Args:
            None
        Returns:
            str: The string representation of the tree.
        Raises:
            None
        Yields:
            None
        Examples:
            ```
            tree = Tree()
            tree_str = tree.to_str()
            print(tree_str)
            ```
        Note:
            None
        """
        return self.tree.to_str()

    @singledispatchmethod
    def write(self, filepath) -> None:
        '''```
        @staticmethod
        def write(filepath: str) -> None:
            """
            Writes the content of the object to a file.
            Args:
                filepath (str): The path of the file to write.
            Returns:
                None
            Raises:
                FileNotFoundError: If the specified file path does not exist.
            Examples:
                obj = MyClass()
                obj.write('output.txt')
            Note:
                - This function will overwrite the content of the file if it already exists.
                - If the file does not exist, it will be created.
            """
            with open(filepath, 'w') as f:
                f.write(self.to_str())
        ```
        '''
        with open(filepath, 'w') as f:
            f.write(self.to_str())

    @write.register
    def write(self) -> None:
        """one-line description:
        Writes the string representation of an object to a file.
        Description:
        This function opens a file in write mode and writes the string representation of an object to the file.
        Args:
            None
        Returns:
            None
        Raises:
            None
        Yields:
            None
        Examples:
            ```
            obj = MyClass()
            obj.write()
            ```
        Note:
            None
        """
        with open(self.filepath, 'w') as f:
            f.write(self.to_str())