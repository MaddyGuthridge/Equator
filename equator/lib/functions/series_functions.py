"""Functions for performing bulk operations on a set of numbers
"""

from decimal import Decimal

import sympy as sym

from .. import tokens

from .function import Function
from ..argset import ArgSet
from ..eq_except import EqFunctionArgumentException
from ..segment import Segment

from .function_helpers import assertArgCount, isTokenInteger

class SeriesFunction(Function):
    """An abstract function used to imitate the functionality of series 
    operations such as sigma notation sums
    
    Syntax: `operation(var = start, end, expression)`
    Starts at 1 and steps up to and including end, substituting var into 
    expression, running operation for each result to get a cumulative total
    """
    def __init__(self, func_name: str, on: ArgSet):
        """Create a series operation function

        Args:
            func_name (str): name of function (eg sum or mul)
            on (ArgSet): function arguments
        """
        super().__init__(tokens.Symbol(func_name), on)
        
        assertArgCount(func_name, 3, on)
        
        # Check validity of arguments
        if (
            # First arg
            len(on[0]) != 3
         or not isinstance(on[0][0], tokens.Symbol) # var
         or not (on[0][1] == "=")                   # =
         or not isTokenInteger(on[0][2])            # start
            # Second arg
         or not isTokenInteger(on[1])               # end
        ):
            raise EqFunctionArgumentException(
                f"Incorrect argument types for {func_name}. Expected "
                f"{func_name}(var = start, end, expression)"
                )
        
        # Store for evaluation
        self._var = on[0][0]
        self._start = on[0][2]
        self._end = on[1]
        self._expression = on[2]

    def evaluate(self, operation):
        """Evaluate the function's result

        Args:
            operation (lambda function): operation to perform to join values
        """
        
        total = None

        expr = self._expression.evaluate()
        var = self._var.evaluate()

        for i in range(int(self._start.evaluate()), int(self._end.evaluate()) + 1):
            
            # If expression is doesn't contain variable to substitute
            # Workaround for https://github.com/sympy/sympy/issues/22142
            # Expression is constant
            if isinstance(expr, Decimal):
                val = expr
            # Expression contains variables
            # Credit: https://stackoverflow.com/a/31050711/6335363
            elif isinstance(expr, sym.Basic) and var not in expr.free_symbols:
                val = expr
            # Otherwise, substitute value of n
            else:
                val = sym.Subs(expr, var, i)
            
            if total is None:
                total = val
            else:
                total = operation(total, val)
        
        return total

class SumFunction(SeriesFunction):
    """Represents a sigma notation sum expression
    """
    def __init__(self, on: ArgSet):
        super().__init__("sum", on)

    def evaluate(self):
        return super().evaluate(lambda x, y: x + y)

class MulFunction(SeriesFunction):
    """Represents a sigma notation sum expression
    """
    def __init__(self, on: ArgSet):
        super().__init__("mul", on)

    def evaluate(self):
        return super().evaluate(lambda x, y: x * y)
