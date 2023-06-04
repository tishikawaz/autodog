from .fortranast import (
    FortranAST,
    ModuleNode,
    TypeNode,
    FunctionNode,
    SubroutineNode,
    ProgramNode
)
from .docengine import DocEngine

from functools import singledispatchmethod

class FortranCode:
    def __init__(self, filepath:str):
        with open(filepath, 'r') as f:
            self.tree = FortranAST(f.read())

    def to_str(self) -> str:
        return self.tree.to_str()

    def insert_docs(self, engine:any, overwrite=False) -> None:
        for node in self.tree.walk():
            self._insert_docs(node, engine, overwrite)

    @singledispatchmethod
    def _insert_docs(self, node:any, engine:DocEngine, overwrite:bool) -> None:
        pass

    @_insert_docs.register
    def _(self, node:ModuleNode, engine:DocEngine, overwrite:bool) -> None:
        if(not node.doc or overwrite):
            node.write_doc(engine.generate_module_doc(node.to_str()))

    @_insert_docs.register
    def _(self, node:FunctionNode, engine:DocEngine, overwrite:bool) -> None:
        if(not node.doc or overwrite):
            node.write_doc(engine.generate_func_doc(node.to_str()))

    @_insert_docs.register
    def _(self, node:SubroutineNode, engine:DocEngine, overwrite:bool) -> None:
        if(not node.doc or overwrite):
            node.write_doc(engine.generate_func_doc(node.to_str()))

    @_insert_docs.register
    def _(self, node:TypeNode, engine:DocEngine, overwrite:bool) -> None:
        if(not node.doc or overwrite):
            node.write_doc(engine.generate_class_doc(node.to_str()))

    @_insert_docs.register
    def _(self, node:ProgramNode, engine:DocEngine, overwrite:bool) -> None:
        if(not node.doc or overwrite):
           node.write_doc(engine.generate_code_doc(node.to_str()))
