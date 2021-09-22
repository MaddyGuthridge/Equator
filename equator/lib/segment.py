"""Class definitions for segments (collections of tokens in a parsable order)
These contain:
    - Definitions for managing order of operations
    - Definitions for stringifying collections of tokens
    - Definitions for evaluating segments

Author: Miguel Guthridge (hdsq@outlook.com.au)
"""

from . import tokens
from .eq_object import EqObject
from . import consts
from .output_formatter import OutputFormatter
from . import operation
from .eq_except import EqInternalException, EqParserException

class Segment(EqObject):
    """Hierarchy of tokens in a form that can be simplified and calculated with
    """
    def __init__(self, contents: list):
        self._contents: list[EqObject] = contents
        # There is always contents here as otherwise no segments are created
        self._parseBrackets()
        self._parseArgSets()
        self._parseFunctions()
        self._parseOperators(['^'])
        self._parseOperators(['*', '/'])
        self._parseLeadingNegative()
        self._parseOperators(['+', '-'])
        self._parseOperators(['='])
    
    def __getitem__(self, index) -> EqObject:
        return self._contents[index]
    
    def __len__(self) -> int:
        return len(self._contents)
    
    def stringify(self, str_opts: OutputFormatter):
        """Returns a string representing the segment
        Unlike str(obj), has options to control fancy stringification

        Args:
            str_opts (OutputFormatter): 
                Formatting options for stringification.

        Raises:
            ValueError: Error with user's input

        Returns:
            str: string representation of this segment
        """
        if len(self._contents) == 1:
            return self._contents[0].stringify(str_opts)
        elif len(self._contents) != 3: # pragma: no cover
            raise EqInternalException("stringify: bad contents length")

        left  = self._contents[0]
        op    = self._contents[1]
        right = self._contents[2]
        
        l_str = left.stringify(str_opts)
        if left.getOperatorPrecedence() <= self.getOperatorPrecedence():
            l_str = "(" + l_str + ")"
        
        r_str = right.stringify(str_opts)
        if right.getOperatorPrecedence() <= self.getOperatorPrecedence():
            r_str = "(" + r_str + ")"
    
        return f"{l_str} {op.stringify(str_opts)} {r_str}"
        
    def evaluate(self):
        """Returns the evaluation of this segment

        Raises:
            ValueError: Error when evaluating

        Returns:
            Operatable: The result of the conversion: stringify for proper result
                        in a meaningful format 
        """
        if len(self._contents) == 1:
            return self._contents[0].evaluate()
            
        elif len(self._contents) == 3:
            op = self._contents[1]
            a = self._contents[0]
            b = self._contents[2]
            return operation.doOperation(op, a.evaluate(), b.evaluate())

        else: # pragma: no cover
            raise EqInternalException("Evaluation error: couldn't evaluate segment:\n"
                             "Bad content length\n"
                             + repr(self))

    def getOperatorPrecedence(self):
        """Returns the precedence of the top operator of this segment, as per
        operationPrecedence function in operator.py

        Raises:
            ValueError: Middle contents isn't an operator
            ValueError: Contents are bad length - this shouldn't happen

        Returns:
            int: operator precedence
        """
        if len(self._contents) in [0, 1]:
            return operation.NO_OPERATION_PRECEDENCE
        elif len(self._contents) == 3:
            if isinstance(self._contents[1], tokens.Operator):
                return operation.operatorPrecedence(self._contents[1])
            else: # pragma: no cover
                raise EqInternalException("Precedence error: failed to get operator for:\n"
                                 + repr(self))
        else: # pragma: no cover
            raise EqInternalException("Precedence error: Bad content length for\n"
                             + repr(self))

    def __str__(self):
        return self.stringify()
    
    def __repr__(self) -> str:
        return "Segment(" + repr(self._contents) + ")"
    
    def _parseBrackets(self):
        # List after parse
        out = []
        # Items collected in bracket
        gather = []
        # How deep the brackets are
        bracket_depth = 0
        # For each element
        for ele in self._contents:
            # Opening bracket
            if ele == "(":
                bracket_depth += 1
                # If we are on the lowest bracket depth
                if bracket_depth > 1:
                    gather.append(ele)
            # Closing bracket 
            elif ele == ")":
                bracket_depth -= 1
                if bracket_depth < 0:
                    raise EqParserException("Brackets don't match (too many closing)")
                elif bracket_depth == 0:
                    # End of the bracket pair
                    if not len(gather):
                        raise EqParserException("Brackets don't contain contents")
                    out.append(Segment(gather))
                    gather = []
                else:
                    gather.append(ele)
            # Other elements
            else:
                if bracket_depth >= 1:
                    gather.append(ele)
                else:
                    out.append(ele)
        
        if bracket_depth != 0:
            raise EqParserException("Brackets don't match (too many opening)")

        self._contents = out

    def _parseArgSets(self):
        if len(self._contents) < 2:
            return
        
        args_list = []
        curr_tokens = []
        
        # Loop through each token
        for t in self._contents:
            # If it's a comma
            if isinstance(t, tokens.Operator) and t == ",":
                # Empty curr_tokens means syntax error
                if len(curr_tokens) == 0:
                    raise EqParserException("Expected value before token ','")
                # Current set of tokens is a single argument
                # Add it to the list
                args_list.append(curr_tokens)
                curr_tokens = []
            # Otherwise, just add it to the current list of tokens
            else:
                curr_tokens.append(t)
        
        # If there are items in args_list, we've got some comma-separated values
        if len(args_list):
            # Add on remaining tokens, make sure there are some, otherwise
            # Raise a parser error
            if not len(curr_tokens):
                raise EqParserException("Expected value after token ','")
            args_list.append(curr_tokens)
            
            # Now create a segment for each argument
            arg_segs = [Segment(items) for items in args_list]
            
            # Then make an ArgSet object and set that to the segment's contents
            self._contents = [ArgSet(arg_segs)]
        # Otherwise, there weren't any commas, so do nothing
        
    def _parseFunctions(self):
        if len(self._contents) < 2:
            return
        out = []
        skip = 0
        for i in range(len(self._contents) - 1):
            if skip > 0:
                skip -= 1
                continue
            # If it's a segment, this was bracketed
            if isinstance(self._contents[i + 1], Segment)\
                and isinstance(self._contents[i], tokens.Symbol):
                    skip = 1
                    # If the segment doesn't contain an argset (ie 1 argument), 
                    # make its contents into one to simplify argument types for
                    # functions
                    if not isinstance(self._contents[i+1][0], ArgSet):
                        self._contents[i+1] = ArgSet([self._contents[i+1]])
                    else:
                        self._contents[i+1] = self._contents[i+1][0]
                    out.append(detectFunction(self._contents[i], self._contents[i+1]))
            else:
                out.append(self._contents[i])
        
        if skip == 0:
            out.append(self._contents[-1])
        self._contents = out

    def _parseLeadingNegative(self):
        # Expands '-x' to 'neg(x)' to fix issues with unary operators
        if len(self._contents) < 2:
            return
        
        if self._contents[0] == "-":
            assert len(self._contents) >= 2
            self._contents = [NegateFunction( ArgSet([self._contents[1]]) )] + self._contents[2:]
        
        """out = [self.contents[0]]
        skip = 0
        for i in range(1, len(self.contents) - 1):
            if skip > 0:
                skip -= 1
                continue
            if self.contents[i-1] in consts.OPERATORS\
                and self.contents[i] == "-":
                    out.append(NegateFunction(self.contents[i+1]))
                    skip = 1
            else:
                out.append(self.contents[i])
        
        if skip == 0 and len(self.contents) > 1:
            out.append(self.contents[-1])
        
        self.contents = out"""

    def _parseOperators(self, operators: list):
        
        # Check for starting and ending with operators
        for op in operators:
            if op in (self._contents[0], self._contents[-1]):
                raise EqParserException(f"Bad positioning of '{op}'")
        
        found = True
        # Continue until we don't simplify any further
        while found:
            found = False
            out = []
            skip = 0
            # Prevent infinite recursion
            if len(self._contents) <= 3:
                continue
            for i in range(1, len(self._contents) - 1):
                if skip > 0:
                    skip -= 1
                    continue
                if isinstance(self._contents[i], tokens.Operator)\
                    and str(self._contents[i]) in operators and not found:
                        skip = 2
                        found = True
                        # Check for negative before lower signs
                        if isinstance(self._contents[i-1], tokens.Operator) \
                            and self._contents[i] == '-':
                                out.append(self._contents[i-1])
                                out.append(NegateFunction(ArgSet([self._contents[i+1]])))
                                #skip += 1
                        # Check for leading negative
                        elif self._contents[i+1] == '-':
                            if len(self._contents) == i + 2:
                                raise EqParserException("Expected value after leading negative")
                            neg = NegateFunction(ArgSet([self._contents[i+2]]))
                            skip += 1
                            out.append(Segment(self._contents[i-1 : i+1] + [neg]))
                        else:
                            # Create a segment of tokens surrounded by the operator
                            out.append(Segment(self._contents[i-1 : i+2]))
                else:
                    out.append(self._contents[i-1])

            if skip == 0:
                out.append(self._contents[-2])
                out.append(self._contents[-1])
            elif skip == 1:
                # Haven't been able to find a case that causes this
                # Is it already caught earlier?
                raise EqParserException("Expected full expression after operator group")
            
            self._contents = out

from .argset import ArgSet
from .functions import NegateFunction, detectFunction
