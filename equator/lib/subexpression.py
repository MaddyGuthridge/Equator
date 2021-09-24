"""Contains definition for SubExpression class. This represents a singular
mathematical expression or equation (compare to ParsedInput class).
"""

from decimal import Decimal

from . import consts
from . import tokens
from . import operation

from .eq_except import EqTokeniseException
from .eq_object import EqObject
from .segment import Segment

class SubExpression(EqObject):
    """Singular expression or equation, evaluated as a set with other 
    SubExpressions.
    """
    def __init__(self, inp: str) -> None:
        self._tokens = self._parseTokens(inp)
        self._segment = None
        self._evaluation = None
    
    def __repr__(self) -> str:
        if self._segment is None:
            return repr(self._tokens) + " (Not parsed)"
        else:
            return repr(self._segment)
    
    def getTokens(self) -> 'list[tokens.Token]':
        """Returns tokens used by this subexpression

        Returns:
            list[tokens.Token]: tokens
        """
        return self._tokens
    
    def stringifyOriginal(self) -> str:
        return ''.join([t.stringifyOriginal() for t in self._tokens])

    def stringify(self, str_opts) -> str:
        return self.getSegment().stringify(str_opts)

    def getSegment(self) -> Segment:
        """Generate and return a segment that is cached to speed up things
        """
        if self._segment is None:
            self._segment = Segment(self._tokens)
        return self._segment

    def evaluate(self):
        # If the subexpression is empty, return None
        if not len(self._tokens) or\
            (len(self._tokens) == 1\
                and self._tokens[0].getContents() == ""):
                return None
        
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

    def _parseTokens(self, inp) -> 'list[tokens.Token]':
        words = []
        word = ""
        
        # Loop through characters and split by operators
        
        post_op = False # Whether we're adding whitespace after an operator
        skip = 0
        for i, c in enumerate(inp):
            if skip:
                skip -= 1
                continue
            if post_op and c != ' ':
                words.append(word)
                word = ""
                post_op = False
            # HACK: Detect `..` operator
            # Yuck please fix this future me
            if c == '.' and i+1 < len(inp) and inp[i+1] == '.':
                if len(word.strip(' ')):
                    words.append(word)
                    word = ""
                post_op = True
                skip = 1
                word += c # Awful hack to append both dots
            # If we found an operator
            if c in consts.OPERATORS:
                if len(word.strip(' ')):
                    words.append(word)
                    word = ""
                post_op = True
            word += c
        
        if len(word):
            words.append(word)
            
        # Parse out exponent notations
        words = self._parseExponentNotation(words)
        
        # For each word, convert to the required type of token
        out = [self._createToken(word) for word in words]
        return out

    def _createToken(self, word: str) -> 'tokens.Token':
        try:
            if self._isDecimal(word):
                return tokens.Number(word)
            elif word.strip(' ') in consts.OPERATORS:
                return tokens.Operator(word)
            else:
                # Parse symbols and constants
                if word.strip(' ').lower() in consts.NUMERIC_CONSTANTS:
                    return tokens.Constant(word)
                else:
                    # Word is a symbol
                    # Ensure there isn't any whitespace in symbol
                    if not tokens.validSymbol(word):
                        raise EqTokeniseException("Invalid symbol")
                    return tokens.Symbol(word)
        except EqTokeniseException as e:
            return tokens.BadToken(word, e)

    def _parseExponentNotation(self, words: 'list[tokens.Token]')\
        -> 'list[tokens.Token]':
        ret = []
        skip = 0
        for i, word in enumerate(words):
            if skip:
                skip -= 1
                continue
            if self._isWordExponent(word):
                try:
                    # If it's an exponent, then grab the next two elements
                    t_word = [word] + words[i+1: i+3]
                    # And join them together
                    t_word = "".join(t_word)
                    # If there's whitespace, skip joining them
                    if ' ' not in t_word.strip(' '):
                        if not self._isDecimal(t_word):
                            # Join together anyway, and we'll get an error
                            # tokenising which will prevent crashes
                            #raise ValueError("Parser Error: Bad exponent notation")
                            pass
                        word = t_word
                        skip = 2
                except IndexError:
                    # It's missing an exponent, insert the remainder
                    # This will be picked up when creating tokens
                    #raise ValueError("Parser Error: Expected exponent")
                    word = words[i:]
                    # And join them together
                    word = "".join(word)
                    skip = 2
            ret.append(word)
        return ret
    
    def _isWordExponent(self, word: str) -> bool:
        """Returns True if it's the start of an exponent spanning multiple words
        otherwise False
        """
        # If the word is one character long, it can't be using exponent notation
        if len(word) == 1:
            return False
        # If it ends with "e" it might be the first part of an exponent notation number
        if word[-1] in ["e", "E"]:
            if self._isDecimal(word[:-1]):
                return True
        return False

    def _isDecimal(self, word: str) -> bool:
        """Return true if word is a decimal"""
        # Remove leading and trailing spaces
        e: word = word.strip(' ')
        try:
            Decimal(word)
            return True
        except Exception:
            return False
