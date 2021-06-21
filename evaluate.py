import parse
import segment

def evaluate(inp: str):
    prep = parse.prepString(inp)
    seg = segment.Segment(prep)
    return str(seg.evaluate()).replace("**", "^")
