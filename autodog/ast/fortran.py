"""This module provides classes for creating and manipulating an Abstract
Syntax Tree (AST) for Fortran code.
Classes:
- EndStatementNotFound: Exception raised when the end statement of a
block is not found.
- UndefinedFortranNodeName: Exception raised when a Fortran node name is
undefined.
- BaseNode: Base class for all nodes in the AST.
- BodyNode: Represents a body node in the AST.
- StatementNode: Represents a statement node in the AST.
- ProgramNode: Represents a program node in the AST.
- FunctionNode: Represents a function node in the AST.
- SubroutineNode: Represents a subroutine node in the AST.
- TypeNode: Represents a type node in the AST.
- ModuleNode: Represents a module node in the AST.
- FortranAST: Represents the AST for Fortran code.
Functions:
- _remove_comment: Removes comments from a line of code.
- _is_continue_line: Checks if a line of code is a continuation line.
- _has_doc_block: Checks if a block of code has a documentation block.
- _search_end_statement: Searches for the end statement of a block of
code.
- _reconstruct_code_block: Reconstructs a block of code from a list of
lines.
- _make_blocks: Splits a list of lines into three blocks based on a
statement.
- _match_whole: Checks if a word matches a whole string.
- _make_nodes: Creates nodes from a block of code.
- _is_type_statement: Checks if a line of code is a type statement.
"""
import os
import re

class EndStatementNotFound(Exception):
    """Custom exception class raised when an end statement is not found.
    This exception is raised when a specific end statement is expected but
    not found in the code. It can be used to handle cases where the code
    execution cannot proceed without a specific end statement.
    Attributes:
        None
    Methods:
        None
    """
    pass

class UndefinedFortranNodeName(Exception):
    """Exception raised when a Fortran node name is undefined.
    This exception is raised when attempting to access a Fortran node name
    that has not been defined.
    Attributes:
        None
    Methods:
        None
    """
    pass

class BaseNode:
    """Represents a base node in a code tree.
    Attributes:
        children (list): A list of child nodes.
    Initializes a new instance of the class.
    Parameters:
    - code (str): The code to be processed.
    Returns:
    - None
    Side Effects:
    - Initializes the 'children' attribute with the result of '_make_nodes'
    function.
    Converts the current object and its children to a string representation.
    Returns:
        str: The string representation of the current object and its
        children.
    """

    def __init__(self, code: str):
        """Initializes a new instance of the class.
        Parameters:
        - code (str): The code to be processed.
        Returns:
        - None
        Side Effects:
        - Initializes the 'children' attribute with the result of the
        '_make_nodes' function.
        """
        self.children = _make_nodes(code)

    def to_str(self) -> str:
        """Converts the current object and its children to a string representation.
        Returns:
            str: The string representation of the current object and its
            children.
        """
        return _reconstruct_code_block([child.to_str() for child in self.children])

class BodyNode(BaseNode):
    """Represents a body node in a tree structure.
    Attributes:
        children (list): A list of child nodes.
        code (str): The code associated with the node.
    Methods:
        to_str: Returns the code associated with the node as a string.
    """

    def __init__(self, code: str):
        """Initializes a new instance of the class.
        Parameters:
        - code (str): The code associated with the instance.
        Returns:
        - None
        """
        self.children = []
        self.code = code

    def to_str(self) -> str:
        """Converts the code attribute of the object to a string.
        Returns:
            str: The code attribute as a string.
        """
        return self.code

