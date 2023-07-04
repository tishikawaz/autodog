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
import argparse
import glob

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
    args = parser.parse_args()
    e = engine(name=args.engine, api_key=args.key)
    if args.recursively:
        for dir in glob.glob(f'{args.path}/**/', recursive=True):
            for file in glob.glob(f'{dir}/*.{parser.extension}'):
                c = code(file)
                print('Insert documentation in', file)
                c.insert_docs(e, overwrite=args.overwrite, progress_bar=progress_bar)
                c.write()
    else:
        c = code(args.path)
        c.insert_docs(e, overwrite=args.overwrite, progress_bar=progress_bar)
        c.write()
if __name__ == '__main__':
    app()