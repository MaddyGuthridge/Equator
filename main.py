import sys

from pprint import pprint

import evaluate

def runInput(command, expression):
    if command == "ev":
        return evaluate.evaluate(expression)
    else:
        return None

if __name__ == "__main__":
    # No arguments, enter interpreter mode
    if len(sys.argv) == 1:
        print("PlaceHolderName")
        print("Interpreter Mode")
        print("Press Ctrl+C to quit")
        while True:
            try:
                inp = input("calc > ")
                command, expression = inp.split(' ', 1)
                pprint(runInput(command, expression))
            except Exception as e:
                print(e)
                #raise e
    else:
        input = ""
        for arg in sys.argv[1:]:
            input += arg
        # Given command as arguments
        command, expression = input.split(' ', 1)
        
        pprint(runInput(command, expression))
