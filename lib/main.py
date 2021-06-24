import sys

#from pprint import pprint
from . import segment
from . import evaluate
from . import solve
from . import parse

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

def formatOutput(output):
    output = parse.prepString(str(output).replace('**', '^'))
    s = segment.Segment(output)
    return str(s)
