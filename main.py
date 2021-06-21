import sys

#from pprint import pprint
import consts
import evaluate
import solve

def runInput(command, expression):
    if command == "ev":
        return evaluate.evaluate(expression)
    if command == "eq":
        return solve.solve(expression)
    else:
        print("Unrecognised command")
        return None

if __name__ == "__main__":
    # No arguments, enter interpreter mode
    if len(sys.argv) == 1:
        print(f"{consts.NAME} (v{consts.VERSION})")
        print("Interpreter Mode")
        print("Press Ctrl+C to quit")
        try:
            while True:
                try:
                    inp = input("calc > ")
                    command, expression = inp.split(' ', 1)
                    print(runInput(command, expression))
                except ValueError as e:
                    print(e)
                    raise e
        except KeyboardInterrupt:
            exit()
    else:
        input = ""
        for arg in sys.argv[1:]:
            input += arg
        # Given command as arguments
        command, expression = input.split(' ', 1)
        
        print(runInput(command, expression))
