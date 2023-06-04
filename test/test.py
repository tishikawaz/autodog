from autodog.fortrancode import FortranCode
from autodog.dummyengine import DummyEngine

code = FortranCode('test.f90')
engine = DummyEngine()

code.insert_docs(engine)

print(code.to_str())