class StatementNode(BaseNode):
    """Represents a node in the abstract syntax tree that represents a
    statement.
    Args:
        code (str): The code representing the statement.
    Attributes:
        statement (str): The reconstructed code block of the statement.
        doc (str): The reconstructed code block of the documentation.
        end_statement (str): The last line of the statement.
        indent_level (int): The level of indentation of the statement.
    """

    def __init__(self, code: str):
        """Initializes an instance of the class.
        Parameters:
        - code (str): The code to be processed.
        Returns:
        - None
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
        """Converts the current object to a string representation.
        Returns:
            str: The string representation of the object.
        """
        code = self.statement + os.linesep
        if self.doc:
            code += self.doc
        code += _reconstruct_code_block([child.to_str() for child in self.children]) + os.linesep
        code += self.end_statement
        return code

    def write_doc(self, doc: str) -> None:
        """Writes the given documentation string to the object's 'doc' attribute.
        Parameters:
        - doc (str): The documentation string to be written.
        Returns:
        - None
        Example:
        write_doc('This is a sample documentation string.')
        """
        doc_lines = doc.splitlines()
        self.doc = ''.join([' ' * self.indent_level + '! ' + doc + os.linesep for doc in doc_lines])

class ProgramNode(StatementNode):
    """
    Initializes a new ProgramNode object.
    Args:
        code (str): The code associated with the program node.
    Returns:
        None
    """

    def __init__(self, code: str):
        super().__init__(code)

class FunctionNode(StatementNode):
    """Represents a node in an abstract syntax tree (AST) that represents a
    function.
    Args:
        code (str): The code representing the function.
    Attributes:
        code (str): The code representing the function.
    """

    def __init__(self, code: str):
        super().__init__(code)

class SubroutineNode(StatementNode):
    """
    Initializes a new instance of the SubroutineNode class.
    Args:
        code (str): The code representing the subroutine.
    """

    def __init__(self, code: str):
        super().__init__(code)

class TypeNode(StatementNode):
    """Represents a node in the abstract syntax tree (AST) that represents a
    type declaration statement.
    Args:
        code (str): The code representing the type declaration statement.
    Attributes:
        code (str): The code representing the type declaration statement.
    """

    def __init__(self, code: str):
        super().__init__(code)

class ModuleNode(StatementNode):
    """Represents a node in the abstract syntax tree (AST) that represents a
    module.
    Args:
        code (str): The code associated with the module.
    Attributes:
        code (str): The code associated with the module.
    """

    def __init__(self, code: str):
        super().__init__(code)

def _remove_comment(line: str) -> str:
    """Removes the comment from the given line.
    Parameters:
    line (str): The input line containing a comment.
    Returns:
    str: The line with the comment removed.
    """
    return line.split('!')[0]

def _is_continue_line(line: str) -> bool:
    """Checks if the given line is a continuation line.
    Args:
        line (str): The line to be checked.
    Returns:
        bool: True if the line is a continuation line, False otherwise.
    """
    segments = _remove_comment(line).split()
    return '&' in segments[-1][-1]

def _has_doc_block(lines: list, end_of_statement: int) -> bool:
    """
    Checks if there is a doc block after the given statement.
    Args:
        lines (list): The list of lines containing the code.
        end_of_statement (int): The index of the end of the statement.
    Returns:
        bool: True if there is a doc block after the statement, False
        otherwise.
    """
    if lines[end_of_statement + 1]:
        return lines[end_of_statement + 1].lstrip()[0] == '!'

def _search_end_statement(lines: list, statement: str, start_num: int) -> int:
    """
    Searches for the end statement of a given statement in a list of lines.
    Args:
        lines (list): A list of lines to search through.
        statement (str): The statement to find the end statement for.
        start_num (int): The line number to start searching from.
    Returns:
        int: The line number of the end statement.
    Raises:
        EndStatementNotFound: If the end statement is not found.
    """
    for (line_num, line) in enumerate(lines[start_num:]):
        if _match_whole(line.lower(), 'end ' + statement.lower()):
            return start_num + line_num
    raise EndStatementNotFound()

def _reconstruct_code_block(lines: list, start_num=0, end_num=-1) -> str:
    """Reconstructs a code block from a list of lines.
    Args:
        lines (list): A list of lines representing the code block.
        start_num (int, optional): The starting line number to include in
        the reconstruction. Defaults to 0.
        end_num (int, optional): The ending line number to include in the
        reconstruction. Defaults to -1.
    Returns:
        str: The reconstructed code block as a string.
    """
    if not lines:
        return ''
    return ''.join([line + os.linesep for line in lines[start_num:end_num]]) + lines[end_num]

def _make_blocks(lines: list, statement: str, line_num: int) -> list:
    """Splits the given list of lines into three blocks: before_block, block,
    and after_block.
    Args:
        lines (list): A list of lines.
        statement (str): The statement to search for.
        line_num (int): The line number to start the search from.
    Returns:
        tuple: A tuple containing three lists: before_block, block, and
        after_block.
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
    """
    Checks if the given word contains the specified string as a whole word.
    Args:
        word (str): The word to search within.
        find (str): The string to find as a whole word.
    Returns:
        bool: True if the word contains the specified string as a whole
        word, False otherwise.
    """
    regex = re.compile('\\b{0}\\b'.format(find))
    return len(regex.findall(word)) != 0

def _make_nodes(code: str) -> list:
    """Parses the given code and returns a list of nodes representing the
    program structure.
    Args:
        code (str): The code to be parsed.
    Returns:
        list: A list of nodes representing the program structure.
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

def _is_type_statement(line: str) -> bool:
    """Checks if a given line is a type statement.
    Args:
        line (str): The line to be checked.
    Returns:
        bool: True if the line is a type statement, False otherwise.
    """
    declaration = re.split('[,]|[:]+', line)[0]
    return _match_whole(declaration.lower(), 'type') and (not '(' in declaration)

class FortranAST:
    """
    Initializes a new instance of the FortranAST class.
    Args:
        code (str): The code to be used for creating the BaseNode.
    Returns:
        None
    Methods:
        - to_str(): Returns a string representation of the tree.
        - walk(): Returns a list of all the elements in the tree, obtained
        by performing a depth-first traversal.
        - _walk(node: StatementNode): Recursively walks through the tree of
        StatementNodes starting from the given node and returns a list of
        all nodes encountered.
    """

    def __init__(self, code: str):
        """Initializes a new instance of the class.
        Args:
            code (str): The code to be used for creating the BaseNode.
        Returns:
            None
        """
        self.tree = BaseNode(code)

    def to_str(self):
        """Returns a string representation of the tree.
        """
        return self.tree.to_str()

    def walk(self) -> list:
        """Returns a list of all the elements in the tree, obtained by performing a
        depth-first traversal.
        """
        return self._walk(self.tree)

    def _walk(self, node: StatementNode) -> list:
        """Recursively walks through the tree of StatementNodes starting from the
        given node and returns a list of all nodes encountered.
        Args:
            node (StatementNode): The starting node of the tree.
        Returns:
            list: A list of StatementNodes encountered during the traversal.
        """
        if not node.children:
            return [node]
        nodes = []
        for child in node.children:
            nodes += [child]
            nodes += self._walk(child)
        return nodes