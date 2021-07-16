
import curses
from lib.expression import Expression

class OutputContainer:
    def __init__(self) -> None:
        self._contents = []
    
    def addOutput(self, expr: Expression):
        self._contents.insert(0, expr)
    
    def redraw(self, stdscr: 'curses._CursesWindow', 
               row_start: int, col_start: int, rows: int, cols: int):
        """Print output history onto screen

        Args:
            stdscr (curses._CursesWindow): window to draw onto
            row_start (int): starting row
            col_start (int): starting col
            rows (int): number of rows
            cols (int): number of cols
        """
        curr_row = row_start + rows - 1
        
        # Print content in order of history
        for content in self._contents:
            # Prevent printing back past start row
            if curr_row < row_start:
                break
            
            # Get output rows in order of printing
            print_order = [content.getInputStr()] + content.getOutputStr().split('\n')
            print_order.reverse()
            
            for p in print_order:
                # Prevent printing back past start row
                if curr_row < row_start:
                    break
                stdscr.addstr(curr_row, col_start, str(p))
                stdscr.clrtoeol()
                curr_row -= 1
