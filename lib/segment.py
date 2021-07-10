from . import tokens
from . import consts
from . import operation

class Segment(tokens.Token):
    def __init__(self, contents: list):
        self._contents = contents
        # Don't even bother trying to parse if there's nothing there
        if len(self._contents) == 0:
            return
        self.parseBrackets()
        self.parseFunctions()
        self.parseOperators(['^'])
        self.parseOperators(['*', '/'])
        self.parseLeadingNegative()
        self.parseOperators(['+', '-'])
        self.parseOperators(['='])
    
    def stringify(self, num_type=None):
        if len(self._contents) == 0:
            return "0"
        elif len(self._contents) == 1:
            return self._contents[0].stringify(num_type)
        elif len(self._contents) != 3:
            raise ValueError("stringify: bad contents length")

        left  = self._contents[0]
        op    = self._contents[1]
        right = self._contents[2]
        
        l_str = left.stringify(num_type)
        if left.getOperatorPrecedence() <= self.getOperatorPrecedence():
            l_str = "(" + l_str + ")"
        
        r_str = right.stringify(num_type)
        if right.getOperatorPrecedence() <= self.getOperatorPrecedence():
            r_str = "(" + r_str + ")"
    
        return f"{l_str} {op.stringify(num_type)} {r_str}"
    
    def __str__(self):
        return self.stringify()
    
    def __repr__(self) -> str:
        return "Segment(" + repr(self._contents) + ")"
    
    def parseBrackets(self):
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
                    raise ValueError("Parse error: brackets don't match (too many closing)")
                elif bracket_depth == 0:
                    # End of the bracket pair
                    if not len(gather):
                        raise ValueError("Parse error: brackets don't contain contents")
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
            raise ValueError("Parse error: brackets don't match (too many opening)")

        self._contents = out

    def parseFunctions(self):
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
                    out.append(Function(self._contents[i], self._contents[i+1]))
            else:
                out.append(self._contents[i])
        
        if skip == 0:
            out.append(self._contents[-1])
        self._contents = out

    def parseLeadingNegative(self):
        # Expands '-x' to '(0 - x)'
        if len(self._contents) < 2:
            return
        
        if self._contents[0] == "-":
            assert len(self._contents) >= 2
            self._contents = [NegateFunction(self._contents[1])] + self._contents[2:]
        
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

    def parseOperators(self, operators: list):
        
        # Check for starting and ending with operators
        for op in operators:
            if op in (self._contents[0], self._contents[-1]):
                raise ValueError(f"Parse error: bad positioning of '{op}'")
        
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
                                out.append(NegateFunction(self._contents[i+1]))
                                skip += 1
                        # Check for leading negative
                        elif self._contents[i+1] == '-':
                            if len(self._contents) == i + 2:
                                raise ValueError("Parser Error: Expected value after leading negative")
                            neg = NegateFunction(self._contents[i+2])
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
                raise ValueError("Parser error: expected full expression after operator group")
            
            self._contents = out
        
    def evaluate(self):
        
        if len(self._contents) == 0:
            return 0.0
        
        if len(self._contents) == 1:
            return self._contents[0].evaluate()
            
        elif len(self._contents) == 3:
            op = self._contents[1]
            a = self._contents[0]
            b = self._contents[2]
            return operation.doOperation(op, a.evaluate(), b.evaluate())

        else:
            raise ValueError("Evaluation error: couldn't evaluate segment:\nBad content length\n"
                             + repr(self))

    def getOperatorPrecedence(self):
        if len(self._contents) in [0, 1]:
            return operation.NO_OPERATION_PRECEDENCE
        elif len(self._contents) == 3:
            if isinstance(self._contents[1], tokens.Operator):
                return operation.operatorPrecedence(self._contents[1])
            else:
                raise ValueError("Precedence error: failed to get operator for:\n"
                                 + repr(self))
        else:
            raise ValueError("Precedence error: Bad content length for\n"
                             + repr(self))

class Function(Segment):
    def __init__(self, type: tokens.Symbol, on: Segment):
        self._op = type
        self._on = on

    def __str__(self):
        return self.stringify(num_type=None)

    def __repr__(self) -> str:
        return f"Function({self._op}, {self._on})"

    def stringify(self, num_type):
        return f"{self._op.stringify()}({self._on.stringify()})"

    def evaluate(self):
        e = self._on.evaluate()
        return operation.doFunction(str(self._op), e)

    def getOperatorPrecedence(self):
        return operation.FUNCTION_OPERATOR_PRECEDENCE

class NegateFunction(Function):
    def __init__(self, on: Segment):
        self._op = consts.NEGATE
        self._on = on
    
    def __str__(self):
        return self.stringify(None)

    def stringify(self, num_type):
        return f"-{self._on.stringify(num_type)}"
