"""Contains definition for ParsedInput class. This represents a system of
equations and expressions that are evaluated and solved with respect to one
another.
"""

import sympy as sym

from . import tokens

from .eq_object import EqObject
from .output_formatter import OutputFormatter
from .subexpression import SubExpression
from .eval_options import EvalOptions

class ParsedInput(EqObject):
    """Contains parsed information about an input
     - List of TokenLists
     - List of output formatters
    """
    def __init__(self, inp: str) -> None:
        # Try getting output formatting options
        if "->" in inp:
            inp, output_mode = inp.split("->", 1)
            self._output_formatter = OutputFormatter(output_mode)
        else:
            self._output_formatter = OutputFormatter(None)

        # Split by individual subexpressions
        exps_str = inp.split(';')
        exps = [SubExpression(s) for s in exps_str]
        
        self._sub_exps = exps
        
        self._evaluation = None
    
    def __repr__(self) -> str:
        return repr(self._sub_exps) + " -> " + repr(self._output_formatter)
    
    def evaluate(self, options:EvalOptions=None) -> tuple:
        """Evaluate the input and return results

        Returns:
            tuple: 
                dict: equation results
                list: expression results
        """
        # Caching
        if self._evaluation is not None:
            return self._evaluation
        
        # Determine which are evaluations and equations
        evs = []
        eqs = []
        for e in self._sub_exps:
            a = e.evaluate(options)
            if a is not None:
                if e.isEquation():
                    eqs.append(a)
                else:
                    evs.append(a)
        
        # Solve the equations
        res = sym.solve(eqs)
        
        # Make sure we have a list of sets of solutions all the time
        # If it's empty
        if not len(res):
            res = [dict()]
        # Otherwise if there's only one set of answers
        elif not isinstance(res, list):
            res = [res]
        
        # Substitute equation results into evaluations, then simplify
        # Create one substitution for each set of results
        ev_subs = []
        for r in res:
            ev_subs.append([sym.simplify(sym.sympify(e).subs(r))\
                            for e in evs])
        
        ret = [(r, e) for r, e in zip(res, ev_subs)]
        self._evaluation = ret
        return self._evaluation
    
    def stringifyOriginal(self) -> str:
        """Return a string that should be equivalent to the original string

        Returns:
            str: recreation of original input
        """
        return ';'.join([exp.stringifyOriginal() for exp in self._sub_exps])\
            + self._output_formatter.stringifyOriginal()

    def getTokens(self) -> 'tuple[list[list[tokens.Token]], str]':
        return [e.getTokens() for e in self._sub_exps],\
            self._output_formatter.stringifyOriginal()

    def resultSet(self) -> 'list[tuple[list[str], list[str]]]':
        """Returns results of an evaluation in a format that can be parsed
        programmatically

        Returns:
            list[list[str]]: list of result sets (each set contains a list of 
                solutions, and a list of expression evaluations in a tuple)
        """
        evaluation = self.evaluate()
        
        out = []
        # Loop through each set of solutions
        for eqs, evs in evaluation:
            
            # Format equations
            new_eqs = []
            for key, value in eqs.items():
                s = SubExpression(
                    str(key) + "=" + str(value).replace("**", "^")
                )
                new_eqs.append(s.stringify(self._output_formatter))
            
            # Format evaluations
            new_evs = []
            for e in evs:
                s = SubExpression(str(e).replace("**", "^"))
                new_evs.append(s.stringify(self._output_formatter))
            
            # Add them both to the formatted set
            out.append((new_eqs, new_evs))

        # Check for no results
        if len(out[0][0]) == len(out[0][1]) == 0 and len(out) == 1:
            return []

        return out

    def resultsTokens(self) -> 'list[tuple[list[list[tokens.Token]], list[list[tokens.Token]]]]':
        """Generate results in tokenised form, useful for printing

        Returns:
            list: set of solutions
        """
        results = self.resultSet()
        
        out = []
        
        # Loop through results
        for r in results:
            # For each solution, create a bunch of tokens
            eqs = [SubExpression(eq).getTokens() for eq in r[0]]
            evs = [SubExpression(ev).getTokens() for ev in r[1]]
            out.append((eqs, evs))
        
        return out

    def stringify(self) -> str:
        """Return evaluation as a string

        Returns:
            str: results
        """
        evaluation = self.resultSet()
        
        out = []
        
        do_prepend = len(evaluation) > 1
        
        for i, (eqs, evs) in enumerate(evaluation):
            if do_prepend:
                out += [f'[{i+1}]:']
            for e in eqs:
                out += ['\t' + e] if do_prepend else [e]
            for e in evs:
                out += ['\t' + e] if do_prepend else [e]

        return '\n'.join(out)
