"""Contains helper functions for Equator functions, such as ensuring valid argument types
"""

from ..segment import Segment
from ..argset import ArgSet

from ..eq_except import EqFunctionArgumentException, EqInternalException

def checkArgCount(name: str, expected: int, args: ArgSet, at_least:bool=False):
    """Ensure that the expected argument count for a function matches the
    actual number of argument supplied

    Args:
        name (str): function name (used in exception message)
        expected (int): expected argument count
        args (Segment): arguments
        at_least (bool, optional): whether `expected` is a minimum number of
                                   arguments (rather than the required).
                                   Defaults to False.

    Raises:
        EqFunctionArgumentException: wrong number of arguments
    """
    
    # If the first element is an ArgSet, we know it will be the only element
    if isinstance(args, ArgSet):
        count = len(args)
    else: # pragma: no cover
        raise EqInternalException("Function arguments not in ArgSet type")
    
    if at_least:
        if count < expected:
            raise EqFunctionArgumentException(
                f"Not enough arguments for function '{name}' (expected at "
                f"least {expected}, got {len(args)})"
                )
    else:
        if count != expected:
            raise EqFunctionArgumentException(
                f"Wrong number of arguments for function '{name}' (expected "
                f"{expected}, got {len(args)})"
                )
    
