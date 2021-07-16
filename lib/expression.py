"""Contains class definition for containing an expression and its output, in a
format so that it is easily printable with inner details accessible to allow 
for formatting
"""

from .parse import ParsedInput

class Expression:
    def __init__(self, inp) -> None:
        self._parsed = ParsedInput(inp)

    def getInputStr(self) -> str:
        return self._parsed.stringifyOriginal()
    
    def getOutputStr(self) -> list:
        return self._parsed.stringify()
