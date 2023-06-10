from .ast.fortran import (
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
        self.filepath = filepath
        with open(filepath, 'r') as f:
            self.tree = FortranAST(f.read())

    def to_str(self) -> str:
        return self.tree.to_str()

    def insert_docs(self, engine:any, overwrite=False) -> None:
        for node in self.tree.walk():
            self._insert_docs(node, engine, overwrite)

    def write(self, filepath='') -> None:
        if filepath == '':
            return self._write_to_original()
        with open(filepath, 'w') as f:
            f.write(self.to_str())

    def _write_to_original(self) -> None:
        with open(self.filepath, 'w') as f:
            f.write(self.to_str())
