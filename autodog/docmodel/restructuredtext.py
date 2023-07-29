from autodog.utils.string import multiline
from autodog.docmodel.base import DocModel

class ReStructuredText(DocModel):
    def __init__(self, **kwarg):
        pass

    def function_format(self) -> str:
        return multiline(
            "Write a one-line abstract of the function here.",
            "",
            "A description of the function is written here.",
            "",
            ":param [argument name] [argument type] [argument number]: description",
            "(If the function doesn't have an argument, this item should not be written.)",
            "...",
            ":returns: description",
            "(If the function doesn't have an return variables, this item should not be written.)",
            ":rtype: type of return variable",
            "(If the function doesn't have an return variables, this item should not be written.)",
            ":raises [exception name]: description"
            "(If the function doesn't throw exception, this item should not be written.)",
            "...",
        )

    def class_format(self) -> str:
        return multiline(
            "Write a one-line abstract of the class here.",
            "",
            "A description of the class is written here.",
            ""
        )

    def module_format(self) -> str:
        return multiline(
            "Write a one-line abstract of the module here.",
            "",
            "A description of the module is written here.",
            ""
        )