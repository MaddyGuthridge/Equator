
import sympy as sym

from . import parse
from . import segment
from . import main

def equate(input: str):
    prep = parse.prepStrings(input)
    
    # For each expression, create a segment for it
    parsed = []
    for p in prep:
        seg = segment.Segment(p)
        parsed.append(seg.evaluate())

    res = sym.solve(parsed)
    
    # Format results
    if len(res) == 0:
        # If we didn't get a result when we solved, return the unsolved expression
        res = [main.formatOutput(p) for p in parsed]
    else:
        # Otherwise its a set of equations
        if not isinstance(res, list):
            res = [res]
        
        for r in res:
            for key, value in r.items():
                r[key] = main.formatOutput(value)
    return res
