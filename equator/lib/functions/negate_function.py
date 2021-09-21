"""Negate function: used to help with leading negatives
"""

from .function import Function

from ..segment import Segment
from .. import consts
from ..output_formatter import OutputFormatter


class NegateFunction(Function):
    """Special function for representing leading negatives
    """
    def __init__(self, on: Segment):
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

    def evaluate(self):
        return -self._on
