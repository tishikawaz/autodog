import os
import re
from copy import copy

class EndStatementNotFound(Exception):
    pass

class UndefinedFortranNodeName(Exception):
    pass

class BaseNode:
    def __init__(self, code:str):
        self.children = _make_nodes(code)

    def to_str(self) -> str:
        return _reconstruct_code_block([child.to_str() for child in self.children])

class BodyNode(BaseNode):
    def __init__(self, code:str):
        self.children = []
        self.code = code

    def to_str(self) -> str:
        return self.code

class StatementNode(BaseNode):
    def __init__(self, code:str):
        lines = code.splitlines()

        end_of_statement = 0
        for i, line in enumerate(lines):
            if not _is_continue_line(line):
                end_of_statement = i
                self.statement = _reconstruct_code_block(lines[0:end_of_statement+1])
                break

        doc_lines = []
        if _has_doc_block(lines, end_of_statement):
            for line in lines[end_of_statement+1:-1]:
                if line == '':
                    break
                if line.lstrip()[0] != '!':
                    break
                doc_lines += [line]
        self.doc = _reconstruct_code_block(doc_lines)
        num_doc_lines = len(doc_lines)

        self.end_statement = lines[-1]

        body_lines = lines[end_of_statement+num_doc_lines+1:-1]
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
        code = self.statement + os.linesep
        if self.doc:
            code += self.doc
        code += _reconstruct_code_block([child.to_str() for child in self.children]) + os.linesep
        code += self.end_statement
        return code

    def write_doc(self, doc:str) -> None:
        doc_lines = doc.splitlines()
        self.doc += ''.join([' '*self.indent_level + '! ' + doc + os.linesep for doc in doc_lines])

class ProgramNode(StatementNode):
    def __init__(self, code:str):
        super().__init__(code)

class FunctionNode(StatementNode):
    def __init__(self, code:str):
        super().__init__(code)

class SubroutineNode(StatementNode):
    def __init__(self, code:str):
        super().__init__(code)

class TypeNode(StatementNode):
    def __init__(self, code:str):
        super().__init__(code)

class ModuleNode(StatementNode):
    def __init__(self, code:str):
        super().__init__(code)

def _remove_comment(line:str) -> str:
    return line.split('!')[0]

def _is_continue_line(line) -> bool:
    segments = _remove_comment(line).split()
    return '&' in segments[-1][-1] # final segment, final position

def _has_doc_block(lines:list, end_of_statement:int) -> bool:
    if lines[end_of_statement+1]:
        return lines[end_of_statement+1].lstrip()[0] == '!'

def _search_end_statement(lines:list, statement:str, start_num:int) -> int:
    for line_num, line in enumerate(lines[start_num:]):
        if _match_whole(line.lower(), 'end ' + statement.lower()):
            return start_num+line_num
    raise EndStatementNotFound()

def _reconstruct_code_block(lines:list, start_num=0, end_num=-1) -> str:
    if not lines:
        return ''
    return ''.join([line + os.linesep for line in lines[start_num:end_num]]) + lines[end_num]

def _make_blocks(lines:list, statement:str, line_num:int) -> list:
    end_num      = _search_end_statement  (lines, statement, line_num)
    before_block = []
    if line_num > 0:
        before_block = lines[:line_num]
    block        = lines[line_num:end_num+1]
    after_block  = []
    if end_num < len(lines):
        after_block = lines[end_num+1:]
    return before_block, block, after_block

def _match_whole(word:str, find:str) -> bool:
    regex = re.compile(r"\b{0}\b".format(find))
    return len(regex.findall(word)) != 0

def _make_nodes(code:str) -> list:
    lines = code.splitlines()
    for line_num, line in enumerate(lines):
        if _match_whole(line.lower(), 'program'):
            before_block, block, after_block = _make_blocks(lines, 'program', line_num)
            nodes       = []
            if before_block:
                nodes  += [BaseNode   (_reconstruct_code_block(before_block))]
            nodes      += [ProgramNode(_reconstruct_code_block(block))]
            if after_block:
                nodes  += _make_nodes (_reconstruct_code_block(after_block))
            return nodes
        elif _match_whole(line.lower(), 'module'):
            before_block, block, after_block = _make_blocks(lines, 'module', line_num)
            nodes       = []
            if before_block:
                nodes  += [BaseNode  (_reconstruct_code_block(before_block))]
            nodes      += [ModuleNode(_reconstruct_code_block(block))]
            if after_block:
                nodes  += _make_nodes(_reconstruct_code_block(after_block))
            return nodes
        elif _match_whole(line.lower(), 'function'):
            before_block, block, after_block = _make_blocks(lines, 'function', line_num)
            nodes       = []
            if before_block:
                nodes  += [BaseNode    (_reconstruct_code_block(before_block))]
            nodes      += [FunctionNode(_reconstruct_code_block(block))]
            if after_block:
                nodes  += _make_nodes (_reconstruct_code_block(after_block))
            return nodes
        elif _match_whole(line.lower(), 'subroutine'):
            before_block, block, after_block = _make_blocks(lines, 'subroutine', line_num)
            nodes       = []
            if before_block:
                nodes  += [BaseNode      (_reconstruct_code_block(before_block))]
            nodes      += [SubroutineNode(_reconstruct_code_block(block))]
            if after_block:
                nodes  += _make_nodes    (_reconstruct_code_block(after_block))
            return nodes
        elif _match_whole(line.lower(), 'type'):
            before_block, block, after_block = _make_blocks(lines, 'type', line_num)
            nodes       = []
            if before_block:
                nodes  += [BaseNode  (_reconstruct_code_block(before_block))]
            nodes      += [TypeNode  (_reconstruct_code_block(block))]
            if after_block:
                nodes  += _make_nodes(_reconstruct_code_block(after_block))
            return nodes
    return [BodyNode(code)]

class FortranAST:
    def __init__(self, code:str):
        self.tree = BaseNode(code)

    def to_str(self):
        return self.tree.to_str()

    def walk(self) -> list:
        return self._walk(self.tree)

    def _walk(self, node:StatementNode) -> list:
        if not node.children:
            return [node]

        nodes = []
        for child in node.children:
            nodes += [child]
            nodes += self._walk(child)
        return nodes

