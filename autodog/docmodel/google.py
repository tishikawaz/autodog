from autodog.utils.string import multiline
from autodog.docmodel.base import DocModel

class GoogleStyleDocstring(DocModel):
    def __init__(self, **kwarg):
        pass

    def function_format(self) -> str:
        return multiline(
            "Write a one-line abstract of the function here.",
            "",
            "A description of the function is written here.",
            "",
            "Args:",
            "    argument name (argument type): description",
            "    (If the function doesn't have an argument, this item should be marked as None.)",
            "    ...",
            "",
            "Returns:",
            "    return variable type : description",
            "    (If the function doesn't have a return variable, this item should not be written.)",
            "    ...",
            "",
            "Raises:",
            "    exception name : description",
            "    (If the function doesn't have throw an exception, this item should be marked as None.)",
            "    ...",
            "",
            "Yields:",
            "    yield variable type : description",
            "    (If the function doesn't have yield variable, this item should not be written.)",
            "    ...",
            "",
            "Examples:",
            "    The usage of the function is described here.",
            "",
            "Note:",
            "    Notes and limitations are listed here.",
            "    (If this function doesn't have a note, this item should not be written.)"
        )

    def class_format(self) -> str:
        return multiline(
            "Write a one-line abstract of the class here.",
            "",
            "A description of the class is written here.",
            "",
            "Attributes:",
            "    attribute name (attribute type): description",
            "    (If the class doesn't have attribute, this item should be marked as None.)",
            "    ...",
        )

    def module_format(self) -> str:
        return multiline(
            "Write a one-line abstract of the module here.",
            "",
            "A description of the module is written here.",
            "",
            "Todo:"
            "    * Todo is written here.",
            "    (If the module doesn't have todo, this item should not be written.)",
            "    ..."
        )