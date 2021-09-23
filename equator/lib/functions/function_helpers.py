"""Contains helper functions for Equator functions, such as ensuring valid argument types
"""

from decimal import Decimal

from ..eq_object import EqObject
from ..argset import ArgSet

from ..eq_except import EqFunctionArgumentException, EqInternalException

def assertArgCount(name: str, expected: int, args: ArgSet, at_least:bool=False):
    """Ensure that the expected argument count for a function matches the
    actual number of argument supplied, and raise an exception if not.

    Args:
        name (str): function name (used in exception message)
        expected (int): expected argument count
        args (ArgSet): arguments
        at_least (bool, optional): whether `expected` is a minimum number of
                                   arguments (rather than the required).
                                   Defaults to False.

    Raises:
        EqFunctionArgumentException: wrong number of arguments
    """
    
    # If the first element is an ArgSet, we know it will be the only element
    if not checkArgCount(expected, args, at_least):
            raise EqFunctionArgumentException(
                f"Not enough arguments for function '{name}' (expected "
                f"{'at least' if at_least else ''} {expected}, got {len(args)})"
                )

def checkArgCount(expected: int, args: ArgSet, at_least:bool=False) -> bool:
    """Check whether the expected argument count for a function matches the
    actual number of argument supplied

    Args:
        expected (int): expected argument count
        args (ArgSet): arguments
        at_least (bool, optional): whether `expected` is a minimum number of
                                   arguments (rather than the required).
                                   Defaults to False.

    Returns:
        bool: whether there is the right number of arguments
    """
    
    # If the first element is an ArgSet, we know it will be the only element
    if isinstance(args, ArgSet):
        count = len(args)
    else: # pragma: no cover
        raise EqInternalException("Function arguments not in ArgSet type")
    
    if at_least:
        return count >= expected
    else:
        return count == expected

def isTokenInteger(value: EqObject) -> bool:
    """Returns whether the contents of an EqObject evaluates to an integer

    Args:
        value (EqObject): value to check

    Returns:
        bool: whether value is an integer
    """
    try:
        dec = Decimal(value.evaluate())

        return dec == int(dec)
    except Exception as e:
        return False
