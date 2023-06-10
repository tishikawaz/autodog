from ..docengine import DocEngine

class DummyEngine(DocEngine):
    def __init__(self, dummy_doc = 'This is a dummy document.'):
        self.dummy_doc = dummy_doc

    def generate_code_doc(self, code, lang='') -> str:
        return self.dummy_doc

    def generate_module_doc(self, code, lang='') -> str:
        return self.dummy_doc

    def generate_class_doc(self, code, lang='') -> str:
        return self.dummy_doc

    def generate_func_doc(self, code, lang='') -> str:
        return self.dummy_doc