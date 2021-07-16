import sympy as sym

from decimal import Decimal

from . import consts
from . import tokens
from . import operation
from .segment import Segment
from .eq_object import EqObject
from .output_formatter import OutputFormatter

def isDecimal(word: str):
    # Remove spaces
    word = word.replace(' ', '')
    try:
        Decimal(word)
        return True
    except Exception:
        return False

def isWordExponent(word: str) -> bool:
    """Returns True if it's the start of an exponent spanning multiple words
    otherwise False
    """
    # If the word is one character long, it can't be using exponent notation
    if len(word) == 1:
        return False
    # If it ends with "e" it might be the first part of an exponent notation number
    if word.endswith("e"):
        if isDecimal(word[:-1]):
            return True
    return False

def parseExponentNotation(words: list):
    ret = []
    skip = 0
    for i, word in enumerate(words):
        if skip:
            skip -= 1
            continue
        if isWordExponent(word):
            try:
                # If it's an exponent, then grab the next two elements
                word = [word] + words[i+1: i+3]
                # And join them together
                word = "".join(word)
                if not isDecimal(word):
                    raise ValueError("Parser Error: Bad exponent notation")
                skip = 2
            except IndexError:
                raise ValueError("Parser Error: Expected exponent")
        ret.append(word)
    return ret

def parseToken(word: str, unwrap_symbols=True):
    if isDecimal(word):
        return tokens.Number(word)
    elif word in consts.OPERATORS:
        return tokens.Operator(word)
    else:
        # Parse symbols and constants
        if word in consts.NUMERIC_CONSTANTS:
            return tokens.Constant(word)
        else:
            return tokens.Symbol(word)

def prepString(input: str) -> list:
    input = input.replace(' ', '')
    input = input.lower()
    words = []
    word = ""
    for i in input:
        if i in consts.OPERATORS:
            if len(word):
                words.append(word)
                word = ""
            words.append(i)
        else:
            word += i
    
    if len(word):
        words.append(word)
    
    # Parse out exponent notations
    words = parseExponentNotation(words)
    
    # For each word, convert to the required type
    out = []
    for word in words:
        out.append(parseToken(word))
    return out

def prepStrings(input: str) -> list:
    
    # Split into individual expressions (semicolon separated)
    exprs_str = input.split(";")
    exprs = []
    
    # Parse each expression
    for expr_s in exprs_str:
        out = prepString(expr_s)
            
        # Only append if it has contents
        if len(out):
            exprs.append(out)
    
    return exprs

class SubExpression(EqObject):
    """List of tokens contained by parsed input
    """
    def __init__(self, inp: str) -> None:
        self._leading_space = len(inp) - len(inp.lstrip(' '))
        self._tokens = self._parseTokens(inp)
        self._segment = None
        self._evaluation = None
    
    def stringifyOriginal(self):
        space = self._leading_space * ' '
        
        tokens_s = [t.stringifyOriginal() for t in self._tokens]
        
        return space + ''.join(tokens_s)

    def _parseTokens(self, inp):
        words = []
        word = ""
        
        # Split by operators
        for i in inp:
            if i in consts.OPERATORS:
                if len(word):
                    words.append(word)
                    word = ""
                words.append(i)
            else:
                word += i
        
        if len(word):
            words.append(word)
            
        # Parse out exponent notations
        words = parseExponentNotation(words)
        
        # For each word, convert to the required type
        out = [parseToken(word) for word in words]
        return out
    
    def getSegment(self) -> Segment:
        """Generate and return a segment that is cached to speed up things
        """
        if self._segment is None:
            self._segment = Segment(self._tokens)
        return self._segment

    def evaluate(self):
        if self._evaluation is None:
            self._evaluation = self.getSegment().evaluate()
        return self._evaluation

    def isEquation(self) -> bool:
        """Returns True if this subexpression is an equation

        Returns:
            bool: whether subexpression is an equation
        """
        return self.getSegment().getOperatorPrecedence()\
            == operation.operatorPrecedence('=')

class ParsedInput(EqObject):
    """Contains parsed information about an input
     - List of TokenLists
     - List of output formatters
    """
    def __init__(self, inp: str) -> None:
        self._leading_space = len(inp) - len(inp.lstrip(' '))
        inp = inp.lstrip(' ')
        
        # Try getting output formatting options
        if "->" in inp:
            inp, output_mode = inp.split("->", 1)
            self._output_mode = OutputFormatter(output_mode)
        else:
            self._output_mode = OutputFormatter(None)

        # Split by individual subexpressions
        exps_str = inp.split(';')
        exps = [SubExpression(s) for s in exps_str]
        
        self._sub_exps = exps
        
        self._evaluation = None
    
    def evaluate(self) -> tuple:
        """Evaluate the input and return results

        Returns:
            tuple: 
                dict: equation results
                list: expression results
        """
        # Caching
        if self._evaluation is not None:
            return self._evaluation
        
        # Determine which are evaluations and equations
        evs = []
        eqs = []
        for e in self._sub_exps:
            if e.isEquation():
                eqs.append(e)
            else:
                evs.append(e)
        
        # Solve the equations
        res = sym.solve(eqs)
        
        if not isinstance(res, list):
            res = [res]
        
        # Substitute equation results into evaluations, then simplify
        # Create one substitution for each set of results
        ev_subs = []
        for r in res:
            ev_subs.append([sym.simplify(sym.sympify(e.evaluate()).subs(r))\
                            for e in evs])
        
        self._evaluation = res, evs
        return self._evaluation
    
    def stringifyOriginal(self):
        return self._leading_space*' ' + ';'.join(self._sub_exps)\
            + '->' + self._output_mode.stringifyOriginal()

    def stringify(self, formatting: OutputFormatter) -> str:
        """Return evaluation as a string

        Args:
            formatting (OutputFormatter): behaviour for stringifying numbers

        Returns:
            str: results
        """
        res, evs = self.evaluate()
        
        out = []
        
        # For each answer set
        for r, e in zip(res, evs):
            
            # For each equation solution
            for symbol, value in r:
                s = Segment(str(symbol) + "=" + str(value))
                out.append(s.stringify(formatting))

            # For each evaluation
            for ev in e:
                s = Segment(str(ev))
                out.append(s.stringify(formatting))

        return '\n'.join(out)
