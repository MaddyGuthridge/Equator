import math
import sympy as sym

from fractions import Fraction
from decimal import Decimal, Context, localcontext

from . import operation
from .consts import NUMBER_FORMATTERS, NUMERIC_CONSTANTS, FRACTION_DENOM_LIMITER
from .eq_object import EqObject
from .output_formatter import OutputFormatter

class Token(EqObject):
    """Token base type
    All tokens are derived from this
    """
    def __init__(self, value: str) -> None:
        self._original = value
    
    def getContents(self) -> str:
        """Returns token contents (with spacing removed)

        Returns:
            str: contents
        """
        return self._original.replace(' ', '')
    
    def __str__(self) -> str:
        return self.getContents()
    
    def __repr__(self) -> str:
        return self.getContents()

    def stringify(self, str_options: OutputFormatter) -> str:
        return str(self)
    
    def stringifyOriginal(self) -> str:
        return self._original

    def evaluate(self):
        return self.getContents()
    
    def getOperatorPrecedence(self):
        return operation.NO_OPERATION_PRECEDENCE

class Operator(Token):
    """Token representing an operator
    Evaluate returns operator string
    """

    def __eq__(self, o: object) -> bool:
        if isinstance(o, str):
            return o == self.getContents()

def asMultipleOf(a: Decimal, b: str):
    """Returns a in terms of b if doing so makes sense

    Args:
        a (Decimal): number
        b (str): constant

    Returns:
        str | None: a in terms of b or a normally (but None if doing so is unreasonable)
    """
    # FIXME: present as pi/3 rather than 1/3*pi
    ret = str(Fraction(a / NUMERIC_CONSTANTS[b]).limit_denominator(FRACTION_DENOM_LIMITER))
    if ret == "0":
        return None
    if len(ret) < 10:
        if ret == "1":
            return b
        return ret + "*" + b
    else:
        return None

def asPowerOf(a: Decimal, b: str):
    """Returns a as a power of b if doing so makes sense

    Args:
        a (Decimal): number
        b (str): constant

    Returns:
        str | None: a as a power of b or a normally (but None if doing so is unreasonable)
    """
    ret = str(Fraction(math.log(a, NUMERIC_CONSTANTS[b])).limit_denominator(FRACTION_DENOM_LIMITER))
    # Add brackets if it's a fraction
    if "/" in ret:
        ret = f"({ret})"
    # Prevent returning this when it's zero since that doesn't read as well as just zero
    if ret == "0":
        return None
    # Return the base if it's just a power of 1
    if ret == "1":
        return b
    # If it's a reasonable length, return it as a power
    if len(ret) < 10:
        return b + "^" + ret
    # otherwise return None
    else:
        return None

def strDecimal_Sci(d: Decimal) -> str:
    return f"{d.normalize():e}"

def strDecimal_Norm(d: Decimal) -> str:
    return f"{d.normalize():f}"

def stringifyDecimal(d: Decimal):
    # Note: this would fail for d = 0, but there is a check earlier in a 
    # parent function
    a = abs(math.log10(abs(d)))
    if a < 9:
        return strDecimal_Norm(d)
    else:
        return strDecimal_Sci(d)

class Number(Token):
    """Token representing a number
    Evaluate returns numberified version
    """
    def evaluate(self):
        return Decimal(self.getContents())

    def str_number(self):
        """Stringifies to a number 
        (either standard or scientific notation)

        Returns:
            str: number
        """
        return stringifyDecimal(self.evaluate())

    def str_scientific(self):
        """Always stringifies to scientific notation
        """
        return strDecimal_Sci(self.evaluate())
    
    def str_decimal(self):
        """Always stringifies to standard decimal notation
        """
        return strDecimal_Norm(self.evaluate())

    def stringify(self, str_options: OutputFormatter):
        if str_options.getNumFormatting() is NUMBER_FORMATTERS.SMART:
            return str(self)
        elif str_options is NUMBER_FORMATTERS.DECIMAL:
            return self.str_decimal()
        elif str_options is NUMBER_FORMATTERS.SCIENTIFIC:
            return self.str_scientific()
        elif str_options is NUMBER_FORMATTERS.NUMBER:
            return self.str_number()
        else:
            raise ValueError("Bad stringify mode")

    def __str__(self) -> str:
        """Smart stringify: determines the best format and stringifies to that

        Returns:
            str: evaluation
        """
        ev = self.evaluate()
        
        # Check for zeros
        if ev == 0:
            return "0"
        
        # Check for multiples of pi
        in_pi = asMultipleOf(ev, "pi")
        if in_pi is not None: return in_pi
        # And of e
        in_e = asPowerOf(ev, "e")
        if in_e is not None: return in_e
        
        # Present as fraction if possible
        fract = str(Fraction(ev).limit_denominator(FRACTION_DENOM_LIMITER))
        if len(fract) < 10 and fract != "0":
            # If it's a whole number
            if '/' not in fract:
                return stringifyDecimal(ev)
            return fract
        
        # Check for square roots
        sqr = Fraction(ev ** 2).limit_denominator(FRACTION_DENOM_LIMITER)
        if len(str(sqr)) < 10 and sqr != 0:
            mul, rt = operation.reduceSqrt(sqr)
            mul = f"{mul}*" if mul != 1 else ""
            return f"{mul}sqrt({rt})"
        
        return stringifyDecimal(ev)

class Constant(Number):
    """Token representing a constant such as pi. 
    Stringifies to the name of the constant
    """
    def evaluate(self):
        return NUMERIC_CONSTANTS[self.getContents()]
    
    def __str__(self) -> str:
        return self.getContents()

class Symbol(Token):
    """Token representing a symbol
    Evaluate registers and returns a SymPy symbol
    
    Note, depending on context, this could be a function
    """
    def evaluate(self):
        return sym.Symbol(self.getContents())
