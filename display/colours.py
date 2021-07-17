"""Sets up and maintains colour schemes
"""

import curses

def init_colour(stdscr: 'curses._CursesWindow'):
    if not curses.can_change_color():
        stdscr.addstr("Terminal must support colour")
        exit(1)
    curses.use_default_colors()
    curses.start_color()
    
    curses.init_pair(NUMBER, curses.COLOR_WHITE, -1)
    curses.init_pair(OPERATOR, curses.COLOR_CYAN, -1)
    curses.init_pair(SYMBOL, curses.COLOR_MAGENTA, -1)
    curses.init_pair(CONSTANT, curses.COLOR_YELLOW, -1)
    curses.init_pair(FORMATTING, curses.COLOR_BLUE, -1)
    curses.init_pair(ERROR, curses.COLOR_RED, -1)

NUMBER      = 1
OPERATOR    = 2
SYMBOL      = 3
CONSTANT    = 4
FORMATTING  = 5
ERROR       = 6
