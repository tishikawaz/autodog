"""This module provides a Fortran Abstract Syntax Tree (AST) class and
related node classes to parse and manipulate Fortran code.
Classes:
- EndStatementNotFound: Exception raised when the end statement of a
block cannot be found.
- UndefinedFortranNodeName: Exception raised when an undefined Fortran
node name is encountered.
- BaseNode: Base class for all AST nodes.
- BodyNode: AST node representing a code block without a statement.
- StatementNode: AST node representing a code block with a statement.
- ProgramNode: AST node representing a Fortran program.
- FunctionNode: AST node representing a Fortran function.
- SubroutineNode: AST node representing a Fortran subroutine.
- TypeNode: AST node representing a Fortran type definition.
- ModuleNode: AST node representing a Fortran module.
- FortranAST: Class for creating and manipulating a Fortran AST.
Functions:
- _remove_comment: Removes comments from a line of Fortran code.
- _is_continue_line: Determines if a line of Fortran code is a
continuation line.
- _has_doc_block: Determines if a code block has a documentation block.
- _search_end_statement: Searches for the end statement of a code block.
- _reconstruct_code_block: Reconstructs a code block from a list of
lines.
- _make_blocks: Splits a list of lines into three blocks: before,
current, and after.
- _match_whole: Determines if a word matches a whole string.
- _make_nodes: Recursively creates AST nodes from a block of Fortran
code.
"""
import os
import re

class EndStatementNotFound(Exception):
    """The `EndStatementNotFound` class is an exception that can be raised when
    an expected end statement is not found in the code. This can be useful
    for handling errors in situations where the code is expected to have a
    specific structure or syntax.
    """
    pass

class UndefinedFortranNodeName(Exception):
    """The `UndefinedFortranNodeName` class is an exception that can be raised
    when a Fortran node name is undefined. This class does not have any
    additional functionality beyond the base `Exception` class.
    """
    pass

class BaseNode:
    """A class representing a base node in a code block.
    Attributes:
        children (list): A list of child nodes.
    Methods:
        __init__(code: str): Initializes the BaseNode object with the given
        code string and creates child nodes.
        to_str() -> str: Returns the reconstructed code block as a string by
        calling the to_str() method on each child node.
    """

    def __init__(self, code: str):
        """Initializes an object of a class with a given code string. The code
        string is used to create child nodes using the _make_nodes() function.
        The child nodes are stored in the 'children' attribute of the object.
        Args:
            code (str): A string representing the code to be parsed.
        Returns:
            None
        """
        self.children = _make_nodes(code)

    def to_str(self) -> str:
        """Converts the children of a code block object to a string representation.
        Args:
            self: A code block object.
        Returns:
            A string representation of the children of the code block object.
        """
        return _reconstruct_code_block([child.to_str() for child in self.children])

class BodyNode(BaseNode):
    """A class representing a body node in a tree structure.
    Attributes:
        children (list): A list of child nodes.
        code (str): The code associated with the node.
    Methods:
        to_str(): Returns the code associated with the node as a string.
    """

    def __init__(self, code: str):
        """Initialize a new instance of a class with the given code.
        Args:
            code (str): The code to be assigned to the instance.
        Attributes:
            children (list): An empty list to store the children of the
            instance.
            code (str): The code assigned to the instance.
        Returns:
            None
        """
        self.children = []
        self.code = code

    def to_str(self) -> str:
        """Converts the code attribute of the object to a string and returns it.
        Returns:
            A string representation of the code attribute of the object.
        """
        return self.code

