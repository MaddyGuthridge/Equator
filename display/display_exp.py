"""Contains code required to display an input at a position on the screen
"""

import curses

from lib import tokens

from lib.expression import Expression

from . import colours

def getColourPair(token: 'tokens.Token') -> int:
    """Return curses colour code for a token

    Args:
        token (tokens.Token): token

    Returns:
        int: colour code
    """
    if isinstance(token, tokens.Constant):
        return curses.color_pair(colours.CONSTANT)
    elif isinstance(token, tokens.Number):
        return curses.color_pair(colours.NUMBER)
    elif isinstance(token, tokens.Operator):
        return curses.color_pair(colours.OPERATOR)
    elif isinstance(token, tokens.Symbol):
        return curses.color_pair(colours.SYMBOL)
    elif isinstance(token, tokens.BadToken):
        return curses.color_pair(colours.ERROR)

def displayInput(row: int, col: int, stdscr: 'curses._CursesWindow', exp: Expression):
    """Display input string of an expression on the screen

    Args:
        row (int): starting row
        col (int): starting col
        stdscr (curses._CursesWindow): curses screen
        exp (Expression): expression to print
    """
    # Set to starting row/col
    stdscr.addstr(row, col, "")
    
    expressions, formatters = exp.getInputTokens()
    
    # Sub expressions
    do_semicolon = False
    for s in expressions:
        if do_semicolon: stdscr.addstr(';')
        do_semicolon = True

        # For each token
        for t in s:
            stdscr.addstr(t.stringifyOriginal(), getColourPair(t))

    # Print formatter options
    stdscr.addstr(formatters, curses.color_pair(colours.FORMATTING))
    
    # Clear to end of line
    stdscr.clrtoeol()
