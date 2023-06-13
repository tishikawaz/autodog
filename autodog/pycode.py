"""The `PyCode` class provides methods to manipulate Python code stored in
a file. It can parse the code into an abstract syntax tree, convert the
tree back to a string, write the code to a file, and insert
documentation strings generated by a `DocEngine` object into the code.
The `insert_docs` method walks through the tree and calls the
appropriate `_insert_docs` method based on the type of node encountered.
The `_insert_docs` methods generate documentation strings using the
`DocEngine` object and insert them into the code using the
`insert_docstring` function. The `offset_lines` function is a helper
function used by `insert_docstring` to properly format the documentation
string. The class takes a file path as input and parses the code using
the `ast` module. It provides methods to convert the parsed code back to
a string, write the code to a file, and insert documentation strings
into the code using a `DocEngine` object. The `insert_docs` method walks
through the parsed code and calls the appropriate `_insert_docs` method
based on the type of node encountered. The `_insert_docs` methods
generate documentation strings using the `DocEngine` object and insert
them into the code using the `insert_docstring` function. The `write`
method writes the contents of the current object to a file specified by
the `filepath` parameter. If `filepath` is an empty string, the method
writes to the original file. If `filepath` is not empty, the method
writes to the file specified by `filepath`. The method returns `None`.
The `insert_docs` method inserts documentation strings for all nodes in
the abstract syntax tree of the current object into the specified
database engine. If `overwrite` is set to `True`, overwrites existing
documentation strings in the database. The `offset_lines` function takes
in a string `doc` and an integer `level` as input and returns a modified
string with each line of the input string indented by `level` spaces,
except for the first and last lines. The `insert_docstring` function
adds a docstring to the given AST node. The node can be of type
`ast.AsyncFunctionDef`, `ast.FunctionDef`, `ast.ClassDef`, or
`ast.Module`. If the node is not of any of these types, the function
returns without doing anything. If the node already has a docstring, the
function replaces it with the new docstring. If the node does not have a
docstring, the function adds the new docstring as the first statement in
the node's body. The function also adjusts the indentation of the
docstring to match the indentation of the node's body.
"""
from .docengine import DocEngine
from functools import singledispatchmethod
import ast
import os