class StatementNode(BaseNode):
    """The `StatementNode` class represents a node in an abstract syntax tree
    for a statement in Python code. It takes a string of code as input and
    extracts the statement, documentation, and body of the statement. The
    `to_str` method returns the reconstructed code for the statement,
    including its documentation and body. The `write_doc` method takes a
    string of documentation and writes it to the node's `doc` attribute,
    properly indented and formatted.
    """

    def __init__(self, code: str):
        """The `__init__` method initializes an instance of a class with a given
        `code` string. It splits the code into lines and determines the end of
        the statement by checking if the line is a continuation line. It then
        reconstructs the code block up to the end of the statement and assigns
        it to the `statement` attribute.
        If there is a doc block present in the code, it extracts the lines
        starting with `!` and assigns them to the `doc` attribute. The number of
        lines in the doc block is also stored in `num_doc_lines`.
        The method then determines the end of the statement by assigning the
        last line of the code to the `end_statement` attribute. It extracts the
        body of the code by skipping the doc block and the statement and assigns
        it to the `body_lines` variable.
        The method then determines the indentation level of the body by counting
        the number of spaces at the beginning of the first non-empty line. This
        value is assigned to the `indent_level` attribute.
        Finally, the method calls the `__init__` method of the superclass with
        the reconstructed body of the code block.
        """
        lines = code.splitlines()
        end_of_statement = 0
        for (i, line) in enumerate(lines):
            if not _is_continue_line(line):
                end_of_statement = i
                self.statement = _reconstruct_code_block(lines[0:end_of_statement + 1])
                break
        doc_lines = []
        if _has_doc_block(lines, end_of_statement):
            for line in lines[end_of_statement + 1:-1]:
                if line == '':
                    break
                if line.lstrip()[0] != '!':
                    break
                doc_lines += [line]
        self.doc = _reconstruct_code_block(doc_lines)
        num_doc_lines = len(doc_lines)
        self.end_statement = lines[-1]
        body_lines = lines[end_of_statement + num_doc_lines + 1:-1]
        indent_level = 0
        for line in body_lines:
            if line == '':
                continue
            for c in line:
                if c != ' ':
                    break
                indent_level += 1
            break
        self.indent_level = indent_level
        super().__init__(_reconstruct_code_block(body_lines))

    def to_str(self) -> str:
        """Converts the current node and its children to a string representation.
        Returns:
            A string representation of the current node and its children.
        Raises:
            None.
        Args:
            self: The current node.
        """
        code = self.statement + os.linesep
        if self.doc:
            code += self.doc
        code += _reconstruct_code_block([child.to_str() for child in self.children]) + os.linesep
        code += self.end_statement
        return code

    def write_doc(self, doc: str) -> None:
        """Write the given documentation string to the object's `doc` attribute
        with an added exclamation mark and indentation level.
        :param doc: The documentation string to be written.
        :type doc: str
        :return: None
        """
        doc_lines = doc.splitlines()
        self.doc = ''.join([' ' * self.indent_level + '! ' + doc + os.linesep for doc in doc_lines])

class ProgramNode(StatementNode):
    """The `ProgramNode` class is a subclass of `StatementNode` that represents
    a node in an abstract syntax tree (AST) for a program. It takes a string
    `code` as input and initializes the `StatementNode` superclass with it
    using the `super()` function. The `code` parameter represents the code
    that this node represents in the AST.
    """

    def __init__(self, code: str):
        super().__init__(code)

class FunctionNode(StatementNode):
    """A class representing a function node in an abstract syntax tree.
    Attributes:
        code (str): The code representing the function.
    Methods:
        __init__(self, code: str): Initializes a FunctionNode object with
        the given code.
    Inherits from:
        StatementNode: A class representing a statement node in an abstract
        syntax tree.
    """

    def __init__(self, code: str):
        super().__init__(code)

class SubroutineNode(StatementNode):
    """The SubroutineNode class is a subclass of StatementNode that represents
    a subroutine in a program. It takes a string parameter 'code' which
    contains the code for the subroutine. The constructor initializes the
    object by calling the constructor of the superclass StatementNode with
    the 'code' parameter.
    """

    def __init__(self, code: str):
        super().__init__(code)

class TypeNode(StatementNode):
    """A class representing a type node in an abstract syntax tree.
    Attributes:
        code (str): The code representing the type node.
    Methods:
        __init__(self, code: str): Initializes a TypeNode object with the
        given code.
    """

    def __init__(self, code: str):
        super().__init__(code)

class ModuleNode(StatementNode):
    """The `ModuleNode` class is a subclass of `StatementNode` that represents
    a module in Python. It takes a `code` parameter, which is a string
    representing the code of the module. The `__init__` method initializes
    the `code` parameter using the `super()` method to call the `__init__`
    method of the `StatementNode` class.
    """

    def __init__(self, code: str):
        super().__init__(code)

