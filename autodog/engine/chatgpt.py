"""This is a Python class that generates documentation for code using
OpenAI's GPT-3 language model. The class takes in various parameters
such as notes, document type, API key, model, and line length. It has
four methods that generate documentation for code at different levels:
`generate_code_doc`, `generate_module_doc`, `generate_class_doc`, and
`generate_func_doc`. Each method takes in a code string and an optional
language parameter and returns a string containing the generated
documentation. The class also has several helper methods such as
`_make_prompt`, `_sleep_rate_limit`, and `_format`. The `_indent_level`
method is a private helper method that calculates the indentation level
of a given line.
The class `ChatGPTEngine` initializes an instance with the following
parameters:
- `notes` (list, optional): A list of notes to be used for the instance.
Default value is an empty list.
- `doc_type` (str, optional): A string representing the type of
documentation to be generated. Default value is 'docstring'.
- `api_key` (str, optional): A string representing the OpenAI API key to
be used for generating documentation. Default value is an empty string.
- `model` (str, optional): A string representing the OpenAI model to be
used for generating documentation. Default value is 'gpt-3.5-turbo'.
- `line_length` (int, optional): An integer representing the maximum
line length for the generated documentation. Default value is 72.
The class has the following methods:
- `__init__(self, notes=[], doc_type='docstring', api_key='',
model='gpt-3.5-turbo-0613', line_length=72)`: Initializes an instance of
the class with the specified parameters.
- `_make_prompt(self, code: str, lang: str, statement_kind: str,
context='') -> str`: Creates a formatted prompt asking the user to
suggest a document for the given code.
- `_sleep_rate_limit(self) -> None`: Limits the rate of requests made to
an API.
- `generate_doc(self, code: str, lang: str, statement_kind: str,
context='') -> str`: Generates documentation for the given code using
the OpenAI chatbot.
- `_get_doc(response: str, lang: str, line_length: int) -> str`: Formats
the given documentation string based on the specified language and line
length.
- `_get_doc_python(line_length: int, response: str)`: Formats the given
Python docstring to fit within the specified line length.
- `_get_doc_fortran(line_length: int, response: str)`: Formats the given
Fortran documentation string by removing leading exclamation marks,
wrapping lines to the specified line length, and preserving the
indentation level.
- `_all_lines_are_not_comment(lines: list[str], comment='!') -> bool`:
Checks if all lines in the given list are not comments.
- `_first_indentation_level(lines: list[str]) -> int`: Returns the
indentation level of the first non-empty line in the given list of
lines.
- `_indent_level(line: str) -> int`: Returns the number of leading
spaces in a given string.
"""
import os
import re
import textwrap
import time
from typing import Optional

import openai

from autodog.engine.base import Engine
from autodog.utils.string import multiline

