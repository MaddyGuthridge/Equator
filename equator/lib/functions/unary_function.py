"""Function with only one argument

This class provides code to ensure that single argument functions are given
the correct number of arguments
"""

from . import Function

from ..segment import Segment
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
        
        # TODO: Ensure that there are the correct number of segment (ie, not an
        # ArgSet)

    def evaluate(self):
        return self._py_function(self._on.evaluate(), *self._args)
