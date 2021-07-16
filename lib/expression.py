"""Contains class definition for containing an expression and its output, in a
format so that it is easily printable with inner details accessible to allow 
for formatting
"""

from .smart_equate import equate
from .parse import S

class Expression:
    def __init__(self, inp) -> None:
        self._string = inp
        self._result = equate(inp)

    def getInput(self) -> str:
        return self._string
    
    def getOutput(self) -> list:
        return self._result

class ExpressionInput:
    """Contains list of tokens for inputs
    """
    def __init__(self, inp: str) -> None:
        self._inp = inp

class ExpressionOutput:
    """Contains list of TokenLists containing individual outputs
    """
