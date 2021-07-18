
import curses
from lib.expression import Expression

from .display_exp import displayExpression, displayInputExpression
from . import colours

class OutputContainer:
    def __init__(self) -> None:
        self._contents = []
    
    def __len__(self) -> int:
        return len(self._contents)
    
    def addOutput(self, expr: Expression):
        self._contents.insert(0, expr)
    
    def getInputHistory(self, index: int) -> str:
        """Returns input at index in history

        Args:
            index (int): index

        Raises:
            IndexError: too far back in history

        Returns:
            str: input from history
        """
        return self._contents[index].getInputStr()
    
    def _drawLine(self, stdscr: 'curses._CursesWindow', 
                  row_start: int, col_start: int, row_min: int, col_max: int,
                  margin: str, exp, is_input:bool) -> int:
        # Check within bounds
        if row_start < row_min:
            raise StopIteration("Row min")
        
        # Draw margin
        stdscr.addstr(row_start, col_start, margin, curses.color_pair(colours.PROMPT))
        
        col_start += len(margin)
        
        if exp is not None:
            if is_input:
                displayInputExpression(row_start, col_start, stdscr, exp)
            else:
                displayExpression(row_start, col_start, stdscr, exp)
        else:
            stdscr.clrtoeol()
        
        # Return number of rows drawn on
        # Currently, expressions can't span multiple lines
        return 1
    
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
        
        # Space to leave for numbers in margin
        mar_just = len(str(len(self._contents)))
        margin = mar_just + 4
        
        # When exception is raised we've run out of values
        try:
            # Print content in order of history
            for ci, content in enumerate(self._contents):
                ci = len(self._contents) - ci
                
                # Generate margin text for output
                out_mar = ' ' * (margin) + '|' + ' '
                
                # Add line break between expressions
                curr_row -= self._drawLine(stdscr, curr_row, col_start, 
                                                row_start, cols, out_mar, 
                                                None, False)
                
                # Get output tokens
                out_tokens = content.getOutputTokens()
                
                # Whether to do solution margins
                long_mar = False
                margin_s = out_mar
                if len(out_tokens) > 1:
                    long_mar = True
                    # 4 extra spaces with solution margins
                    out_mar += ' '*4
                else:
                    # 2 without
                    out_mar += ' '*2
                
                # For each solution
                for i, s in enumerate(reversed(out_tokens)):
                    i = len(out_tokens) - i
                    # Print evaluations then equations
                    for es in reversed(s):
                        for e in reversed(es):
                            curr_row -= self._drawLine(stdscr, curr_row, col_start, 
                                                    row_start, cols,
                                                    out_mar, [e], False)
                    # If we're doing big margins, generate a solution number
                    if long_mar:
                        sl_margin = margin_s + f" {{{i}}}:"
                        curr_row -= self._drawLine(stdscr, curr_row, col_start, 
                                                row_start, cols, sl_margin, 
                                                None, False)
                # Finally, display the input
                inp_mar = f" [{str(ci).rjust(mar_just)}] > "
                curr_row -= self._drawLine(stdscr, curr_row, col_start, row_start, cols, inp_mar, content, True)
                
        except StopIteration:
            pass
