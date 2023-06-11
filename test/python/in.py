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

    @singledispatchmethod
    def write(self, filepath) -> None:
        with open(filepath, 'w') as f:
            f.write(self.to_str())

    @write.register
    def write(self) -> None:
        with open(self.filepath, 'w') as f:
            f.write(self.to_str())
