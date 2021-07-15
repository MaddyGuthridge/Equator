import sys
import curses

from lib import consts, smart_equate

def c_main(stdscr: 'curses._CursesWindow') -> int:
    stdscr.addstr(0, 0, f"{consts.NAME} (v{consts.VERSION})")
    stdscr.addstr(1, 0, f"by {consts.AUTHOR}")
    stdscr.addstr(2, 0, "Interpreter Mode")
    stdscr.addstr(3, 0, "Press Ctrl+C to quit")
    # Input loop
    while True:
        prompt = "eq > "
        inp_row = curses.LINES - 1
        inp_col = len(prompt)
        stdscr.addstr(inp_row, 0, prompt)
        # Get char loop
        inp = ""
        cursor_pos = 0
        while True:
            stdscr.addstr(inp_row, inp_col, inp)
            stdscr.clrtoeol()
            char = stdscr.get_wch(inp_row, inp_col + cursor_pos)
            
            # Keyboard interrupt
            if isinstance(char, str) and char in ['\x03']:
                return 0
            
            # Insert character
            elif isinstance(char, str) and char.isprintable():
                inp = inp[:cursor_pos] + char + inp[cursor_pos:]
                cursor_pos += 1

            # Backspace
            elif char == curses.KEY_BACKSPACE or char in '\x7f\x08':
                if len(inp) == 0:
                    continue
                #elif cursor_pos > len(inp):
                #    inp = inp[:-1]
                else:
                    inp = inp[:cursor_pos-1] + inp[cursor_pos:]
                cursor_pos -= 1
            
            elif char == '\n':
                break
            else:
                stdscr.addstr(4, 0, "Ignored: " + repr(char))
                stdscr.clrtoeol()
        
        # Got input
        stdscr.addstr(4, 0, "Output: " + str(smart_equate.equate(inp)))
        stdscr.clrtoeol()

def main() -> int:
    curses.wrapper(c_main)

if __name__ == "__main__":
    exit(main())
