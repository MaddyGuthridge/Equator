from fractions import Fraction
from decimal import Decimal
import sympy as sym

from . import operation

class Token:
    """Token base type
    All tokens are derived from this
    """
    def __init__(self, value: str) -> None:
        self._contents = value
    
    def __str__(self) -> str:
        return self._contents
    
    def __repr__(self) -> str:
        return self._contents + " (Token)"

    def evaluate(self):
        return self._contents

class Operator(Token):
    """Token representing an operator
    Evaluate returns operator string
    """

    def __eq__(self, o: object) -> bool:
        if isinstance(o, str):
            return o == self._contents
    
    def __repr__(self) -> str:
        return self._contents + " (Operator)"

class Number(Token):
    """Token representing a number
    Evaluate returns numberified version
    """
    def evaluate(self):
        return operation.conditionalFraction(Decimal(self._contents))
    
    def __repr__(self) -> str:
        return self._contents + " (Number)"

class Symbol(Token):
    """Token representing a symbol
    Evaluate regeisters and returns a SymPy symbol
    
    Note, depending on context, this could be a function
    """
    def evaluate(self):
        return sym.Symbol(self._contents)

    def __repr__(self) -> str:
        return self._contents + " (Symbol)"
