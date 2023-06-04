from autodocgen.fortrancode import FortranCode
from autodocgen.dummyengine import DummyEngine


code = FortranCode('test.f90')
engine = DummyEngine()

code.insert_docs(engine)

print(code.to_str())