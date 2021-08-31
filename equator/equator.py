"""equator.py

Main entry point into the CLI for Equator

Parses command line arguments and runs commands accordingly

Author: Miguel Guthridge
"""
import sys

from .eq_curses import curses_main
from .eq_json import json_main
from .lib import consts
from .lib import Expression
from .lib import EqExternalException, EqInternalException

def usage():
    print("\n".join([
        f"Equator v{consts.VERSION}",
        f"Author: {consts.AUTHOR}",
        f"",
        f"Commands:",
        f" * int: launch the interpreter",
        f" * json: launch the JSON interface",
        f" * ev [expression]: run a quick evaluation",
        f" * help: print this message",
        f"Default: launch the interpreter"
        f"",
        f"Licenced under the GNU General Public License V3",
        f"Refer to LICENCE.txt for a copy of this licence"
    ]))

def quick_equate(eq: list):
    eq = " ".join(eq)
    try:
        print(Expression(eq).getOutputStr())
    except EqExternalException as e:
        print(str(e))    

def main() -> int:
    argv = sys.argv[1:]
    try:
        if len(argv) == 0:
            curses_main()
        else:
            if argv[0] == "int":
                curses_main()
            elif argv[0] == "json":
                json_main()
            elif argv[0] == "ev":
                quick_equate(argv[1:])
            elif argv[0] == "help":
                usage()
            else:
                print(f"{argv[0]}: unrecognised command")
                usage()
        return 0
    except EqInternalException as e:
        print(f"Unfortunately, an error occurred, and Equator had to close")
        print(f"Type: {str(type(e))}")
        print(f"Details: {e.args}")
        print(f"Please create an issue on the project's GitHub page, including")
        print(f"your Equator version ({consts.VERSION}) and your input (if "
              "possible):")
        if e.input is not None: print(e.input)

