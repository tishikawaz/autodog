# AutoDog: An automatic documentation generator to document a specific segment of code

Utilizes ChatGPT to generate documentation for specific segments of code automatically.
AutoDog is currently developed for Fortran code. Additional functionality for Python will be added in the future.

## Usage

```python:usage.py
from autodog.fortrancode import FortranCode
from autodog.gpt3engine import GPT3Engine

code = FortranCode('your_code.f90')
engine = GPT3Engine(api_key='YOUR-API-KEY')

code.insert_docs(engine)

print(code.to_str())

code.write() # overwrite your_code.f90
```