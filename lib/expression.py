"""Contains class definition for containing an expression and its output, in a
format so that it is easily printable with inner details accessible through
simple function calls to allow for formatting in external code.
"""

from . import tokens

from .parsedinput import ParsedInput

class Expression:
    def __init__(self, inp) -> None:
        self._parsed = ParsedInput(inp)

    def __repr__(self) -> str:
        return repr(self._parsed)

    def getInputStr(self) -> str:
        return self._parsed.stringifyOriginal()
    
    def getInputTokens(self) -> 'tuple[list[list[tokens.Token]], str]':
        return self._parsed.getTokens()

    def getOutputStr(self) -> str:
        return self._parsed.stringify()

    def getOutputList(self) -> list:
        return self._parsed.resultSet()
    
    def getOutputTokens(self) -> list:
        return self._parsed.resultsTokens()
