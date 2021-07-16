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
    if word[-1] in ["e", "E"]:
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
    elif word.strip(' ') in consts.OPERATORS:
        return tokens.Operator(word)
    else:
        # Parse symbols and constants
        if word.strip(' ') in consts.NUMERIC_CONSTANTS:
            return tokens.Constant(word)
        else:
            # Word is a symbol
            # Ensure there isn't any whitespace in symbol
            if ' ' in word.strip(' '):
                raise ValueError(f"Found whitespace in word: {word}")
            return tokens.Symbol(word)

class SubExpression(EqObject):
    """List of tokens contained by parsed input
    """
    def __init__(self, inp: str) -> None:
        self._leading_space = len(inp) - len(inp.lstrip(' '))
        inp = inp.lstrip(' ')
        self._tokens = self._parseTokens(inp)
        self._segment = None
        self._evaluation = None
    
    def __repr__(self) -> str:
        if self._segment is None:
            return repr(self._tokens) + " (Not parsed)"
        else:
            return repr(self._segment)
    
    def stringifyOriginal(self):
        space = self._leading_space * ' '
        
        tokens_s = [t.stringifyOriginal() for t in self._tokens]
        
        return space + ''.join(tokens_s)

    def stringify(self, str_opts) -> str:
        return self.getSegment().stringify(str_opts)

    def _parseTokens(self, inp):
        words = []
        word = ""
        
        # Loop through characters and split by operators
        
        post_op = False # Whether we're adding whitespace after an operator
        for i in inp:
            if post_op and i != ' ':
                words.append(word)
                word = ""
                post_op = False
            # If we found an operator
            if i in consts.OPERATORS:
                if len(word.strip(' ')):
                    words.append(word)
                    word = ""
                post_op = True
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
            self._output_formatter = OutputFormatter(output_mode)
        else:
            self._output_formatter = OutputFormatter(None)

        # Split by individual subexpressions
        exps_str = inp.split(';')
        exps = [SubExpression(s) for s in exps_str]
        
        self._sub_exps = exps
        
        self._evaluation = None
    
    def __repr__(self) -> str:
        return repr(self._sub_exps) + " -> " + repr(self._output_formatter)
    
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
                eqs.append(e.evaluate())
            else:
                evs.append(e.evaluate())
        
        # Solve the equations
        res = sym.solve(eqs)
        
        # Make sure we have a list of sets of solutions all the time
        # If it's empty
        if not len(res):
            res = [dict()]
        # Otherwise if there's only one set of answers
        elif not isinstance(res, list):
            res = [res]
        
        # Substitute equation results into evaluations, then simplify
        # Create one substitution for each set of results
        ev_subs = []
        for r in res:
            ev_subs.append([sym.simplify(sym.sympify(e).subs(r))\
                            for e in evs])
        
        ret = [(r, e) for r, e in zip(res, ev_subs)]
        self._evaluation = ret
        return self._evaluation
    
    def stringifyOriginal(self):
        ret = self._leading_space*' ' \
            + ';'.join([exp.stringifyOriginal() for exp in self._sub_exps])
        if self._output_formatter.givenArgs():
            ret += "->" + self._output_formatter.stringifyOriginal()
        return ret

    def result_set(self) -> list:
        """Returns results of an evaluation in a format that can be parsed
        programmatically

        Returns:
            list: list of result sets (each set contains a list of solutions,
                  and a list of expression evaluations in a tuple)
        """
        evaluation = self.evaluate()
        
        out = []
        # Loop through each set of solutions
        for eqs, evs in evaluation:
            
            # Format equations
            new_eqs = []
            for key, value in eqs.items():
                s = SubExpression(str(key) + "=" + str(value))
                new_eqs.append(s.stringify(self._output_formatter))
            
            # Format evaluations
            new_evs = []
            for e in evs:
                s = SubExpression(str(e))
                new_evs.append(s.stringify(self._output_formatter))
            
            # Add them both to the formatted set
            out.append((new_eqs, new_evs))

        return out

    def stringify(self) -> str:
        """Return evaluation as a string

        Returns:
            str: results
        """
        evaluation = self.result_set()
        
        out = []
        
        do_prepend = len(evaluation) > 1
        
        for i, (eqs, evs) in enumerate(evaluation):
            if do_prepend:
                out += [f'[{i+1}]:']
            for e in eqs:
                out += ['\t' + e] if do_prepend else [e]
            for e in evs:
                out += ['\t' + e] if do_prepend else [e]

        return '\n'.join(out)
