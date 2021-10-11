"""Contains definition of ArgSet class
"""

from .eq_object import EqObject
from .eval_options import EvalOptions
from .eq_except import EqCommaError

class ArgSet(EqObject):
    """Represents a set of comma-separated arguments
    """
    def __init__(self, elements: 'list[Segment]') -> None:
        """Create an ArgSet object, representing comma-separated objects

        Args:
            elements (`list[Segment]`): list of elements in the set, where each
            is a segment
        """
        super().__init__()
        self._contents = elements

    def __len__(self) -> int:
        return len(self._contents)

    def __getitem__(self, index) -> 'Segment':
        return self._contents[index]
        
    def stringify(self, num_behaviour="num") -> str:
        return ', '.join([c.stringify(num_behaviour) for c in self._contents])

    def stringifyOriginal(self, num_behaviour="num") -> str:
        return ', '.join([c.stringifyOriginal(num_behaviour)
                          for c in self._contents])

    def __repr__(self) -> str:
        return self.stringify(None)

    def evaluate(self, options:EvalOptions=None):
        """Evaluate an ArgSet
        
        WARNING: since evaluation is impossible, this will raise an EqCommaError
        to signify that an ArgSet should be used within the context of a 
        function call
        """
        raise EqCommaError("Comma-separated values should only be used in the "
                           "context of function calls")

from .segment import Segment
