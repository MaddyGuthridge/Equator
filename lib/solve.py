import sympy as sym

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
    
    if isinstance(res, list):
        return res
    else:
        return [res]
