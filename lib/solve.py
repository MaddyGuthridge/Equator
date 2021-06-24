import sympy as sym

from fractions import Fraction

from . import main
from . import parse
from . import segment

def solve(inp: str):
    # Parse input
    prep = parse.prepStrings(inp)
    
    # For each expression, create a segment for it
    parsed = []
    for p in prep:
        seg = segment.Segment(p)
        parsed.append(seg.evaluate())

    res = sym.solve(parsed)
    
    if not isinstance(res, list):
        res = [res]

    # Change to fractions if possible
    for r in res:
        for key, value in r.items():
            r[key] = main.formatOutput(value)
    return res
