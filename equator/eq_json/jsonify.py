"""Helper functions to convert Equator types to JSONable types
"""

from ..lib import tokens

def tokenToJsonable(token: tokens.Token) -> dict:
    
    value = token.stringify(None)
    repr = token.stringifyOriginal()
    if isinstance(token, tokens.Number):
        type = "number"
    elif isinstance(token, tokens.Constant):
        type = "constant"
    elif isinstance(token, tokens.Operator):
        type = "operator"
    elif isinstance(token, tokens.Symbol):
        type = "symbol"
    elif isinstance(token, tokens.BadToken):
        type = "undefined"
    comments = []
    
    return {
        "value": value,
        "repr": repr,
        "type": type,
        "comments": comments
    }

def tokenListToJsonable(tokenList: 'list[tokens.Token]'):
    return [tokenToJsonable(t) for t in tokenList]

