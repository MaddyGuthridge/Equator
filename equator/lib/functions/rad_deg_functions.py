"""Functions for converting between degrees and radians
"""

from .unary_function import UnaryFunction

from .. import tokens
from ..segment import Segment
from ..eval_options import EvalOptions
from .. import consts

class DegFunction(UnaryFunction):
    """Degrees function"""
    def __init__(self, on: Segment):
        super().__init__(tokens.Symbol("deg"), on,
                         lambda x: x * 180 / consts.NUMERIC_CONSTANTS["pi"])

class RadFunction(UnaryFunction):
    """Radians function"""
    def __init__(self, on: Segment):
        super().__init__(tokens.Symbol("rad"), on,
                         lambda x: x / 180 * consts.NUMERIC_CONSTANTS["pi"])
