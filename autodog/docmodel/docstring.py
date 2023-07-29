from autodog.utils.string import multiline
from autodog.docmodel.base import DocModel

class Docstring(DocModel):
    def __init__(self, **kwarg):
        pass

    def function_format(self) -> str:
        return multiline(
            "one-line abstract",
            "",
            "description",
            ""
        )

    def class_format(self) -> str:
        return multiline(
            "one-line abstract",
            "",
            "description",
            ""
        )

    def module_format(self) -> str:
        return multiline(
            "one-line abstract",
            "",
            "description",
            ""
        )

    def application_format(self) -> str:
        return multiline(
            "one-line abstract",
            "",
            "description",
            ""
        )