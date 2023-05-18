from typing import Callable


def copy_doc(func: Callable) -> Callable:
    """Function to copy over the docstring from another function

    Args:
        func (Callable): The function of which the docstring should be copied
    """

    def wrapper(func: Callable) -> Callable:
        func.__doc__ = func.__doc__
        return func

    return wrapper
