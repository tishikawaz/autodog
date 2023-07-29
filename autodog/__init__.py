"""This module provides code and engine components for a chatbot
application.
The code components include FortranCode and PyCode, which are used for
implementing different code functionalities.
The engine components include ChatGPTEngine and DummyEngine, which are
used for providing chatbot engine functionalities.
The module exports the following components: code, engineFortranCode,
PyCode, ChatGPTEngine, DummyEngine.
"""
from autodog.app import (
    code,
    engine,
    doc_model
)
from autodog.code.python import PyCode
from autodog.code.fortran import FortranCode
from autodog.engine.chatgpt import ChatGPTEngine
from autodog.engine.dummy import DummyEngine
from autodog.docmodel.docstring import Docstring
from autodog.docmodel.google import GoogleStyleDocstring
from autodog.docmodel.javadoc import Javadoc
from autodog.docmodel.numpy import NumpyStyleDocstring
from autodog.docmodel.restructuredtext import ReStructuredText
from autodog.utils.progress import (
    progress_bar,
    progress_bar_nothing
)

__all__ = [
    "code",
    "engine",
    "doc_model",
    "PyCode",
    "FortranCode",
    "ChatGPTEngine",
    "DummyEngine",
    "Docstring",
    "GoogleStyleDocstring",
    "Javadoc",
    "NumpyStyleDocstring",
    "ReStructuredText",
    "progress_bar_nothing",
    "progress_bar",
]
