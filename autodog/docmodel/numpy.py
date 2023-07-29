from autodog.utils.string import multiline
from autodog.docmodel.base import DocModel

class NumpyStyleDocstring(DocModel):
    def __init__(self, **kwarg):
        pass

    def function_format(self) -> str:
        return multiline(
            "Write a one-line abstract of the function here.",
            "",
            "A description of the function is written here.",
            "",
            "Parameters",
            "----------",
            "argument name : argument type (If argument is set a default value, write the default value like 'id : int, default 0')",
            "    description",
            "    (If the function doesn't have an argument, this item should be marked as None.)",
            "...",
            "",
            "Returns",
            "-------",
            "return variable name : return variable type",
            "    description",
            "    (If the function doesn't have a return variable, this item should not be written.)",
            "...",
            "",
            "Raises",
            "------",
            "exception name",
            "    description",
            "    (If the function doesn't have throw an exception, this item should be marked as None.)",
            "...",
            "",
            "Yields",
            "------",
            "yield variable type",
            "    description",
            "    (If the function doesn't have yield variable, this item should not be written.)",
            "...",
            "",
            "See Also",
            "--------",
            "    An optional section used to refer to related code.",
            "",
            "Notes",
            "-----",
            "Notes such as additional information, limitations, references, and a discussion of the algorithm are listed here.",
            "(If this function doesn't have a note, this item should not be written.)",
            "",
            "Examples",
            "--------",
            "The usage of the function is described here."
        )

    def class_format(self) -> str:
        return multiline(
            "Write a one-line abstract of the class here.",
            "",
            "A description of the class is written here.",
            "",
            "Attributes",
            "----------"
            "attribute name : attribute type"
            "    description",
            "    (If the class doesn't have attribute, this item should be marked as None.)",
            "...",
            "",
            "Methods",
            "-------",
            "function name(arguments)",
            "    description",
            "    (If the class doesn't have attribute, this item should be marked as None.)",
            "..."
        )

    def module_format(self) -> str:
        return multiline(
            "Write a one-line abstract of the module here.",
            "",
            "A description of the module is written here."
        )