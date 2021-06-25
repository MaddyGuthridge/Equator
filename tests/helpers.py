
def simplifyEquationResults(results: list[dict]):
    ret = []
    for r in results:
        d = dict()
        for key, value in r.items():
            d[str(key)] = value
        ret.append(d)
    return ret
