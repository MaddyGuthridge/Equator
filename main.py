import sys

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
                print(runInput(command, expression))
            except Exception as e:
                print(e)
                #raise e
    else:
        # Given command as arguments
        command = sys.argv[1]
        # Join into expression
        expression = ""
        for arg in sys.argv[2:]:
            expression += arg
        print(runInput(command, expression))
