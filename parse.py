
import consts
import tokens

def prepString(input: str) -> list[list[str]]:
    input = input.replace(' ', '')
    
    # Split into individual expressions (semicolon separated)
    exprs_str = input.split(";")
    exprs = []
    
    # Parse each expression
    for expr_s in exprs_str:
        words = []
        word = ""
        for i in expr_s:
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
        # Only append if it has contents        
        if len(out):
            exprs.append(out)
    
    return exprs
