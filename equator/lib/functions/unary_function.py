"""Function with only one argument

This class provides code to ensure that single argument functions are given
the correct number of arguments
"""

from . import Function

from ..segment import Segment
from ..argset import ArgSet
from ..eq_except import EqFunctionException
from .. import tokens

class UnaryFunction(Function):
    """A function that only takes one argument
    """
    
    def __init__(self, func_name: tokens.Symbol, on: Segment, 
                 py_function: 'function', *args):
        """Create unary functions

        Args:
            func_name (tokens.Symbol): function name (for stringification)
            on (Segment): segment to operate on
            py_function (function): function to do
            args: any extra arguments sent to the function required to ensure
                  correct behaviour
        """
        self._py_function = py_function
        self._args = args
        super().__init__(func_name, on)
        
        if (len(on) == 1 and isinstance(on[0], ArgSet)):
            raise EqFunctionException(f"Too many arguments for function "
                                      f"{func_name} (expected 1, got "
                                      f"{len(on[0])})")

    def evaluate(self):
        return self._py_function(self._on.evaluate(), *self._args)
