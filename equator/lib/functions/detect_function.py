"""Detect what function type is required and return an
instance of that
"""

from .. import tokens
from ..segment import Segment
from ..eq_except import EqFunctionNameException

from .function import Function
from .basic_functions import *
from .negate_function import NegateFunction

def detectFunction(func: tokens.Symbol, args: Segment) -> Function:
    """Detects what function is required, and returns a Function object of that
    type

    Args:
        func (tokens.Symbol): function name
        args (Segment): function arguments
    """
    
    simple_funcs = {
        "sqrt": SqrtFunction,
        "sin": SinFunction,
        "cos": CosFunction,
        "tan": TanFunction,
        "asin": AsinFunction,
        "acos": AcosFunction,
        "atan": AtanFunction,
        "abs": AbsFunction,
        "deg": DegFunction,
        "rad": RadFunction,
        "exp": ExpFunction,
        "ln": LnFunction,
        "log": LogFunction,
    }
    
    # HACK: We need a better way to compare a token to a string
    # in a list
    func_str = func.stringify(None)
    
    # Check for a simple function
    if func_str in simple_funcs:
        return simple_funcs[func_str](args)

    # Otherwise, check for a more complex type (eg log_base)
    if func_str.startswith("log_"):
        try:
            base = Decimal(func.replace("log_", ""))
        except:
            raise EqFunctionException(f"Bad base for logarithm \"{func}\"")
        return LogBaseFunction(args, base)

    # If we reach here, we didn't recognise the function, so raise an exception
    raise EqFunctionNameException(f"Unrecognised function name: {func}")
