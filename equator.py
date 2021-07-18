import sys
import curses

from lib import consts
from lib.expression import Expression
from display.output_container import OutputContainer
from display import display_exp, colours

def c_main(stdscr: 'curses._CursesWindow') -> int:
    
    # Set up colour pairs
    colours.init_colour(stdscr)
    
    stdscr.addstr(0, 0, f"{consts.NAME} (v{consts.VERSION})")
    stdscr.addstr(1, 0, f"by {consts.AUTHOR}")
    stdscr.addstr(2, 0, "Interpreter Mode")
    stdscr.addstr(3, 0, "Press Ctrl+C to quit")

    output = OutputContainer()
    
    # Input loop
    while True:
        prompt = f" [{len(output)+1}] > "
        inp_row = curses.LINES - 1
        inp_col = len(prompt)
        stdscr.addstr(inp_row, 0, prompt, curses.color_pair(colours.PROMPT))
        # Get char loop
        inp = ""
        cursor_pos = 0
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

            # Left arrow
            elif char == curses.KEY_LEFT or char == 452:
                if cursor_pos > 0:
                    cursor_pos -= 1
            
            # Right arrow
            elif char == curses.KEY_RIGHT or char == 454:
                if cursor_pos < len(inp):
                    cursor_pos += 1

            # Backspace
            elif char == curses.KEY_BACKSPACE or char in ['\x7f', '\x08']:
                if len(inp) == 0:
                    continue
                else:
                    inp = inp[:cursor_pos-1] + inp[cursor_pos:]
                cursor_pos -= 1
            
            elif char == '\n':
                break
            else:
                stdscr.addstr(4, 0, "Ignored: " + repr(char))
                stdscr.clrtoeol()
        
        # Got input
        output.addOutput(Expression(inp))
        output.redraw(stdscr, 4, 0, curses.LINES - 5, curses.COLS)

def main() -> int:
    try:
        return curses.wrapper(c_main)
    except KeyboardInterrupt:
        return 0

if __name__ == "__main__":
    exit(main())
