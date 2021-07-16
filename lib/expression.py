"""Contains class definition for containing an expression and its output
"""

from .smart_equate import equate

class Expression:
    def __init__(self, inp) -> None:
        self._string = inp
        self._result = equate(inp)

    def getInput(self) -> str:
        return self._string
    
    def getOutput(self) -> list:
        return self._result
