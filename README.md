# AutoDog: An automatic documentation generator to document a specific segment of code

[![License](https://img.shields.io/badge/license-MIT-red.svg)](https://opensource.org/license/mit/)

AutoDog uses ChatGPT to generate documentation for specific segments of code automatically.
It can be made documentation of the following language.

- Python
- Fortran
## Requests

- Python 3.9 or above
- OpenAI Python Library

## Installation

```
python -m pip install pip install git+https://github.com/tishikawaz/autodog.git
```

## Usage

### Python

```python:usage_python.py
import autodog

code = autodog.code('your_code.py')
engine = autodog.engine(api_key='YOUR-API-KEY')

# insert code documents to a function, class, module, ...
code.insert_docs(engine)

# overwrite your_code.py
code.write()
```

We can find a code documentation generated by ChatGPT in ['test/python/out.py'](https://github.com/tishikawaz/autodog/blob/main/test/python/out.py). Or please see the AutoDog codes.
AutoDog generated the code documentation by itself.

### Fortran

```python:usage_fortran.py
import autodog

code = autodog.code('your_code.f90')
engine = autodog.engine(api_key='YOUR-API-KEY')

# insert code documents to a function, subroutine, type definition, ...
code.insert_docs(engine)

# overwrite your_code.f90
code.write()
```

We can find a code document generated by ChatGPT in ['test/fortran/out.f90'](https://github.com/tishikawaz/autodog/blob/main/test/fortran/out.f90).

### Options of Engine

You can set the following options.

```python
engine = autodog.engine(
    api_key     = 'YOUR-API-KEY',         # Default is ''. Please set your key.
    doc_type    = 'Numpy style docstring' # Default is 'docstring'.
    model       = 'gpt-3.5-turbo',        # Default is 'gpt-3.5-tubo'. You can chose '/v1/chat/completions' from https://platform.openai.com/docs/models/model-endpoint-compatibility.
    line_length = 128 # Default is 72.
)
```

where `api_key` is the OpenAI API key, `doc_type` si the documentation type, `model` is model of ChatGPT, and `line_lenght` is the maximum number of characters in each line.  

### Insert options

You can set the following options.

```python
code.insert_docs(engine, overwrite=True)
```

where `overwrite` is the option for overwriting code documentation.

## License

[![License](https://img.shields.io/badge/license-MIT-red.svg)](https://opensource.org/license/mit/)

AutoDog is an open source software, it is distributed under the MIT license. More details of the MIT license available at the following file: [LICENSE](LICENSE).