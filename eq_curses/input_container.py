"""Contains class for displaying input field
"""

import curses
from lib.expression import Expression

class InputContainer:
    def __init__(self) -> None:
        pass

    def redraw(self, stdscr: 'curses._CursesWindow', bottom_row: int) -> int:
        pass
