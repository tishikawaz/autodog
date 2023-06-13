"""This is a Python class that generates documentation for code using
OpenAI's GPT-3 language model. The class takes in various parameters
such as notes, document type, API key, model, and line length. It has
four methods that generate documentation for code at different levels:
`generate_code_doc`, `generate_module_doc`, `generate_class_doc`, and
`generate_func_doc`. Each method takes in a code string and an optional
language parameter and returns a string containing the generated
documentation. The class also has several helper methods such as
`_make_question`, `_sleep_rate_limit`, and `_format`. The
`_indent_level` method is a private helper method that calculates the
indentation level of a given line.
"""
from ..docengine import DocEngine
import openai
import time
import textwrap
import os
import re

class ChatGPTEngine(DocEngine):
    """This is a Python class that generates documentation for code, modules,
    classes, and functions using OpenAI's GPT-3 language model. The class
    takes in various parameters such as notes, document type, API key,
    model, and line length. It has four methods that generate documentation
    for code, modules, classes, and functions respectively. The
    `_make_question` method creates a question for the GPT-3 model to
    generate the documentation. The `_sleep_rate_limit` method ensures that
    the rate limit for the OpenAI API is not exceeded. The `_format` method
    formats the generated documentation. The class uses a chat-based
    approach where the GPT-3 model is asked a question and it responds with
    the generated documentation.
    """

    def __init__(self, notes=[], doc_type='docstring', api_key='', model='gpt-3.5-turbo', line_length=72):
        """Initializes an instance of the class with the following parameters:
        - notes: A list of notes to be used for the instance. Default value is
        an empty list.
        - doc_type: A string representing the type of documentation to be
        generated. Default value is 'docstring'.
        - api_key: A string representing the OpenAI API key to be used for
        generating documentation. Default value is an empty string.
        - model: A string representing the OpenAI model to be used for
        generating documentation. Default value is 'gpt-3.5-turbo'.
        - line_length: An integer representing the maximum line length for the
        generated documentation. Default value is 72.
        - last_request_time: A float representing the time of the last API
        request made. Default value is 0.
        """
        self.notes = notes
        self.doc_type = doc_type
        openai.api_key = api_key
        self.model = model
        self.line_length = line_length
        self.last_request_time = 0

    def _make_question(self, code: str, lang='') -> str:
        """The `_make_question` function takes in a string `code` and an optional
        string `lang` as arguments and returns a formatted string that asks the
        user to suggest a document for the given code. The function also
        includes any notes that may have been added to the object calling the
        function.
        Parameters:
        - `self`: the object calling the function
        - `code`: a string representing the code for which the user needs to
        suggest a document
        - `lang`: an optional string representing the language of the code
        Returns:
        - A formatted string that asks the user to suggest a document for the
        given code, including any notes that may have been added to the object
        calling the function.
        """
        q = 'Please suggest a {0} for the following {1}code and write the document only.\n'.format(self.doc_type, lang + ' ')
        q += '```:code' + '\n'
        q += code + '\n'
        q += '```' + '\n'
        if self.notes:
            q += 'Notes:\n'
            for note in self.notes:
                q + '- {0}\n'.format(note)
        return q

    def _sleep_rate_limit(self) -> None:
        """The `_sleep_rate_limit` function is used to limit the rate of requests
        made to an API. It takes no arguments and returns nothing. The function
        first checks if the `last_request_time` attribute is set to 0, which
        indicates that no requests have been made yet. If this is the case, the
        function simply returns. Otherwise, the function calculates the time
        difference between the current time and the `last_request_time`
        attribute. It then sleeps for the maximum of 0 and 20 minus the time
        difference. This ensures that at least 20 seconds have passed since the
        last request was made before making another request. The function is
        intended to be used as a helper function within a larger API client
        class.
        """
        if self.last_request_time == 0:
            return
        t_diff = time.time() - self.last_request_time
        time.sleep(max([0, 20 - t_diff]))

    def _format(self, doc: str):
        """This function takes a string `doc` as input and formats it by removing
        any triple quotes or backticks and wrapping the text to fit within the
        specified `line_length`. The function returns the formatted string. If
        the input string is empty or contains only triple quotes or backticks,
        an empty string is returned. The `_indent_level` function is used to
        determine the indentation level of each line. The formatted string is
        separated by line breaks using the `os.linesep` method.
        """
        lines = doc.splitlines()
        if not lines:
            return ''
        return ''.join([textwrap.fill(re.sub('"""|```|' + "'''", '', line), self.line_length, subsequent_indent=' ' * _indent_level(line)) + os.linesep for line in lines if not any((s == line for s in ['```', '"""', "'''"]))])

    def generate_code_doc(self, code: str, lang='') -> str:
        """The `generate_code_doc` function takes in a string `code` and an
        optional string `lang` as input parameters and returns a string. It uses
        the private method `_make_question` to create a question based on the
        input `code` and `lang`. It then creates a list of messages containing a
        system message and the generated question. The function then waits for a
        certain amount of time to avoid rate limiting and sends the messages to
        the OpenAI chatbot using the `openai.ChatCompletion.create` method.
        Finally, it formats and returns the response received from the chatbot.
        """
        question = self._make_question(code, lang)
        messages = [{'role': 'system', 'content': 'You are an helpful programmer.'}, {'role': 'user', 'content': question}]
        self._sleep_rate_limit()
        response = openai.ChatCompletion.create(model=self.model, messages=messages, temperature=0.0)
        self.last_request_time = time.time()
        return self._format(response['choices'][0]['message']['content'])

    def generate_module_doc(self, code: str, lang='') -> str:
        """The `generate_module_doc` function takes in a string of code and an
        optional language parameter and returns a string. It uses the
        `_make_question` method to create a question based on the code and
        language provided, then sends that question to the OpenAI chatbot API
        along with a message indicating that the user is a helpful programmer.
        The function then waits for the API response, formats it, and returns
        it. This function is part of a larger class that interacts with the
        OpenAI chatbot API to generate documentation for code.
        """
        question = self._make_question(code, lang)
        messages = [{'role': 'system', 'content': 'You are an helpful programmer.'}, {'role': 'user', 'content': question}]
        self._sleep_rate_limit()
        response = openai.ChatCompletion.create(model=self.model, messages=messages, temperature=0.0)
        self.last_request_time = time.time()
        return self._format(response['choices'][0]['message']['content'])

    def generate_class_doc(self, code: str, lang='') -> str:
        """The `generate_class_doc` function takes in a string `code` and an
        optional string `lang` as input parameters and returns a string. It uses
        the private method `_make_question` to create a question based on the
        input `code` and `lang`. It then creates a list of messages containing a
        system message and the generated question. The function then waits for a
        certain amount of time to avoid rate limiting and sends the messages to
        the OpenAI chatbot using the `ChatCompletion` API. Finally, it formats
        and returns the response received from the chatbot.
        """
        question = self._make_question(code, lang)
        messages = [{'role': 'system', 'content': 'You are an helpful programmer.'}, {'role': 'user', 'content': question}]
        self._sleep_rate_limit()
        response = openai.ChatCompletion.create(model=self.model, messages=messages, temperature=0.0)
        self.last_request_time = time.time()
        return self._format(response['choices'][0]['message']['content'])

    def generate_func_doc(self, code: str, lang='') -> str:
        """The `generate_func_doc` function takes in a string `code` and an
        optional string `lang` as input parameters and returns a string. It uses
        the OpenAI API to generate a response to a question that is constructed
        using the `_make_question` method. The response is obtained by sending a
        message to the OpenAI chatbot using the `openai.ChatCompletion.create`
        method. The function also includes rate limiting to avoid exceeding the
        API usage limits. The response is then formatted using the `_format`
        method and returned.
        """
        question = self._make_question(code, lang)
        messages = [{'role': 'system', 'content': 'You are an helpful programmer.'}, {'role': 'user', 'content': question}]
        self._sleep_rate_limit()
        response = openai.ChatCompletion.create(model=self.model, messages=messages, temperature=0.0)
        self.last_request_time = time.time()
        return self._format(response['choices'][0]['message']['content'])

def _indent_level(line: str) -> int:
    """Returns the number of leading spaces in a given string.
        :param line: A string to check for leading spaces.
        :type line: str
        :return: The number of leading spaces in the given string.
        :rtype: int
        """
    n = 0
    for c in line:
        if c == ' ':
            n += 1
        else:
            break
    return n