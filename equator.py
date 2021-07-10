import sys

from colorama import Fore

from lib import main, consts, smart_equate

def printOutput(out):
    for i, e in enumerate(out):
        print(f"{Fore.RESET}[{i+1}]:{Fore.YELLOW} {e}")

if __name__ == "__main__":
    # No arguments, enter interpreter mode
    if len(sys.argv) == 1:
        print(f"{consts.NAME} (v{consts.VERSION})")
        print(f"by {consts.AUTHOR}")
        print("Interpreter Mode")
        print("Press Ctrl+C to quit")
        try:
            counter = 1
            while True:
                try:
                    inp = input(Fore.RESET + f"eq {Fore.YELLOW}[{counter}]{Fore.WHITE} > " + Fore.YELLOW)
                    printOutput(smart_equate.equate(inp))
                    counter += 1
                    
                except Exception as e:
                    print(Fore.RED, end='')
                    print(e)
                    #raise e
        except KeyboardInterrupt:
            print(Fore.RESET)
            exit()
    else:
        inp = ""
        for arg in sys.argv[1:]:
            inp += arg
        
        printOutput(smart_equate.equate(inp))