class ChatGPTEngine(Engine):
    """Initializes an instance of the class with the following parameters:
    Args:
        notes (list, optional): A list of notes to be used for the instance.
            Default value is an empty list.
        doc_type (str, optional): A string representing the type of
        documentation
            to be generated. Default value is 'docstring'.
        api_key (str, optional): A string representing the OpenAI API key to
        be
            used for generating documentation. Default value is an empty
            string.
        model (str, optional): A string representing the OpenAI model to be
        used
            for generating documentation. Default value is 'gpt-3.5-turbo'.
        line_length (int, optional): An integer representing the maximum
        line
            length for the generated documentation. Default value is 72.

    Returns
    -------
        None.
    """

    def __init__(
        self,
        model:str="gpt-3.5-turbo",
        line_length:int = 72,
        notes:list[str] = [],
        deployment_id:Optional[str] = None,
        api_key:str = openai.api_key,
        api_key_path:Optional[str] = openai.api_key_path,
        api_base:str = openai.api_base,
        api_version:str = openai.api_version,
        api_type:str = openai.api_type,
        http_proxy:Optional[str] = None,
        https_proxy:Optional[str] = None,
        rate_limit:float = 20.0
    ) -> None:
        """Initializes an instance of the class with the following parameters:
        Args:
            notes (list, optional): A list of notes to be used for the
            instance. Default value is an empty list.
            doc_type (str, optional): A string representing the type of
            documentation to be generated. Default value is 'docstring'.
            api_key (str, optional): A string representing the OpenAI API
            key to be used for generating documentation. Default value is an
            empty string.
            model (str, optional): A string representing the OpenAI model to
            be used for generating documentation. Default value is
            'gpt-3.5-turbo'.
            line_length (int, optional): An integer representing the maximum
            line length for the generated documentation. Default value is
            72.

        Returns
        -------
            None.
        """
        self.model = model
        self.deployment_id:Optional[str] = deployment_id

        self.notes = notes
        self.line_length = line_length
        self.rate_limit = rate_limit

        openai.api_key = api_key
        openai.api_key_path = api_key_path
        openai.api_base = api_base
        openai.api_version = api_version
        openai.api_type = api_type
        if http_proxy is not None:
            if isinstance(openai.proxy, dict):
                openai.proxy["http"] = http_proxy
        if https_proxy is not None:
            if isinstance(openai.proxy, dict):
                openai.proxy["https"] = https_proxy

        self.last_request_time:Optional[float] = None

    def _make_prompt(
        self, code:str, lang:str, statement_kind:str, doc_format:str, context:Optional[str]=None
    ) -> str:
        """The `_make_prompt` function takes in a string `code` and an optional
        string `lang` as arguments and returns a formatted string that asks the
        user to suggest a document for the given code. The function also
        includes any notes that may have been added to the object calling the
        function.

        Parameters
        ----------
        - `self`: the object calling the function
        - `code`: a string representing the code for which the user needs to
        suggest a document
        - `lang`: an optional string representing the language of the code
        Returns:
        - A formatted string that asks the user to suggest a document for the
        given code, including any notes that may have been added to the object
        calling the function.
        """
        return multiline(
            f"Suggest a documentation for the following {lang} {statement_kind}.",
            f"",
            f"Desired format:",
            f"{doc_format}",
            f"",
            f"{self._insert_context(statement_kind, context)}",
            f"{self._insert_notes()}",
            f"{statement_kind}```",
            f"{code}",
            f"```"
        )

    def _insert_context(self, statement_kind:str, context:Optional[str]=None):
        if context is None:
            return ""
        return multiline(
            f"This {statement_kind} is defined in the following context.",
            f"context```",
            f"{context}",
            f"```",
            f""
        )

    def _insert_notes(self):
        if not self.notes:
            return ""
        return multiline(
            "Notes:",
            "".join([
                f" - {note}" + os.linesep for note in self.notes
            ])
        )

    def _sleep_rate_limit(self) -> None:
        """Limits the rate of requests made to an API.
        This function takes no arguments and returns nothing. It first checks if
        the `last_request_time` attribute is set to 0, which indicates that no
        requests have been made yet. If this is the case, the function simply
        returns.
        Otherwise, the function calculates the time difference between the
        current time and the `last_request_time` attribute. It then sleeps for
        the maximum of 0 and 20 minus the time difference. This ensures that at
        least 20 seconds have passed since the last request was made before
        making another request.
        This function is intended to be used as a helper function within a
        larger API client class.
        """
        if self.last_request_time is None:
            return
        t_diff = time.time() - self.last_request_time
        time.sleep(max([0, self.rate_limit - t_diff]))

    def generate_doc(
        self, code:str, lang:str, statement_kind:str, doc_format:str, context:Optional[str]=None
    ) -> str:
        """The `generate_doc` function takes in a string `code`, a string `lang`, a
        string `statement_kind`, and an optional string `context` as input
        parameters and returns a string.
        It uses the private method `_make_prompt` to create a prompt based on
        the input `code`, `lang`, `statement_kind`, and `context`.
        The function then creates a list of messages containing a system message
        and the generated prompt.
        After waiting for a certain amount of time to avoid rate limiting, the
        function sends the messages to the OpenAI chatbot using the
        `openai.ChatCompletion.create` method.
        Finally, it formats and returns the response received from the chatbot.
        """
        prompt = [
            {
                "role": "system",
                "content": "You are an experienced programmer."
            },
            {
                "role": "user",
                "content": self._make_prompt(
                    code,
                    lang,
                    statement_kind,
                    doc_format,
                    context
                ),
            },
        ]

        self._sleep_rate_limit()
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=prompt,
            temperature=0.0,
            deployment_id=self.deployment_id
        )
        self.last_request_time = time.time()

        message = response["choices"][0]["message"]["content"]
        return _get_doc(message, lang, self.line_length)


