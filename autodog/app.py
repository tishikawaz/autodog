"""
AutoDog Application
This function is the entry point for the AutoDog application. It
generates documentation for a specific segment of code.
Args:
    path (str): The path to the code segment to be documented.
    -e, --engine (str, optional): The documentation generation engine
    name.
        Defaults to 'chatgpt'.
    -k, --key (str, optional): The API key for the documentation
    generation
        engine. Defaults to an empty string.
    -r, --recursively (bool, optional): Flag to recursively generate
        documentation in the entire directory structure. Defaults to
        False.
    -o, --overwrite (bool, optional): Flag to overwrite existing
        documentation. Defaults to False.
Returns:
    None
"""
from autodog.core import code, engine
from autodog.utils.progress import progress_bar
import openai
import argparse
import glob
import os
from time import sleep

def _insert_doc(code, engine, overwrite, n_tries, interval=20):
    for n in range(n_tries):
        try:
            code.insert_docs(engine, overwrite=overwrite,  progress_bar=progress_bar)
            return
        except openai.error.ServiceUnavailableError as e:
            print()
            print(f'[{n}/{n_tries} try]: An exception was thrown from `insert_docs` due to the following:')
            print(f'Service Unavailable Error: {e}')
            print(f'Continue.')
            sleep(interval)
            continue
        except openai.error.APIError as e:
            print()
            print(f'[{n}/{n_tries} try]: An exception was thrown from `insert_docs` due to the following:')
            print(f'API Error: {e}')
            print(f'Continue.')
            sleep(interval)
            continue
    print('Give up!')
    return

def app():
    """
    AutoDog Application
    This function is the entry point for the AutoDog application. It
    generates documentation for a specific segment of code.
    Args:
        path (str): The path to the code segment to be documented.
        -e, --engine (str, optional): The documentation generation engine
        name.
        Defaults to 'chatgpt'.
        -k, --key (str, optional): The API key for the documentation
        generation
        engine. Defaults to an empty string.
        -r, --recursively (bool, optional): Flag to recursively generate
        documentation in the entire directory structure. Defaults to False.
        -o, --overwrite (bool, optional): Flag to overwrite existing
        documentation. Defaults to False.
    Returns:
        None
    """
    parser = argparse.ArgumentParser(prog='AutoDog', description='An automatic documentation generator to document a specific segment of code')
    parser.add_argument('path', help='Code filepath you want to write a documentation automatically.')
    parser.add_argument('-k', '--key', help='API key.', default='')
    parser.add_argument('-r', '--recursively', help='Recursively generate documentation in the entire directory structure.', action='store_true')
    parser.add_argument('-e', '--extension', help='File extension you want to select.', default='py', choices=['py', 'f90', 'f'])
    parser.add_argument('--engine', help='Documentation generation engin name.', default='chatgpt', choices=['chatgpt', 'dummy'])
    parser.add_argument('--overwrite', help='Overwrite documentation.', action='store_true')
    parser.add_argument('--tries', help='Number of reconnections on server errors.', default=3, type=int)
    args = parser.parse_args()
    e = engine(name=args.engine, api_key=args.key)
    if args.recursively:
        for dir in glob.glob(f'{args.path}/**/', recursive=True):
            for file in glob.glob(f'{dir}/*.{parser.extension}'):
                c = code(file)
                print('Insert documentation to', file)
                _insert_doc(c, e, args.overwrite, args.tries)
                c.write()
    else:
        c = code(args.path)
        _insert_doc(c, e, args.overwrite, args.tries)
        c.write()
if __name__ == '__main__':
    app()