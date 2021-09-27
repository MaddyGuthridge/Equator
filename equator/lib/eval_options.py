"""Evaloptions module

Contains definition for evaluation options type, which specifies how Equator
should evaluate certain items, such as forcing number types to evaluate as
integers.
"""

class EvalOptions:
    """Options for how evaluations should be done
    """
    def __init__(self, number_as_rational:bool=False) -> None:
        """Create a set of evaluation options

        Args:
            number_as_rational (bool, optional): Whether to force SymPy rational
            types for evaluation. Defaults to False.
        """
        self.number_as_rational = number_as_rational
