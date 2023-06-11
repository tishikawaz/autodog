from .docengine import DocEngine

from functools import singledispatchmethod
import ast
import os

class PyCode:
    def __init__(self, filepath:str):
        self.filepath = filepath
        with open(filepath, 'r') as f:
            self.tree = ast.parse(f.read())

    def to_str(self) -> str:
        return ast.unparse(self.tree)

    @singledispatchmethod
    def write(self, filepath) -> None:
        with open(filepath, 'w') as f:
            f.write(self.to_str())

    @write.register
    def _(self) -> None:
        with open(self.filepath, 'w') as f:
            f.write(self.to_str())

    def insert_docs(self, engine:any, overwrite=False) -> None:
        for node in ast.walk(self.tree):
            self._insert_docs(node, engine, overwrite)

    @singledispatchmethod
    def _insert_docs(self, node:any, engine:DocEngine, overwrite:bool) -> None:
        pass

    @_insert_docs.register
    def _(self, node:ast.Module, engine:DocEngine, overwrite:bool) -> None:
        if(ast.get_docstring(node) is not None or overwrite):
            doc = engine.generate_module_doc(ast.unparse(node), lang='Python')
            insert_docstring(node, doc)

    @_insert_docs.register
    def _(self, node:ast.FunctionDef, engine:DocEngine, overwrite:bool) -> None:
        if(ast.get_docstring(node) is not None or overwrite):
            doc = engine.generate_func_doc(ast.unparse(node), lang='Python')
            insert_docstring(node, doc)

    @_insert_docs.register
    def _(self, node:ast.AsyncFunctionDef, engine:DocEngine, overwrite:bool) -> None:
        if(ast.get_docstring(node) is not None or overwrite):
            doc = engine.generate_func_doc(ast.unparse(node), lang='Python')
            insert_docstring(node, doc)

    @_insert_docs.register
    def _(self, node:ast.ClassDef, engine:DocEngine, overwrite:bool) -> None:
        if(ast.get_docstring(node) is not None or overwrite):
            doc = engine.generate_class_doc(ast.unparse(node), lang='Python')
            insert_docstring(node, doc)

def offset_lines(doc:str, level:int) -> str:
    lines = doc.splitlines()
    return lines[0] + ''.join([os.linesep + (' '*level) + line for line in lines[1:]]) + os.linesep + (' '*level)

def insert_docstring(node:any, doc:str) -> None:
    if not isinstance(node, (ast.AsyncFunctionDef, ast.FunctionDef, ast.ClassDef, ast.Module)):
        return
    if not(node.body and isinstance(node.body[0], ast.Expr)):
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