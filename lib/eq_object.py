"""Contains definition for abstract type EqObject,
with methods required by all types used in the equator hierarchy
"""

class EqObject: # pragma: no cover
    """Base object for most Equator types.
    Helps keep consistency in implementation
    """
    def stringify(self, num_behaviour="num") -> str:
        """Convert object to string

        Args:
            num_behaviour (str, optional): behaviour for number stringification.
                                           Should be propogated through
                                           subsequent stringify calls.
                                           Defaults to "num".

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

    def evaluate(self):
        """Return evaluation of object
        """
        return NotImplemented
