
import consts
import tokens

def prepString(input: str) -> list[str]:
    input = input.replace(' ', '')
    words = []
    
    word = ""
    for i in input:
        if i in consts.OPERATORS:
            if len(word):
                words.append(word)
                word = ""
            words.append(i)
        else:
            word += i
    
    if len(word):
        words.append(word)
    
    # For each word, convert to the required type
    out = []
    for word in words:
        if word.isdecimal():
            out.append(tokens.Number(word))
        elif word in consts.OPERATORS:
            out.append(tokens.Operator(word))
        else:
            out.append(tokens.Symbol(word))
    
    return out
