from autodog.utils.string import multiline
from autodog.docmodel.base import DocModel

class Docstring(DocModel):
    def __init__(self, **kwarg):
        pass

    def function_format(self) -> str:
        return multiline(
            f"Write a one-line abstract of the function here.",
            f"",
            f"A description of the function, such as description of ",
            f"about arguments, returns, and exceptions, is written here."
        )

    def class_format(self) -> str:
        return multiline(
            f"Write a one-line abstract of the class here.",
            f"",
            f"A description of the class, such as description of ",
            f"class methods and exceptions, is written here."
        )

    def module_format(self) -> str:
        return multiline(
            f"Write a one-line abstract of the module here.",
            f"",
            f"A description of the module, such as description of ",
            f"public classes, functions, and global variables, is written here."
        )

    def application_format(self) -> str:
        return multiline(
            f"Write a one-line abstract of the application here.",
            f"",
            f"A description of the application, such as description of ",
            f"usage, I/O, and interfaces, is written here."
        )