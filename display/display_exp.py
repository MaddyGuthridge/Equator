"""Contains code required to display an input at a position on the screen
"""

import curses

from lib import tokens

from lib.tokens import Token
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

def displayExpression(row: int, col: int, stdscr: 'curses._CursesWindow', 
                 exp: 'list[Token]', clear:bool=True):
    # Set to starting row/col
    stdscr.addstr(row, col, "")
    
    # Sub expressions
    do_semicolon = False
    for s in exp:
        if do_semicolon: stdscr.addstr(';')
        do_semicolon = True

        # For each token
        for t in s:
            stdscr.addstr(t.stringifyOriginal(), getColourPair(t))

def displayInputExpression(row: int, col: int, stdscr: 'curses._CursesWindow', 
                 exp: Expression):
    """Display input string of an expression on the screen

    Args:
        row (int): starting row
        col (int): starting col
        stdscr (curses._CursesWindow): curses screen
        exp (list[Token]): expression to print as list of tokens
        formatters (str): formatting options (appended to output)
    """
    expr, formatters = exp.getInputTokens()
    
    # Print expression
    displayExpression(row, col, stdscr, expr, False)

    # Print formatter options
    stdscr.addstr(formatters, curses.color_pair(colours.FORMATTING))
    
    # Clear to end of line
    stdscr.clrtoeol()
