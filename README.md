# AutoDog: An automatic documentation generator to document a specific segment of code

AutoDog uses ChatGPT to generate documentation for specific segments of code automatically.
It is currently developed for Fortran code. Additional functionality for Python will be added in the future.

## Usage

```python:usage_fortran.py
import autodog

code = autodog.code('your_code.f90')
engine = autodog.engine(api_key='YOUR-API-KEY')

# insert code documentations to a function, subroutine, type definition, ...
code.insert_docs(engine)

# overwrite your_code.f90
code.write()
```