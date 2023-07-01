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

def progress_bar_nothing(iteration_object, **kwargs):
    """A function that returns the given iteration object without any progress
    bar.
    Parameters:
    - iteration_object: The object to be returned.
    Returns:
    - The given iteration object.
    """
    return iteration_object