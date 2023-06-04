from .docengine import DocEngine

class GPT3Engine(DocEngine):
    def __init__(self, notes=[], doc_type='docstring', *args, **kwargs):
        self.notes = notes
        self.doc_type = doc_type

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