import math
import sympy as sym

def doOperation(operator: str, a, b):
    if operator == '^':
        return a ** b
    elif operator == '*':
        return a * b
    elif operator == '/':
        return a / b
    elif operator == '+':
        return a + b
    elif operator == '-':
        return a - b
    elif operator == '=':
        return sym.Eq(a, b)

def doFunction(func: str, a):
    if func == "sqrt":
        return sym.sqrt(a)
    elif func == "sin":
        return sym.sin(a)
    elif func == "cos":
        return sym.cos(a)
    elif func == "tan":
        return sym.tan(a)
    elif func == "abs":
        return sym.Abs(a)
    elif func == "deg":
        return sym.deg(a)
    elif func == "rad":
        return sym.rad(a)

def getConstant(const: str):
    if const == "pi":
        return str(math.pi)
    else:
        return const
