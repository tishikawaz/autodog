from .fortrancode import FortranCode

from .engine.chatgpt import ChatGPTEngine
from .engine.dummy import DummyEngine

import os
class UnknownEngineName(Exception):
    pass

class UnknownFileExtension(Exception):
    pass

def engine(name='chatgpt', **kwargs):
    if(name == 'chatgpt'):
        return ChatGPTEngine(**kwargs)
    elif(name == 'dummy'):
        return DummyEngine(**kwargs)

    raise UnknownEngineName

def code(filepath:str, **kwargs):
    extension = os.path.splitext(filepath)[1][1:]
    if any((s in extension.lower()) for s in ['f', 'f90']):
        return FortranCode(filepath)

    raise UnknownFileExtension