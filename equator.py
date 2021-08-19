"""Main interface for terminal interpreter interface

This code is exceptionally terrible. Please judge my code based on the other
sections, as this is just a hastily thrown-together wrapper that allows the
library to be tested in a console without it being a painful experience to do so

Author: Miguel Guthridge
"""

import curses

from lib import consts
from lib.expression import Expression
from display.output_container import OutputContainer
from display import display_exp, colours

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

def redrawFull(stdscr: 'curses._CursesWindow', output: OutputContainer, exp: str):
    """Redraw all contents on the screen (eg after window resize)

    Args:
        stdscr (curses._CursesWindow): curses window
    """
    stdscr.clear()
    lines, cols = stdscr.getmaxyx()
    drawHeader(stdscr)
    output.redraw(stdscr, 4, 0, lines - 5, cols)
    col = drawPrompt(stdscr, output)
    display_exp.displayInputExpression(lines-1, col, stdscr, Expression(exp))

def c_main(stdscr: 'curses._CursesWindow') -> int:
    
    # Set up colour pairs
    colours.init_colour(stdscr)

    output = OutputContainer()
    
    redrawFull(stdscr, output, "")
    
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
                display_exp.displayInputExpression(inp_row, inp_col, stdscr, Expression(inp))
                
                char = stdscr.get_wch(inp_row, inp_col + cursor_pos)
                
                # Keyboard interrupt
                if isinstance(char, str) and char in ['\x03']:
                    return 0
                
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


def main() -> int:
    try:
        return curses.wrapper(c_main)
    except KeyboardInterrupt:
        return 0

if __name__ == "__main__":
    exit(main())
