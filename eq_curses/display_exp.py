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
    else:
        # Default colour
        return curses.color_pair(colours.PROMPT)

def displayExpression(row: int, col: int, stdscr: 'curses._CursesWindow', 
                 exp: 'list[Token]', clear:bool=True):
    # Set to starting row/col
    stdscr.addstr(row, col, "")
    
    # For each token
    do_semicolon = False
    for t in exp:
        stdscr.addstr(t.stringifyOriginal(), getColourPair(t))
    
    if clear:
        stdscr.clrtoeol()

def unravelInputTokens(tokens: 'list[list[Token]]') -> 'list[Token]':
    ret = []
    add_semi = False
    for t in tokens[0]:
        if add_semi:
            ret.append(Token(";"))
        else:
            add_semi = True
        ret.extend(t)
    return ret, tokens[1]

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
    # Horrible hack to get a function to work
    displayExpression(row, col, stdscr, unravelInputTokens((expr, ""))[0], False)

    # Print formatter options
    stdscr.addstr(formatters, curses.color_pair(colours.FORMATTING))
    
    # Clear to end of line
    stdscr.clrtoeol()

def splitExpression(max_line_len: int, exp: 'list[Token]') -> 'list[list[Token]]':
    """Split expression so that lines don't go past the end of input
    """
    max_line_len -= 1
    split = []
    curr = []
    curr_len = 0
    for token in exp:
        if curr_len + len(token) > max_line_len and len(curr):
            split.append(curr)
            curr = []
            curr_len = 0
        # Break token up into smaller parts if it's too long by its self
        while len(token) > max_line_len:
            token_type = type(token)
            t_str = token.stringifyOriginal()
            # Add first part of token
            split.append([token_type(t_str[:max_line_len])])
            # Create trimmed token from remaining part of token
            token = token_type(t_str[max_line_len:])
        curr.append(token)
        curr_len += len(token)
    if len(curr):
        split.append(curr)
    return split
