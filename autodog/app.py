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
    parser.add_argument('path')
    parser.add_argument('-e', '--engine', help='Documentation generation engin name.', default='chatgpt')
    parser.add_argument('-k', '--key', help='API key.', default='')
    parser.add_argument('-r', '--recursively', help='Recursively generate documentation in the entire directory structure.', default=False)
    parser.add_argument('-o', '--overwrite', help='Overwrite documentation.', default=False)
    args = parser.parse_args()
    e = engine(name=args.engine, api_key=args.key)
    if args.recursively:
        for dir in glob.glob(f'{args.path}/**/', recursive=True):
            for file in glob.glob(f'{dir}/*.py'):
                c = code(file)
                print('Insert documentation in', file)
                c.insert_docs(e, overwrite=args.overwrite)
                c.write()
    else:
        c = code(args.path)
        c.insert_docs(e, overwrite=args.overwrite)
        c.write()
if __name__ == '__main__':
    app()