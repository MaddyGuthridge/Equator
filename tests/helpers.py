"""Contains helper functions for testing output

Author: Miguel Guthridge
"""

def removeSpacing(s: str):
    """Remove spaces from a string"""
    return s.replace(" ", "")

def simplifyEq(results: list[dict]):
    """Returns list of dictionaries
    Each dict contains one set of unique results

    Args:
        results (list[dict]): results of equate function

    Returns:
        list[dict]: parsed results
    """
    ret = []
    for r in results:
        d = dict()
        for key, value in r.items():
            d[str(key)] = removeSpacing(value)
        ret.append(d)
    return ret

def simplifyExp(results: list[str]):
    """Simplify results of an expression by removing spacing for each result

    Args:
        results (list[str]): output from equate function

    Returns:
        list[str]: parsed output from equate function
    """
    return [removeSpacing(s) for s in results]
