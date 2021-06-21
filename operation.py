import math

def doOperation(operator: str, a, b):
    if operator == "^":
        return a ** b
    elif operator == "*":
        return a * b
    elif operator == "/":
        return a / b
    elif operator == "+":
        return a + b
    elif operator == "-":
        return a - b

def doFunction(func: str, a):
    if func == "sqrt":
        return math.sqrt(a)
    elif func == "sin":
        return math.sin(a)
    elif func == "cos":
        return math.cos(a)
    elif func == "tan":
        return math.tan(a)
    elif func == "abs":
        return abs(a)
    elif func == "deg":
        return math.degrees(a)
    elif func == "rad":
        return math.radians(a)