class PyCode:
    """This is a Python class that provides methods to manipulate Python code.
    The class takes a file path as input and parses the code using the `ast`
    module. It provides methods to convert the parsed code back to a string,
    write the code to a file, and insert documentation strings into the code
    using a `DocEngine` object. The `insert_docs` method walks through the
    parsed code and calls the appropriate `_insert_docs` method based on the
    type of node encountered. The `_insert_docs` methods generate
    documentation strings using the `DocEngine` object and insert them into
    the code using the `insert_docstring` function.
    """

    def __init__(self, filepath: str):
        """The following is a suggested docstring for the given Python code:
        Initialize a new instance of the class with the given file path. The
        file is opened in read mode and its contents are parsed using the ast
        module. The resulting abstract syntax tree is stored in the 'tree'
        attribute of the instance.
        :param filepath: A string representing the path to the file to be
        parsed.
        :type filepath: str
        :return: None
        :rtype: None
        The docstring provides a brief description of the function, its
        parameters, and its return value. It also explains what the function
        does and how it works.
        """
        self.filepath = filepath
        with open(filepath, 'r') as f:
            self.tree = ast.parse(f.read())

    def to_str(self) -> str:
        """Converts an abstract syntax tree (AST) to a string representation.
        Args:
            self: The AST object to be converted.
        Returns:
            A string representation of the AST.
        Raises:
            None.
        """
        return ast.unparse(self.tree)

    def write(self, filepath='') -> None:
        """The `write` method writes the contents of the current object to a file
        specified by the `filepath` parameter. If `filepath` is an empty string,
        the method writes to the original file. If `filepath` is not empty, the
        method writes to the file specified by `filepath`. The method returns
        `None`.
        """
        if filepath == '':
            return self._write_to_original()
        with open(filepath, 'w') as f:
            f.write(self.to_str())

    def _write_to_original(self) -> None:
        """The `_write_to_original` method writes the string representation of the
        object to the file specified by `self.filepath`. It takes no arguments
        and returns nothing (`None`). The file is opened in write mode (`'w'`)
        and any existing content is overwritten. If the file does not exist, it
        is created.
        """
        with open(self.filepath, 'w') as f:
            f.write(self.to_str())

    def insert_docs(self, engine: any, overwrite=False) -> None:
        """The `insert_docs` function inserts documentation strings for all nodes
        in the abstract syntax tree of the current object into the specified
        database engine. It takes two arguments: `engine`, which is the database
        engine to insert the documentation strings into, and `overwrite`
        (optional), which is a boolean value that determines whether to
        overwrite existing documentation strings in the database. The function
        returns `None`.
        The function iterates over all nodes in the abstract syntax tree using
        the `ast.walk` method and calls the `_insert_docs` method for each node,
        passing in the node, the database engine, and the `overwrite` flag.
        """
        for node in ast.walk(self.tree):
            self._insert_docs(node, engine, overwrite)

    @singledispatchmethod
    def _insert_docs(self, node: any, engine: DocEngine, overwrite: bool) -> None:
        """The `_insert_docs` function is a decorated method that inserts
        documentation for a given node using the specified documentation engine.
        It takes three arguments: `node`, which is the node for which
        documentation needs to be inserted, `engine`, which is the documentation
        engine to be used for inserting documentation, and `overwrite`, which is
        a flag indicating whether to overwrite existing documentation. The
        function returns `None`.
        """
        pass

    @_insert_docs.register
    def _(self, node: ast.Module, engine: DocEngine, overwrite: bool) -> None:
        """Registers a function `_` to insert documentation into a given
        `ast.Module` node using a specified `DocEngine`. If the `node` already
        has a docstring or `overwrite` is set to `True`, the function generates
        a new documentation using the `DocEngine` and inserts it into the
        `node`.
        **Args:**
        - `node` (ast.Module): The `ast.Module` node to insert documentation
        into.
        - `engine` (DocEngine): The `DocEngine` to use for generating
        documentation.
        - `overwrite` (bool): A flag indicating whether to overwrite an existing
        docstring in the `node`.
        **Returns:**
        - `None`
        """
        if ast.get_docstring(node) is None or overwrite:
            doc = engine.generate_module_doc(ast.unparse(node), lang='Python')
            insert_docstring(node, doc)

    @_insert_docs.register
    def _(self, node: ast.FunctionDef, engine: DocEngine, overwrite: bool) -> None:
        """This function is a decorator that registers a function to insert
        docstrings into Python code. It takes in three parameters: `node`, an
        AST node representing a function definition; `engine`, a `DocEngine`
        object used to generate the docstring; and `overwrite`, a boolean
        indicating whether to overwrite an existing docstring. If the `node`
        does not have a docstring or `overwrite` is `True`, the function
        generates a docstring using the `DocEngine` object and inserts it into
        the `node` using the `insert_docstring` function. The generated
        docstring is based on the unparsed source code of the `node` and the
        language is set to Python. The function returns `None`.
        """
        if ast.get_docstring(node) is None or overwrite:
            doc = engine.generate_func_doc(ast.unparse(node), lang='Python')
            insert_docstring(node, doc)

    @_insert_docs.register
    def _(self, node: ast.AsyncFunctionDef, engine: DocEngine, overwrite: bool) -> None:
        """Registers a function `_insert_docs` that takes in a node of type
        `ast.AsyncFunctionDef`, a `DocEngine` object, and a boolean `overwrite`.
        If the node already has a docstring or `overwrite` is True, the function
        generates a new docstring using the `generate_func_doc` method of the
        `DocEngine` object and inserts it into the node using the
        `insert_docstring` function. The function does not return anything.
        """
        if ast.get_docstring(node) is None or overwrite:
            doc = engine.generate_func_doc(ast.unparse(node), lang='Python')
            insert_docstring(node, doc)

    @_insert_docs.register
    def _(self, node: ast.ClassDef, engine: DocEngine, overwrite: bool) -> None:
        """This function is a decorator that registers a function to insert a
        docstring for a Python class definition. The function takes in three
        parameters:
        - `node`: an AST (Abstract Syntax Tree) `ClassDef` node representing the
        class definition
        - `engine`: a `DocEngine` object used to generate the class
        documentation
        - `overwrite`: a boolean value indicating whether to overwrite an
        existing docstring or not
        If the class definition already has a docstring or the `overwrite`
        parameter is `True`, the function generates a new docstring using the
        `DocEngine` object and inserts it into the class definition using the
        `insert_docstring` function. The function does not return anything.
        """
        if ast.get_docstring(node) is None or overwrite:
            doc = engine.generate_class_doc(ast.unparse(node), lang='Python')
            insert_docstring(node, doc)

def offset_lines(doc: str, level: int) -> str:
    """This function takes in a string `doc` and an integer `level` as input
    and returns a modified string with each line of the input string
    indented by `level` spaces, except for the first and last lines. The
    `doc` parameter is a string containing the document to be indented,
    while the `level` parameter is an integer representing the number of
    spaces to indent each line. The function returns a modified string with
    each line of the input string indented by `level` spaces, except for the
    first and last lines. The return type is a string.
    """
    lines = doc.splitlines()
    return lines[0] + ''.join([os.linesep + ' ' * level + line if line else '' for line in lines[1:]]) + os.linesep + ' ' * level

def insert_docstring(node: any, doc: str) -> None:
    """Function: insert_docstring
    Parameters:
    - node: any - The AST node to which the docstring needs to be added.
    - doc: str - The docstring to be added.
    Return Type: None
    Description:
    This function adds a docstring to the given AST node. The node can be of
    type ast.AsyncFunctionDef, ast.FunctionDef, ast.ClassDef, or ast.Module.
    If the node is not of any of these types, the function returns without
    doing anything. If the node already has a docstring, the function
    replaces it with the new docstring. If the node does not have a
    docstring, the function adds the new docstring as the first statement in
    the node's body. The function also adjusts the indentation of the
    docstring to match the indentation of the node's body.
    """
    if not isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef, ast.ClassDef, ast.Module)):
        return
    if not (node.body and isinstance(node.body[0], ast.Expr)):
        offset = node.body[0].col_offset
        node.body.insert(0, ast.Expr(value=ast.Constant(offset_lines(doc, offset)), col_offset=offset, end_col_offset=offset))
        return
    node_head = node.body[0].value
    if isinstance(node_head, ast.Str):
        node_head.s = offset_lines(doc, node_head.col_offset)
        return
    elif isinstance(node_head, ast.Constant) and isinstance(node_head.value, str):
        node_head.value = offset_lines(doc, node_head.col_offset)
        return