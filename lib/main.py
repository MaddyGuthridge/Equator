"""Contains front-facing equate function for quick result calculation
"""
from .expression import Expression

def equate(inp: str) -> 'list[list[str]]':
    """Evaluates and returns results in form:
    list (separate solutions) of lists (results)

    Args:
        inp (str): expression to evaluate
    
    Returns:
        list[list[str]]: result
    """
    return Expression(inp).getOutputList()
