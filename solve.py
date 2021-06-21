import sympy as sym

import parse
import segment

def solve(inp: str):
    # Parse input
    prep = parse.prepString(inp)
    
    # For each expression, create a segment for it
    parsed = []
    for p in prep:
        seg = segment.Segment(p)
        parsed.append(seg.evaluate())

    return [sym.solve(parsed)]
