import sys

from colorama import Fore

from lib import main, consts

def printOutput(out):
    for i, e in enumerate(out):
        print(f"{Fore.RESET}[{i+1}]:{Fore.YELLOW} {e}")

if __name__ == "__main__":
    # No arguments, enter interpreter mode
    if len(sys.argv) == 1:
        print(f"{consts.NAME} (v{consts.VERSION})")
        print("Interpreter Mode")
        print("Press Ctrl+C to quit")
        try:
            while True:
                try:
                    inp = input(Fore.RESET + "calc > " + Fore.YELLOW)
                    command, expression = main.splitInput(inp)
                    printOutput(main.runInput(command, expression))
                    
                except Exception as e:
                    print(Fore.RED)
                    print(e)
                    #raise e
        except KeyboardInterrupt:
            print(Fore.RESET)
            exit()
    else:
        inp = ""
        for arg in sys.argv[1:]:
            inp += arg
        # Given command as arguments
        command, expression = main.splitInput(inp)
        
        printOutput(main.runInput(command, expression))

