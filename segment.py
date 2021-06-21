import consts
import operation

class Segment:
    def __init__(self, contents: list):
        self.contents = contents
        # Don't even bother trying to parse if there's nothing there
        if len(self.contents) == 0:
            return
        self.parseBrackets()
        self.parseFunctions()
        self.parseLeadingNegative()
        self.parseOperators(['^'])
        self.parseOperators(['*', '/'])
        self.parseOperators(['+', '-'])
    
    def __str__(self):
        out = "["
        for ele in self.contents:
            out += str(ele)
            out += " "
        out = out[:-1] + "]"
        return out
    
    def parseBrackets(self):
        # List after parse
        out = []
        # Items collected in bracket
        gather = []
        # How deep the brackets are
        bracket_depth = 0
        # For each element
        for ele in self.contents:
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

        self.contents = out

    def parseFunctions(self):
        if len(self.contents) < 2:
            return
        out = []
        skip = 0
        for i in range(len(self.contents) - 1):
            if skip > 0:
                skip -= 1
                continue
            # If it's a segment, this was bracketed
            if isinstance(self.contents[i + 1], Segment)\
                and isinstance(self.contents[i], str):
                    if not self.contents[i].isdecimal()\
                        and self.contents[i] not in consts.OPERATORS:
                            skip = 1
                            out.append(Function(self.contents[i], self.contents[i+1]))
                    else:
                        out.append(self.contents[i])
            else:
                out.append(self.contents[i])
        
        if skip == 0:
            out.append(self.contents[-1])
        self.contents = out

    def parseLeadingNegative(self):
        # Expands '-x' to '(0 - x)'
        if len(self.contents) < 2:
            return
        
        if self.contents[0] == "-":
            self.contents = ["0"] + self.contents
        
        out = [self.contents[0]]
        skip = 0
        for i in range(1, len(self.contents) - 1):
            if skip > 0:
                skip -= 1
                continue
            if self.contents[i-1] in consts.OPERATORS\
                and self.contents[i] == "-":
                    out.append(Segment(["-", self.contents[i+1]]))
                    skip = 1
            else:
                out.append(self.contents[i])
        
        if skip == 0:
            out.append(self.contents[-1])
        
        self.contents = out

    def parseOperators(self, operators: list[str]):
        
        # Check for starting and ending with operators
        for op in operators:
            if op in (self.contents[0], self.contents[-1]):
                raise ValueError(f"Parse error: bad positioning of '{op}'")
        
        found = True
        # Continue until we don't simplify any further
        while found:
            found = False
            out = []
            skip = 0
            # Prevent infinite recursion
            if len(self.contents) <= 3:
                continue
            for i in range(1, len(self.contents) - 1):
                if skip > 0:
                    skip -= 1
                    continue
                if self.contents[i] in operators and not found:
                    skip = 2
                    found = True
                    out.append(Segment(self.contents[i-1 : i+2]))
                else:
                    out.append(self.contents[i-1])

            if skip == 0:
                out.append(self.contents[-2])
                out.append(self.contents[-1])
            elif skip == 1:
                raise ValueError("Parser error: expected full expression after operator group")
            
            self.contents = out
        
    def evaluate(self):
        
        if len(self.contents) == 0:
            return 0.0
        
        if len(self.contents) == 1:
            e = self.contents[0]
            if isinstance(e, Segment):
                return e.evaluate()
            else:
                return float(e)
            
        elif len(self.contents) == 3:
            op = self.contents[1]
            a = self.contents[0]
            b = self.contents[2]
            
            if isinstance(a, Segment):
                a = a.evaluate()
            if isinstance(b, Segment):
                b = b.evaluate()
            
            return operation.doOperation(op, float(a), float(b))

        else:
            raise ValueError("Evaluation error: couldn't evaluate segment:\n"
                             + str(self))

class Function(Segment):
    def __init__(self, type: str, on: Segment):
        self._op = type
        self._on = on

    def __str__(self):
        return f"{self._op}({str(self._on)})"

    def evaluate(self):
        e = self._on.evaluate()
        return operation.doFunction(self._op, e)