def _get_doc(response: str, lang: str, line_length: int) -> str:
    """Formats the given documentation string based on the specified language
    and line length.

    Args:
    ----
        response (str): The documentation string to be formatted.
        lang (str): The language for which the documentation string should
        be formatted.
        line_length (int): The maximum length of each line in the formatted
        string.

    Returns:
    -------
        str: The formatted documentation string.

    Raises:
    ------
        KeyError: If the specified language is not supported.
    """
    if not response:
        return ""
    getter = {"python": _get_doc_python, "fortran": _get_doc_fortran}
    return getter[lang.lower()](line_length, response)


def _get_doc_python(line_length: int, response: str):
    """Formats the given Python docstring to fit within the specified line
    length.

    Args:
    ----
        line_length (int): The maximum length of each line.
        response (str): The response from chat gpt.

    Returns:
    -------
        str: The formatted docstring.
    """
    segments = response.split('"""')
    if len(segments) > 2:
        lines = segments[1].splitlines()
        level = _first_indentation_level(lines)
        return "".join(
            [
                textwrap.fill(
                    line[level:],
                    line_length,
                    subsequent_indent=" " * _indent_level(line[level:]),
                )
                + os.linesep
                for line in lines
            ],
        )
    lines = response.splitlines()
    return "".join(
        [
            textwrap.fill(
                line, line_length, subsequent_indent=" " * _indent_level(line),
            )
            + os.linesep
            for line in lines
            if not any(s == line for s in ["```", '"""', "'''"])
        ],
    )


def _get_doc_fortran(line_length: int, response: str):
    """Formats the given Fortran documentation string by removing leading
    exclamation marks, wrapping lines to the specified line length, and
    preserving the indentation level.

    Args:
    ----
        line_length (int): The maximum length of each line after wrapping.
        response (str): The response string from chatgpt.

    Returns:
    -------
        str: The formatted Fortran documentation string.
    """
    lines = response.splitlines()
    if _all_lines_are_not_comment(lines):
        comment_lines = [line for line in lines if line not in "```"]
        level = _first_indentation_level(comment_lines)
        return "".join(
            [
                textwrap.fill(
                    line[level:],
                    line_length,
                    subsequent_indent=" " * _indent_level(line[level:]),
                )
                + os.linesep
                for line in comment_lines
            ],
        )
    comment_lines = [line for line in lines if "!" in line]
    level = _first_indentation_level(comment_lines)
    return "".join(
        [
            textwrap.fill(
                re.sub("!", "", line[level:]).strip(),
                line_length,
                subsequent_indent=" " * _indent_level(line[level:]),
            )
            + os.linesep
            for line in comment_lines
        ],
    )


def _all_lines_are_not_comment(lines: list[str], comment="!") -> bool:
    """Checks if all lines in the given list are not comments.

    Args:
    ----
        lines (list[str]): The list of lines to check.
        comment (str, optional): The character(s) used to indicate a
        comment. Defaults to '!'.

    Returns:
    -------
        bool: True if all lines are not comments, False otherwise.
    """
    return all(comment not in line for line in lines)


def _first_indentation_level(lines: list[str]) -> int:
    """Returns the indentation level of the first non-empty line in the given
    list of lines.

    Args:
    ----
        lines (list[str]): A list of strings representing lines of code.

    Returns:
    -------
        int: The indentation level of the first non-empty line.
    """
    for line in lines:
        if line:
            return _indent_level(line)
    return None


def _indent_level(line: str) -> int:
    """Returns the number of leading spaces in a given string.
    :param line: A string to check for leading spaces.
    :type line: str
    :return: The number of leading spaces in the given string.
    :rtype: int.
    """
    n = 0
    for c in line:
        if c == " ":
            n += 1
        else:
            break
    return n
