"""Function with only one argument

This class provides code to ensure that single argument functions are given
the correct number of arguments
"""

from . import Function

from ..segment import Segment
from ..argset import ArgSet
from ..eq_except import EqFunctionArgumentException
from .. import tokens

from .function_helpers import assertArgCount

class UnaryFunction(Function):
    """A function that only takes one argument
    """
    
    def __init__(self, func_name: tokens.Symbol, on: ArgSet, 
                 py_function, *args):
        """Create unary functions

        Args:
            func_name (tokens.Symbol): function name (for stringification)
            on (ArgSet): ArgSet to operate on
            py_function (lambda function): function to do
            args: any extra arguments sent to the function required to ensure
                  correct behaviour
        """
        self._py_function = py_function
        self._args = args
        super().__init__(func_name, on)
        
        assertArgCount(func_name.stringify(None), 1, on)

    def evaluate(self):
        return self._py_function(self._on[0].evaluate(), *self._args)
