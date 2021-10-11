"""json_main.py

Contains main function for json IO
"""
    
import json

from equator import equate, EqExternalException, Expression

from ..lib.consts import VERSION

from .jsonify import tokenListToJsonable

def tokeniseInput(inp: str):
    e = Expression(inp)
    
    subexprs, formatters = e.getInputTokens()
    
    return {
        "expressions":
            [
                tokenListToJsonable(l) for l in subexprs
            ],
        "formatters":
            [
                formatters
            ]
    }

def completeRequest(r: 'dict[str]') -> dict:
    
    try:
        version = r["api_version"]
        argument = r["argument"]
        request = r["request"]
    except KeyError:
        return {
            "api_version": VERSION,
            "success": False,
            "response":
                {
                    "error_msg": "missing required request arguments"
                }
        }
    
    if request == "tokenise":
        ret = tokeniseInput(argument)
    elif request == "solve":
        ...
    
    return {
        "api_version": VERSION,
        "success": True,
        "response": ret
    }

def json_main():
    try:
        while True:
            try:
                inp = json.loads(input())
                print(json.dumps(completeRequest(inp), indent=None))
            except EqExternalException as e:
                print(str(e))
            except json.JSONDecodeError:
                pass
    except EOFError:
        return
