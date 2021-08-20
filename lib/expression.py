"""Contains class definition for containing an expression and its output, in a
format so that it is easily printable with inner details accessible through
simple function calls to allow for formatting in external code.
"""

from . import tokens

from .parsedinput import ParsedInput

class Expression:
    def __init__(self, inp: str) -> None:
        """Create a new Equator Expression

        Args:
            inp (str): input to perform calculations on
        """
        self._parsed = ParsedInput(inp)

    def __repr__(self) -> str:
        return repr(self._parsed)

    def getInputStr(self) -> str:
        """Get a string equivalent to the original input

        Returns:
            str: original input
        """
        return self._parsed.stringifyOriginal()
    
    def getInputTokens(self) -> 'tuple[list[list[tokens.Token]], str]':
        """Return a list of tokens representing the original input

        Returns:
            tuple[
                list[                  : List of expressions
                    list[tokens.Token] : List of tokens for expression
                ]
                str                    : Output formatters as string
            ]
        """
        return self._parsed.getTokens()

    def getOutputStr(self) -> str:
        """Return the output as a string.
        
        Although this function is useful for quick calculations, it doesn't
        provide much flexibility for working with output.
        If the results need to be represented in a specific way, it may be
        better to use `getOutputList()` or `getOutputTokens()`

        Returns:
            str: output
        """
        return self._parsed.stringify()

    def getOutputList(self) -> 'list[tuple[list[str], list[str]]]':
        """Return the output as a collection, using the specification below

        Returns:
            list[             : List of sets of results
                tuple[        : A set of results
                    list[str] : The set of equation solutions
                    list[str] : The list of expression solutions
                ]
            ]
        """
        return self._parsed.resultSet()
    
    def getOutputTokens(self) -> 'list[tuple[list[list[tokens.Token]], list[list[tokens.Token]]]]':
        """Returns the same as `getOutputList()`, except each string is
        tokenised to allow for additional parsing of information on outputs

        Returns:
            list[                    : List of sets of results
                tuple[               : A set of results
                    list[            : The set of equation solutions
                        list[Tokens] : List of tokens representing an equation
                    ]
                    list[            : The list of expression solutions
                        list[Tokens] : List of tokens representing an expression
                    ]
                ]
            ]
        """
        return self._parsed.resultsTokens()
