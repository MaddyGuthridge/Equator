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
        # Unwrap symbols
        if unwrap_symbols:
            return parseToken(operation.getConstant(word), unwrap_symbols=False)
        else:
            return tokens.Symbol(operation.getConstant(word))

def prepString(input: str) -> list:
    input = input.replace(' ', '')
    
    # Split into individual expressions (semicolon separated)
    exprs_str = input.split(";")
    exprs = []
    
    # Parse each expression
    for expr_s in exprs_str:
        words = []
        word = ""
        for i in expr_s:
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
            
        # Only append if it has contents        
        if len(out):
            exprs.append(out)
    
    return exprs
