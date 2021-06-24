import sys

#from pprint import pprint
from . import segment
from . import smart_equate
from . import parse

def splitInput(expression):
    return expression.split(' ', 1)

def runInput(expression):
    smart_equate.equate(expression)

def formatOutput(output):
    output = parse.prepString(str(output).replace('**', '^'))
    s = segment.Segment(output)
    return str(s)
