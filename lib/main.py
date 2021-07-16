import sys

#from pprint import pprint
from . import segment
from . import parse
from .expression import Expression

def equate(inp: str) -> list:
    """Evaluates and returns results in form:
    list (separate solutions) of lists (results)

    Args:
        inp (str): expression to evaluate
    """
    return Expression(inp).getOutputList()
