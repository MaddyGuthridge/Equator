"""equator.py

Main entry point into the CLI for Equator

Parses command line arguments and runs commands accordingly

Author: Miguel Guthridge
"""

from eq_curses import curses_main

def main() -> int:
    curses_main()

if __name__ == "__main__":
    exit(main())
