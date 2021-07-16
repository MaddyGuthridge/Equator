
from .eq_object import EqObject
from . import consts

class OutputFormatter(EqObject):
    """Contains formatting options for an input string
    """
    def __init__(self, inp:str=None) -> None:
        # Currently, we just take a decimal formatting option
        self._inp = inp
        if isinstance(self._inp, str):
            try:
                self._num_formatting = consts.NUM_FORMATTER_STRS[inp.strip(' ')]
            except KeyError:
                self._num_formatting = consts.NUMBER_FORMATTERS.SMART
        # No argument given for output formatter
        else:
            self._num_formatting = consts.NUMBER_FORMATTERS.SMART

    def getNumFormatting(self):
        """Return requested formatting method for numbers

        Returns:
            Enum NUMBER_FORMATTERS: Formatting method
        """
        return self._num_formatting

    def stringifyOriginal(self) -> str:
        return self._inp

    def givenArgs(self) -> bool:
        return self._inp is not None
