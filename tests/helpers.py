
def simplifyEq(results: list[dict]):
    ret = []
    for r in results:
        d = dict()
        for key, value in r.items():
            d[str(key)] = removeSpacing(value)
        ret.append(d)
    return ret

def removeSpacing(s: str):
    return s.replace(" ", "")

def simplifyExp(results: list[str]):
    return [removeSpacing(s) for s in results]
