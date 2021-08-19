"""equator.py

Main entry point into the CLI for Equator

Parses command line arguments and runs commands accordingly

Author: Miguel Guthridge
"""

from display import main_curses

def main() -> int:
    main_curses.curses_main()

if __name__ == "__main__":
    exit(main())
