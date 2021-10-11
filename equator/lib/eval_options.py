"""Evaloptions module

Contains definition for evaluation options type, which specifies how Equator
should evaluate certain items, such as forcing number types to evaluate as
integers.
"""

class EvalOptions:
    """Options for how evaluations should be done
    """
    def __init__(self, previous_options:'EvalOptions'=None, number_as_rational:bool=None) -> None:
        """Create a set of evaluation options

        Args:
            number_as_rational (bool, optional): Whether to force SymPy rational
            types for evaluation. Defaults to None.
        """
        
        # FIXME: This is horribly yucky
        self.number_as_rational = number_as_rational\
            if number_as_rational is not None\
            else (previous_options.number_as_rational
                if previous_options is not None
                else False
                  )
