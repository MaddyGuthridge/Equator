import math

import consts

def prepString(input: str) -> list[str]:
    input = input.replace(' ', '')
    out = []
    
    word = ""
    for i in input:
        if i in consts.OPERATORS:
            if len(word):
                out.append(word)
                word = ""
            out.append(i)
        else:
            word += i
    
    if len(word):
        out.append(word)
    return out


