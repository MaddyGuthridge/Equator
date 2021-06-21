import sympy as sym

from fractions import Fraction

from . import parse
from . import segment

def solve(inp: str):
    # Parse input
    prep = parse.prepString(inp)
    
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
            v = Fraction(str(value))
            if len(str(v)) < 10:
                r[key] = str(v)

    return res
