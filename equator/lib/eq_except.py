
class EqException(Exception):
    """Basic type for Equator exceptions
    """
    def __init__(self, *args: object) -> None:
        """Create an Equator exception
        
        NOTE: An input value for the exception can be given by calling the
        addInput() function on this exception.
        """
        super().__init__(*args)
        self.input = None
    
    def __str__(self) -> str: # pragma: no cover
        return str(type(self)) + ": " + super().__str__()
    
    def addInput(self, input: str): # pragma: no cover
        """Add the value that was entered into Equator in order to generate this
        exception

        Args:
            input (str): input string
        """
        self.input = input

class EqInternalException(EqException):
    """Exception for internal errors
    """

class EqExternalException(EqException):
    """Exception for external errors (errors where the user's input was
    invalid)
    """

class EqParserException(EqExternalException):
    """Exception when parsing an expression
    """

class EqTokeniseException(EqExternalException):
    """Exception when tokenising an expression
    """

class EqEvaluateException(EqExternalException):
    """Exception when evaluating an expression
    """

class EqOperatorException(EqEvaluateException):
    """Exception for when a function or operation isn't
    recognised
    """

class EqFunctionException(EqEvaluateException):
    """Exception for when a function cannot complete due
    to an error with its structure or input
    """

class EqFunctionNameException(EqFunctionException):
    """Exception for when a function name doesn't exist
    """

class EqFunctionArgumentException(EqFunctionException):
    """Exception for when a function is given the wrong type or number of
    arguments
    """

class EqFormatterError(EqExternalException):
    """Exception for when an output formatter is invalid
    """

class EqCommaError(EqEvaluateException):
    """Exception for when commas are used outside of a function
    """

class EqRangeError(EqOperatorException):
    """Exception for when a range operator is used outside of a function
    """
