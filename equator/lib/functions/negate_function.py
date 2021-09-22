"""Negate function: used to help with leading negatives
"""

from .unary_function import UnaryFunction

from .. import tokens
from ..segment import Segment
from ..argset import ArgSet
from .. import consts
from ..output_formatter import OutputFormatter


class NegateFunction(UnaryFunction):
    """Special function for representing leading negatives
    """
    def __init__(self, on: ArgSet):
        super().__init__(tokens.Symbol(consts.NEGATE), on, lambda x: -x)
        self._op = consts.NEGATE
        self._on = on
    
    def __str__(self):
        return self.stringify(None)

    def stringify(self, num_mode: OutputFormatter):
        """Return string representing contents

        Args:
            num_mode (OutputFormatter): string formatting options

        Returns:
            str: contents
        """
        return f"-{self._on.stringify(num_mode)}"
