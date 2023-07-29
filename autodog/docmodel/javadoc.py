from autodog.utils.string import multiline
from autodog.docmodel.base import DocModel

class Javadoc(DocModel):
    def __init__(self, **kwarg):
        pass

    def function_format(self) -> str:
        return multiline(
            "Write a one-line abstract of the function here.",
            "",
            "A description of the function is written here.",
            "",
            " @param [argument name] <[argument type]> description",
            " (If the function doesn't have an argument, this item should not be written.)",
            " ...",
            " @return description",
            " (If the function doesn't have a return variable, this item should not be written.)",
            " ...",
            " @throws [exception name] description",
            " (If the function doesn't throw an exception, this item should not be written.)",
            " ..."
        )

    def class_format(self) -> str:
        return multiline(
            "Write a one-line abstract of the class here.",
            "",
            "A description of the class is written here.",
            "",
            " @param [argument name] <[argument type]> description",
            " (If the function doesn't have an argument, this item should not be written.)",
            " ...",
        )

    def module_format(self) -> str:
        return multiline(
            "Write a one-line abstract of the module here.",
            "",
            "A description of the module is written here.",
        )