from ..docengine import DocEngine
import openai
import time
import textwrap
import os

class ChatGPTEngine(DocEngine):
    def __init__(self, notes=[], doc_type='docstring', api_key='', model='gpt-3.5-turbo', line_length = 72):
        self.notes       = notes
        self.doc_type    = doc_type
        openai.api_key   = api_key
        self.model       = model
        self.line_length = line_length
        self.last_request_time = 0

    def _make_question(self, code:str, lang='') -> str:
        q = 'Please suggest a {0} for the following {1}code and write the document only.\n'.format(
            self.doc_type,
            lang+' '
        )
        q += '```:code' + '\n'
        q += code       + '\n'
        q += '```'      + '\n'
        if self.notes:
            q += 'Notes:\n'
            for note in self.notes:
                q + '- {0}\n'.format(note)
        return q

    def _sleep_rate_limit(self) -> None:
        if self.last_request_time == 0:
            return
        t_diff = time.time() - self.last_request_time
        time.sleep(max([0, 20 - t_diff]))

    def _format(self, doc:str):
        lines = doc.splitlines()
        if not lines:
            return ''
        return ''.join([textwrap.fill(line, self.line_length, subsequent_indent=' '*_indent_level(line)) + os.linesep for line in lines if not any((s in line) for s in ['```', '"""', "'''"])])

    def generate_code_doc(self, code, lang='') -> str:
        question = self._make_question(code, lang)
        messages=[
            {'role': 'system', 'content': 'You are an helpful programmer.'},
            {'role': 'user', 'content': question}]
        self._sleep_rate_limit()
        response = openai.ChatCompletion.create(model       = self.model,
                                                messages    = messages,
                                                temperature = 0.0)
        self.last_request_time = time.time()
        return self._format(response['choices'][0]['message']['content'])

    def generate_module_doc(self, code, lang='') -> str:
        question = self._make_question(code, lang)
        messages=[
            {'role': 'system', 'content': 'You are an helpful programmer.'},
            {'role': 'user', 'content': question}]
        self._sleep_rate_limit()
        response = openai.ChatCompletion.create(model       = self.model,
                                                messages    = messages,
                                                temperature = 0.0)
        self.last_request_time = time.time()
        return self._format(response['choices'][0]['message']['content'])

    def generate_class_doc(self, code, lang='') -> str:
        question = self._make_question(code, lang)
        messages=[
            {'role': 'system', 'content': 'You are an helpful programmer.'},
            {'role': 'user', 'content': question}]
        self._sleep_rate_limit()
        response = openai.ChatCompletion.create(model       = self.model,
                                                messages    = messages,
                                                temperature = 0.0)
        self.last_request_time = time.time()
        return self._format(response['choices'][0]['message']['content'])

    def generate_func_doc(self, code, lang='') -> str:
        question = self._make_question(code, lang)
        messages=[
            {'role': 'system', 'content': 'You are an helpful programmer.'},
            {'role': 'user', 'content': question}]
        self._sleep_rate_limit()
        response = openai.ChatCompletion.create(model       = self.model,
                                                messages    = messages,
                                                temperature = 0.0)
        self.last_request_time = time.time()
        return self._format(response['choices'][0]['message']['content'])

def _indent_level(line:str) -> int:
        n=0
        for c in line:
            if c == ' ':
                n += 1
            else:
                break
        return n