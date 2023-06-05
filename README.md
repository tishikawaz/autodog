# AutoDog: An automatic documentation generator to document a specific segment of code

AutoDog uses ChatGPT to generate documentation for specific segments of code automatically.
It is currently developed for Fortran code. Additional functionality for Python will be added in the future.

## Usage

```python:usage.py
from autodog.fortrancode import FortranCode
from autodog.chatgptengine import ChatGPTEngine

code = FortranCode('your_code.f90')
engine = ChatGPTEngine(api_key='YOUR-API-KEY')

code.insert_docs(engine)

code.write() # overwrite your_code.f90
```