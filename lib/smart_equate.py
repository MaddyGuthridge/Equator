
import sympy as sym

from . import parse
from . import segment
from . import main
from . import operation

def equate(inp: str):
    # Determine output mode
    if "->" in inp:
        inp, output_mode = inp.split("->")
        output_mode = output_mode.replace(" ", "")
    else:
        output_mode = None
    prep = parse.prepStrings(inp)
    
    # For each expression, create a segment for it
    parsed = []
    inType = None
    for p in prep:
        seg = segment.Segment(p)
        
        t = seg.getOperatorPrecedence() == operation.operatorPrecedence('=')
        if t:
            t = "eq"
        else:
            t = "ev"
        
        if inType is None:
            inType = t
        elif t != inType:
            raise ValueError("Parse Error: cannot mix expressions and equations")
        
        parsed.append(seg.evaluate())


    if inType is None:
        raise ValueError("Parse Error: expected an expression or input")
    elif inType == "eq":
        res = sym.solve(parsed)
        if not isinstance(res, list):
            res = [res]
        
        for r in res:
            for key, value in r.items():
                value = sym.simplify(value)
                r[key] = main.formatOutput(value)
    elif inType == "ev":
        res = [main.formatOutput(sym.simplify(p, ), output_mode) for p in parsed]
    else:
        raise ValueError("Something went horribly wrong")
    return res
