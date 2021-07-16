"""Contains helper functions for testing output

Author: Miguel Guthridge (hdsq@outlook.com.au)
"""

from ..lib.main import equate

def removeSpacing(s: str) -> str:
    """Remove spaces from a string"""
    return s.replace(" ", "")

def simplifyResults(results: 'list[list[str]]') -> 'list[list[str]]':
    """Simplify results of an expression by removing spacing for each result

    Args:
        results (list[list[str]]): output from equate function

    Returns:
        list[list[str]]: parsed output from equate function
    """
    out = [] 
    for r in results:
        eqs = [removeSpacing(s) for s in r[0]]
        evs = [removeSpacing(s) for s in r[1]]
        out.append((eqs, evs))
    return out

def oneSolutionExp(results: 'list[list[str]]') -> 'list[str]':
    """Return expressions only and assert there is one solution

    Args:
        results (list[list[str]]): results from equate function
    
    Returns:
        list[str]: List of expressions
    """
    results = simplifyResults(results)
    assert len(results) == 1
    return results[0][1]

def oneSolutionEq(results: 'list[list[str]]') -> 'list[str]':
    """Return equations only and assert there is only one solution

    Returns:
        list[str]: List of equations
    """
    results = simplifyResults(results)
    assert len(results) == 1
    return results[0][0]

def doOneSolutionExp(inp: str) -> 'list[str]':
    """Equate input then ensure only one solution set was given, then return
    expressions

    Returns:
        list[str]: expression results
    """
    return oneSolutionExp(equate(inp))

def doOneSolutionEq(inp: str) -> 'list[str]':
    """Equate input then ensure only one solution set was given, then return
    equations

    Returns:
        list[str]: equations results
    """
    return oneSolutionEq(equate(inp))
