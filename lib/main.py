import sys

#from pprint import pprint
from . import consts
from . import evaluate
from . import solve

def splitInput(expression):
    return expression.split(' ', 1)

def runInput(command, expression):
    if command == "ev":
        return evaluate.evaluate(expression)
    if command == "eq":
        return solve.solve(expression)
    else:
        print("Unrecognised command")
        return None
