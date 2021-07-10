from decimal import Decimal

from . import consts
from . import tokens
from . import operation

def isDecimal(word: str):
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
        if word in consts.NUM_CONSTANTS:
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
