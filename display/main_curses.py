"""main_curses.py

Contains functions for running Equator as a curses module.

NOTE: This particular file's code quality is well... cursed.
The curses CLI is primarily designed to allow for quick testing of the library,
and as such is very much thrown together. If you want to see good code, I
highly recommend checking out other sections, in particular the `lib` module
which is where the actual magic happens.

Author: Miguel Guthridge
"""

import curses

from lib import consts
from lib.expression import Expression
from .output_container import OutputContainer
from . import display_exp, colours

def drawHeader(stdscr: 'curses._CursesWindow'):
    stdscr.addstr(0, 0, f"{consts.NAME} (v{consts.VERSION})")
    stdscr.addstr(1, 0, f"by {consts.AUTHOR}")
    stdscr.addstr(2, 0, "Interpreter Mode")
    stdscr.addstr(3, 0, "Press Ctrl+C to quit")

def drawPrompt(stdscr: 'curses._CursesWindow', output: OutputContainer) -> int:
    """Add prompt and return starting col for input
    """
    prompt = f" [{len(output)+1}] > "
    stdscr.addstr(stdscr.getmaxyx()[0] - 1, 0, prompt, curses.color_pair(colours.PROMPT))
    return len(prompt)

def drawInput(stdscr: 'curses._CursesWindow', inp_row: int, inp_col: int,
              exp: str, pos: int) -> int:
    """Draw input string in a way that doesn't make the program have a hissy fit

    Args:
        stdscr (curses._CursesWindow): screen to draw to
        inp_row (int): row to draw to
        inp_col (int): col to start draw on
        exp (str): expression to draw
        pos (int): Cursor position in exp
    
    Returns:
        int: relative cursor position
    """
    max_len = stdscr.getmaxyx()[1] - inp_col - 1
    
    # FIXME: Make this give some kind of error rather than just dying
    if (max_len < 15):
        raise KeyboardInterrupt()
    
    if len(exp) <= max_len:
        display_exp.displayInputExpression(inp_row, inp_col, stdscr, Expression(exp))
        return pos
    else:
        # Bounds of where we're trimming
        trim_low = len(exp)-max_len
        trim_hi = len(exp)
        
        # Whether we need to add trim ellipses on
        is_trim_low = False
        is_trim_hi = False
        
        # Adjust so that there's always a reasonable number of characters
        # to the left of the cursor
        # 10 chars + len("... ") = 14
        while trim_low+14 >= pos and trim_low > 0:
            trim_low -= 1
            trim_hi -= 1
        
        pos -= trim_low
        
        if trim_low != 0:
            trim_low += 4
            is_trim_low = True
        if trim_hi != len(exp):
            trim_hi -= 4
            is_trim_hi = True
        
        trimmed_exp = exp[trim_low:trim_hi]
        
        # Draw trim on left
        if is_trim_low:
            stdscr.addstr(inp_row, inp_col, "... ")
            inp_col += 4
        
        display_exp.displayInputExpression(inp_row, inp_col, stdscr, Expression(trimmed_exp))
        inp_col += len(trimmed_exp)
        
        if is_trim_hi:
            stdscr.addstr(inp_row, inp_col, " ...")
        return pos

def redrawFull(stdscr: 'curses._CursesWindow', output: OutputContainer, exp: str, pos: int):
    """Redraw all contents on the screen (eg after window resize)

    Args:
        stdscr (curses._CursesWindow): curses window
    """
    stdscr.clear()
    lines, cols = stdscr.getmaxyx()
    drawHeader(stdscr)
    output.redraw(stdscr, 4, 0, lines - 5, cols)
    col = drawPrompt(stdscr, output)
    drawInput(stdscr, lines-1, col, exp, pos)

def equator_curses(stdscr: 'curses._CursesWindow') -> int:
    
    # Set up colour pairs
    colours.init_colour(stdscr)

    output = OutputContainer()
    
    redrawFull(stdscr, output, "", 0)
    
    # Input loop
    while True:
        try:
            # Coordinates of input when user is typing
            inp_row = stdscr.getmaxyx()[0] - 1
            inp_col = drawPrompt(stdscr, output)
            # Get char loop
            inp = ""
            # Cached input for when returning to index -1
            inp_cache = ""
            # Position in output history (reset to -1 when changing text)
            history_pos = -1
            # Position of cursor in string: by default 1 char after last index
            # ie. default = len(inp)
            cursor_pos = 0
            
            # Redraw output
            output.redraw(stdscr, 4, 0, stdscr.getmaxyx()[0] - 5, stdscr.getmaxyx()[1])
            
            # Get characters until enter is pressed (break statement)
            while True:
                # Display input as we type
                draw_col = drawInput(stdscr, inp_row, inp_col, inp, cursor_pos)
                
                char = stdscr.get_wch(inp_row, inp_col + draw_col)
                
                # Keyboard interrupt
                if isinstance(char, str) and char in ['\x03']:
                    raise KeyboardInterrupt()
                
                # Insert character
                elif isinstance(char, str) and char.isprintable():
                    inp = inp[:cursor_pos] + char + inp[cursor_pos:]
                    cursor_pos += 1
                    # Entering text always sets to most recent index in history
                    history_pos = -1

                # Left arrow
                elif char == curses.KEY_LEFT or char == 452:
                    if cursor_pos > 0:
                        cursor_pos -= 1
                
                # Right arrow
                elif char == curses.KEY_RIGHT or char == 454:
                    if cursor_pos < len(inp):
                        cursor_pos += 1

                # Up arrow
                elif char == curses.KEY_UP or char == 450:
                    try:
                        t = output.getInputHistory(history_pos+1)
                    except IndexError:
                        continue
                    if history_pos == -1:
                        inp_cache = inp
                    inp = t
                    history_pos += 1
                    # Put cursor at end of input
                    cursor_pos = len(inp)
                
                # Down arrow
                elif char == curses.KEY_DOWN or char == 456:
                    if history_pos == -1:
                        continue
                    elif history_pos == 0:
                        inp = inp_cache
                    else:
                        inp = output.getInputHistory(history_pos-1)
                    history_pos -= 1
                    # Put cursor at end of input
                    cursor_pos = len(inp)

                # Backspace
                elif char == curses.KEY_BACKSPACE or char in ['\x7f', '\x08']:
                    if cursor_pos == 0:
                        continue
                    else:
                        inp = inp[:cursor_pos-1] + inp[cursor_pos:]
                    cursor_pos -= 1
                # Window resize
                elif char in [curses.KEY_RESIZE]:
                    redrawFull(stdscr, output, inp)
                    inp_row = stdscr.getmaxyx()[0] - 1
                # End line
                elif char == '\n':
                    break
                else:
                    stdscr.addstr(4, 0, "Ignored: " + repr(char))
                    stdscr.clrtoeol()
            
            # Got input
            output.addOutput(Expression(inp))
        
        except Exception as e:
            continue

def curses_main():
    try:
        return curses.wrapper(equator_curses)
    except KeyboardInterrupt:
        return 0
