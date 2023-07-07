"""A function that returns the given iteration object without any progress
bar.
Parameters:
- iteration_object: The object to be iterated over.
Returns:
- The given iteration object.
Example:
>>> progress_bar_nothing(range(10))
range(0, 10)
"""

import shutil

def progress_bar_nothing(iterable_object:any, **kwargs) -> any:
    """A function that returns the given iteration object without any progress
    bar.
    Parameters:
    - iterable_object: The object to be returned.
    Returns:
    - The given iteration object.
    """
    return iterable_object

def progress_bar(iterable_object:any, bar_char = '█', **kwargs) -> any:
    terminal_size = shutil.get_terminal_size()
    bar_length = int(0.5 * terminal_size.columns)
    itr = list(iterable_object)
    n_objs = len(itr)
    for i, obj in enumerate(itr):
        n_char = int(((i + 1) / n_objs) * bar_length)
        n_blank = bar_length - n_char
        progress_bar = '|' + bar_char * n_char + ' ' * n_blank + '|'
        print("\r", progress_bar, end="", flush=True)
        yield obj
    print("\r", progress_bar, "Finished.")