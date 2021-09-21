"""Generic function class
"""

from ..segment import Segment
from .. import tokens

class Function(Segment):
    """Segment representing a function operation
    """
    def __init__(self, func_name: tokens.Symbol, on: Segment):
        self._op = func_name
        self._on = on

    def __str__(self):
        return self.stringify(str_opts=None)

    def __repr__(self) -> str:
        return f"Function({str(self._op)}, {repr(self._on)})"

    def stringify(self, str_opts: OutputFormatter):
        """Returns string version of function, for presenting to the user

        Args:
            str_opts (OutputFormatter): formatting options for string

        Returns:
            str: string representation of string and its contents
        """
        return f"{self._op.stringify(str_opts)}({self._on.stringify(str_opts)})"

    def evaluate(self):
        """Returns evaluation of the function

        Returns:
            Operatable: result of function
        """
        return NotImplemented

    def getOperatorPrecedence(self):
        """Returns operator precedence of function

        Returns:
            int: precedence
        """
        return operation.FUNCTION_OPERATOR_PRECEDENCE
