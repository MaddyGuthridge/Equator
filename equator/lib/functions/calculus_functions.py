"""Functions for integration and differentiation
"""

import sympy

from .function import Function
from .function_helpers import assertArgCount, isTokenInteger

from .. import tokens
from ..argset import ArgSet
from ..eq_except import EqFunctionArgumentException
from ..eval_options import EvalOptions

class DifferentiateFunction(Function):
    """Function that differentiates its arguments
    """
    def __init__(self, on: ArgSet):
        super().__init__(tokens.Symbol("diff"), on)
        
        assertArgCount("diff", 2, on)
        
        self._expr = on[0]
        
        # Check that differential argument is symbol
        if not (len(on[1]) == 1 and isinstance(on[1][0], tokens.Symbol)):
            raise EqFunctionArgumentException("Expected a symbol for 2nd "
                                              "argument")
        
        # With respect to symbol
        self._wrt = on[1]
        
    def evaluate(self, options:EvalOptions=None):
        options = EvalOptions(options, number_as_rational=True)
        return sympy.diff(self._expr.evaluate(options), self._wrt.evaluate(options)).doit()

class IntegrateFunction(Function):
    """Function that integrates its arguments
    """
    def __init__(self, on: ArgSet):
        super().__init__(tokens.Symbol("int"), on)
        
        assertArgCount("int", 2, on)
        
        self._expr = on[0]
        
        # Check that differential argument is symbol
        if (len(on[1]) == 1 and isinstance(on[1][0], tokens.Symbol)):
            self._has_range = False
            self._wrt = on[1]
        # Given range as well
        elif len(on[1]) == 3 and\
            (
                isinstance(on[1][0], tokens.Symbol)
            and on[1][2].getOperator() == ".."
            and isTokenInteger(on[1][2][0])
            and isTokenInteger(on[1][2][2])
            ):
            self._has_range = True
            self._wrt = on[1][0]
            self._start = on[1][2][0]
            self._end = on[1][2][2]
        else:
            raise EqFunctionArgumentException("Expected a symbol and optional "
                                              "range for 2nd argument")
        
    def evaluate(self, options:EvalOptions=None):
        options = EvalOptions(options, number_as_rational=True)
        exp = self._expr.evaluate(options)
        wrt = self._wrt.evaluate(options)
        if self._has_range:
            ret = sympy.integrate(exp, (wrt, self._start, self._end))
        else:
            ret = sympy.integrate(exp, wrt)
        if isinstance(ret, sympy.Integral):
            raise EqFunctionArgumentException("Unable to evaluate integral")
        return ret
