"""Detect what function type is required and return an
instance of that
"""

from decimal import Decimal, InvalidOperation

from .. import tokens
from ..segment import Segment
from ..eq_except import EqFunctionNameException, EqFunctionException, EqInternalException
from ..eval_options import EvalOptions

from .function import Function
from .basic_functions import *
from .negate_function import NegateFunction
from .rad_deg_functions import *
from .lcm_gcd_functions import LcmFunction, GcdFunction
from .series_functions import SumFunction, MulFunction
from .calculus_functions import DifferentiateFunction, IntegrateFunction

EQUATOR_FUNCTIONS = {
    "neg": NegateFunction,
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
    "lcm": LcmFunction,
    "gcd": GcdFunction,
    "sum": SumFunction,
    "mul": MulFunction,
    "diff": DifferentiateFunction,
    "int": IntegrateFunction,
}

def detectFunction(func: tokens.Symbol, args: Segment) -> Function:
    """Detects what function is required, and returns a Function object of that
    type

    Args:
        func (tokens.Symbol): function name
        args (Segment): function arguments
    """
    
    # HACK: We need a better way to compare a token to a string
    # in a list
    func_str = func.stringify(None)
    
    # Check for a simple function
    if func_str in EQUATOR_FUNCTIONS:
        return EQUATOR_FUNCTIONS[func_str](args)

    # Otherwise, check for a more complex type (eg log_base)
    if func_str.startswith("log_"):
        try:
            base = Decimal(func_str.replace("log_", ""))
        except InvalidOperation: # pragma: no cover
            raise EqInternalException(f"Bad base for logarithm \"{func_str}\"")
        return LogBaseFunction(args, base)

    # If we reach here, we didn't recognise the function, so raise an exception
    raise EqFunctionNameException(f"Unrecognised function name: {func}")