def _remove_comment(line: str) -> str:
    """Removes comments from a given string.
    Args:
        line (str): A string containing a comment.
    Returns:
        str: The input string with the comment removed.
    Example:
        >>> _remove_comment('Hello world! This is a comment.')
        'Hello world'
    """
    return line.split('!')[0]

def _is_continue_line(line: str) -> bool:
    """Checks if a given line of code is a continuation line.
    Args:
        line (str): A line of code to be checked.
    Returns:
        bool: True if the line is a continuation line, False otherwise.
    """
    segments = _remove_comment(line).split()
    return '&' in segments[-1][-1]

def _has_doc_block(lines: list, end_of_statement: int) -> bool:
    """Check if the line after the end of a statement contains a doc block.
    Args:
        lines (list): A list of strings representing the lines of code.
        end_of_statement (int): The index of the last line of the statement.
    Returns:
        bool: True if the line after the end of the statement contains a doc
        block, False otherwise.
    """
    if lines[end_of_statement + 1]:
        return lines[end_of_statement + 1].lstrip()[0] == '!'

def _search_end_statement(lines: list, statement: str, start_num: int) -> int:
    """The `_search_end_statement` function takes in a list of `lines`, a
    `statement` string, and a `start_num` integer. It searches for the line
    number of the end statement of the given `statement` starting from the
    `start_num` line number in the `lines` list. If found, it returns the
    line number of the end statement. If not found, it raises an
    `EndStatementNotFound` exception. The function returns an integer
    representing the line number of the end statement.
    """
    for (line_num, line) in enumerate(lines[start_num:]):
        if _match_whole(line.lower(), 'end ' + statement.lower()):
            return start_num + line_num
    raise EndStatementNotFound()

def _reconstruct_code_block(lines: list, start_num=0, end_num=-1) -> str:
    """Reconstructs a code block from a list of lines.
    Args:
        lines (list): A list of strings representing the lines of code.
        start_num (int, optional): The starting line number to include in
        the reconstructed code block. Defaults to 0.
        end_num (int, optional): The ending line number to include in the
        reconstructed code block. Defaults to -1.
    Returns:
        str: A string representing the reconstructed code block.
    Raises:
        None.
    """
    if not lines:
        return ''
    return ''.join([line + os.linesep for line in lines[start_num:end_num]]) + lines[end_num]

def _make_blocks(lines: list, statement: str, line_num: int) -> list:
    """
    This function takes in a list of lines, a statement, and a line number
    as input and returns a tuple of three lists. The first list contains all
    the lines before the block of code starting from the given line number,
    the second list contains the block of code starting from the given line
    number and ending at the line number of the end statement, and the third
    list contains all the lines after the block of code ending at the line
    number of the end statement. The function uses the helper function
    _search_end_statement to find the line number of the end statement. The
    function returns an empty list if the end statement is not found.
    """
    end_num = _search_end_statement(lines, statement, line_num)
    before_block = []
    if line_num > 0:
        before_block = lines[:line_num]
    block = lines[line_num:end_num + 1]
    after_block = []
    if end_num < len(lines):
        after_block = lines[end_num + 1:]
    return (before_block, block, after_block)

def _match_whole(word: str, find: str) -> bool:
    """Checks if the given 'find' string is present as a whole word in the
    'word' string.
    Args:
        word (str): The string in which the 'find' string needs to be
        searched.
        find (str): The string to be searched in the 'word' string.
    Returns:
        bool: True if the 'find' string is present as a whole word in the
        'word' string, False otherwise.
    """
    regex = re.compile('\\b{0}\\b'.format(find))
    return len(regex.findall(word)) != 0

