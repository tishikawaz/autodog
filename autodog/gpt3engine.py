from .docengine import DocEngine
import openai

class GPT3Engine(DocEngine):
    def __init__(self, notes=[], doc_type='docstring', api_key='', engine="davinci", *args, **kwargs):
        self.notes = notes
        self.doc_type = doc_type
        self.engine = engine
        openai.api_key=api_key

    def _make_question(self, code:str, lang='') -> str:
        q = 'Please suggest a {0} for the following {1} code and write the {0} only.'.format(
            self.doc_type,
            lang
        )
        q += '"""'
        q += code
        q += '"""'
        q += 'Notes:'
        for note in self.notes:
            q + '- {0}'.format(note)
        return q

    def generate_code_doc(self, code) -> str:
        prompt = self._make_question(code)
        response = openai.Completion.create(engine      = self.engine,
                                            prompt      = prompt,
                                            max_tokens  = 100,
                                            temperature = 0.5,
                                            echo        = False)
        return response["choices"][0]['text']

    def generate_module_doc(self, code) -> str:
        prompt = self._make_question(code)
        response = openai.Completion.create(engine      = self.engine,
                                            prompt      = prompt,
                                            max_tokens  = 100,
                                            temperature = 0.5,
                                            echo        = False)
        return response["choices"][0]['text']

    def generate_class_doc(self, code) -> str:
        prompt = self._make_question(code)
        response = openai.Completion.create(engine      = self.engine,
                                            prompt      = prompt,
                                            max_tokens  = 100,
                                            temperature = 0.5,
                                            echo        = False)
        return response["choices"][0]['text']

    def generate_func_doc(self, code) -> str:
        prompt = self._make_question(code)
        response = openai.Completion.create(engine      = self.engine,
                                            prompt      = prompt,
                                            max_tokens  = 100,
                                            temperature = 0.5,
                                            echo        = False)
        return response["choices"][0]['text']