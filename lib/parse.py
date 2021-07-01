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

def parseToken(word: str, unwrap_symbols=True):
    if isDecimal(word):
        return tokens.Number(word)
    elif word in consts.OPERATORS:
        return tokens.Operator(word)
    else:
        # Parse symbols and constants
        if word in consts.CONSTANTS:
            return tokens.Constant(word)
        else:
            return tokens.Symbol(word)

def prepString(input: str) -> list:
    input = input.replace(' ', '')
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
