"""Contains definition for abstract type EqObject,
with methods required by all types used in the equator hierarchy
"""

from .eval_options import EvalOptions

class EqObject: # pragma: no cover
    """Base object for most Equator types.
    Helps keep consistency in implementation
    """
    def __str__(self) -> str: # pragma: no cover
        return self.stringify(formatting=None)
    
    def stringify(self, formatting=None) -> str: # pragma: no cover
        """Convert object to string

        Args:
            formatting (OutputFormatter, optional): formatting options for
            output

        Returns:
            str: string representation
        """
        return NotImplemented
    
    def stringifyOriginal(self) -> str:
        """Returns string in original format (including spaces etc)

        Returns:
            str: original string
        """
        return self.stringify()

    def evaluate(self, options:'EvalOptions'=None):
        """Return evaluation of object
        """
        return NotImplemented