def _make_nodes(code: str) -> list:
    """This function `_make_nodes` takes a string of code as input and returns
    a list of nodes representing the different blocks of code in the input.
    It first splits the input code into lines and iterates over each line to
    identify the type of block (program, module, function, subroutine, or
    type) based on certain keywords. It then uses helper functions to
    extract the code block corresponding to each identified type and creates
    a node object for that block. The function recursively calls itself on
    any code blocks that appear after the identified block and appends the
    resulting nodes to the list. If no block type is identified, the
    function creates a single node representing the entire input code. The
    function returns the list of nodes.
    """
    lines = code.splitlines()
    for (line_num, line) in enumerate(lines):
        if _match_whole(line.lower(), 'program'):
            (before_block, block, after_block) = _make_blocks(lines, 'program', line_num)
            nodes = []
            if before_block:
                nodes += [BaseNode(_reconstruct_code_block(before_block))]
            nodes += [ProgramNode(_reconstruct_code_block(block))]
            if after_block:
                nodes += _make_nodes(_reconstruct_code_block(after_block))
            return nodes
        elif _match_whole(line.lower(), 'module'):
            (before_block, block, after_block) = _make_blocks(lines, 'module', line_num)
            nodes = []
            if before_block:
                nodes += [BaseNode(_reconstruct_code_block(before_block))]
            nodes += [ModuleNode(_reconstruct_code_block(block))]
            if after_block:
                nodes += _make_nodes(_reconstruct_code_block(after_block))
            return nodes
        elif _match_whole(line.lower(), 'function'):
            (before_block, block, after_block) = _make_blocks(lines, 'function', line_num)
            nodes = []
            if before_block:
                nodes += [BaseNode(_reconstruct_code_block(before_block))]
            nodes += [FunctionNode(_reconstruct_code_block(block))]
            if after_block:
                nodes += _make_nodes(_reconstruct_code_block(after_block))
            return nodes
        elif _match_whole(line.lower(), 'subroutine'):
            (before_block, block, after_block) = _make_blocks(lines, 'subroutine', line_num)
            nodes = []
            if before_block:
                nodes += [BaseNode(_reconstruct_code_block(before_block))]
            nodes += [SubroutineNode(_reconstruct_code_block(block))]
            if after_block:
                nodes += _make_nodes(_reconstruct_code_block(after_block))
            return nodes
        elif _is_type_statement(line):
            (before_block, block, after_block) = _make_blocks(lines, 'type', line_num)
            nodes = []
            if before_block:
                nodes += [BaseNode(_reconstruct_code_block(before_block))]
            nodes += [TypeNode(_reconstruct_code_block(block))]
            if after_block:
                nodes += _make_nodes(_reconstruct_code_block(after_block))
            return nodes
    return [BodyNode(code)]

def _is_type_statement(line:str) -> bool:
    declaration = re.split(r'[,]|[:]+', line)[0]
    return _match_whole(declaration.lower(), 'type') and (not '(' in declaration)

class FortranAST:
    """class FortranAST:
        A class to represent a Fortran Abstract Syntax Tree.
        Attributes:
        -----------
        code : str
            The Fortran code to be parsed and represented as an AST.
        tree : BaseNode
            The root node of the AST.
        Methods:
        --------
        to_str() -> str:
            Returns the string representation of the AST.
        walk() -> list:
            Returns a list of all the nodes in the AST.
        _walk(node: StatementNode) -> list:
            A recursive helper function to traverse the AST and return a
            list of all the nodes.
    """

    def __init__(self, code: str):
        """Initializes an instance of the class with a given code string. The code
        string is used to create a BaseNode object which is assigned to the
        'tree' attribute of the instance.
        :param code: A string representing the code to be used to create the
        BaseNode object.
        """
        self.tree = BaseNode(code)

    def to_str(self):
        """Return a string representation of the tree.
        Returns:
            A string representation of the tree.
        """
        return self.tree.to_str()

    def walk(self) -> list:
        """The `walk` method returns a list of all the nodes in the tree, starting
        from the root node and traversing the tree in a depth-first manner. The
        method takes no arguments and returns a list of nodes. The return type
        of the method is a list.
        """
        return self._walk(self.tree)

    def _walk(self, node: StatementNode) -> list:
        """Recursively walks through the children of a given StatementNode and
        returns a list of all the nodes.
        Args:
            node (StatementNode): The root node to start the traversal from.
        Returns:
            list: A list of all the nodes in the tree rooted at the given node.
        """
        if not node.children:
            return [node]
        nodes = []
        for child in node.children:
            nodes += [child]
            nodes += self._walk(child)
        return nodes