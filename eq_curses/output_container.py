
import curses
from lib.expression import Expression

from lib.tokens import Token, BadToken

from .display_exp import displayExpression, displayInputExpression, splitExpression, unravelInputTokens
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
                  margin: str, secondary_margin: str, exp: 'Expression | list[Token]', is_input:bool) -> int:

        # If no expression, just draw margin and return 1
        if exp is None:
            stdscr.addstr(row_start, col_start, margin, curses.color_pair(colours.PROMPT))
            stdscr.clrtoeol()
            return 1
        
        line_len = col_max - col_start - len(margin)

        # Split input into lines
        if is_input:
            exp, formatters = exp
        
        lines = splitExpression(line_len, exp)
        lines.reverse()
        
        # Whether we should add input formatters
        # 
        add_formatters = False
        
        if row_start < row_min:
            raise StopIteration("Row min")
        
        # Draw last line (output formatters) if they don't fit on a future line
        if is_input:
            if len("".join([t.stringifyOriginal() for t in lines[0]]))\
                + len(formatters) > line_len:
                    stdscr.addstr(row_start, col_start, secondary_margin,
                                curses.color_pair(colours.PROMPT))
                    stdscr.addstr(formatters, curses.color_pair(colours.FORMATTING))
                    stdscr.clrtoeol()
                    row_start -= 1
            else:
                # Need formatters inline
                add_formatters = True
        
        # Loop over each line
        for i, l in enumerate(lines):
            # If this goes outside the allowable range
            if row_start < row_min:
                raise StopIteration("Row min")
            
            # Draw margin
            m = margin if i == len(lines)-1 else secondary_margin
            stdscr.addstr(row_start, col_start, m, curses.color_pair(colours.PROMPT))
            
            displayExpression(row_start, col_start+len(secondary_margin), stdscr,
                              l, not add_formatters)
            
            if add_formatters:
                assert(is_input)
                stdscr.addstr(formatters, curses.color_pair(colours.FORMATTING))
                stdscr.clrtoeol()
                add_formatters = False
            
            # Decrease row to draw on
            row_start -= 1
        
        # Return number of lines drawn on
        return len(lines)
    
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
                mar_short = ' ' * (margin) + '|' + ' '
                out_mar = mar_short + ' '*2
                
                # Add line break between expressions
                curr_row -= self._drawLine(stdscr, curr_row, col_start, 
                                                row_start, cols, mar_short, mar_short, 
                                                None, False)
                
                # Temporary function for displaying output, this saves us
                # some effort since it can happen in two places, unless we use a
                # really long if statement
                def displayInput() -> int:
                    inp_tokens = unravelInputTokens(content.getInputTokens())
                    inp_mar = f" [{str(ci).rjust(mar_just)}] > "
                    return self._drawLine(stdscr, curr_row, col_start, 
                                          row_start, cols, inp_mar, mar_short, 
                                          inp_tokens, True)
                
                # Get output tokens
                # If this causes a crash catch the error
                try:
                    out_tokens = content.getOutputTokens()
                except Exception as e:
                    # This is the hackiest of hacks for displaying error info
                    # Fix this at some point
                    curr_row -= self._drawLine(stdscr, curr_row, col_start, 
                                               row_start, cols, out_mar, out_mar, 
                                               [BadToken(str(e), e)], False)
                    curr_row -= displayInput()
                    # Skip the remaining processing
                    continue
                    
                # Whether to do solution margins
                long_mar = False
                if len(out_tokens) > 1:
                    long_mar = True
                    # 2 extra spaces with solution margins
                    out_mar += ' '*2
                
                # For each solution
                for i, s in enumerate(reversed(out_tokens)):
                    i = len(out_tokens) - i
                    # Print evaluations then equations
                    for es in reversed(s):
                        for e in reversed(es):
                            curr_row -= self._drawLine(stdscr, curr_row, col_start, 
                                                    row_start, cols,
                                                    out_mar, out_mar, e, False)
                    # If we're doing big margins, generate a solution number
                    if long_mar:
                        sl_margin = mar_short + f" {{{i}}}:"
                        curr_row -= self._drawLine(stdscr, curr_row, col_start, 
                                                row_start, cols, sl_margin, sl_margin, 
                                                None, False)
                # Finally, display the input
                curr_row -= displayInput()
                
        except StopIteration:
            pass
