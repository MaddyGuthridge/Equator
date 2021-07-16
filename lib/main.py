import sys

#from pprint import pprint
from . import segment
from . import smart_equate
from . import parse
from .expression import Expression

def splitInput(expression):
    return expression.split(' ', 1)

def runInput(expression):
    return smart_equate.equate(expression)

def formatOutput(output, num_mode:str=None):
    output = parse.prepString(str(output).replace('**', '^'))
    s = segment.Segment(output)
    return s.stringify(num_mode)

def equate(inp: str) -> list:
    """Evaluates and returns results in form:
    list (separate solutions) of lists (results)

    Args:
        inp (str): expression to evaluate
    """
    return Expression(inp).getOutputList()
