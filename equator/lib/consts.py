
import math
import decimal
from enum import Enum

NAME = "Equator"
VERSION = "1.2.0"
AUTHOR = "Miguel Guthridge"

# Get 15 decimal places of precision - the max given by sympy
MAX_PRECISION = 14
FRACTION_DENOM_LIMITER = 1_000_000_000

# The minimum of abs(log_10(d)) for exponent to be presented using
# exponent notation by default
MIN_EXP_LOG = 9

# Operators used to split string
OPERATORS = [
    "(",
    ")",
    "^",
    "*",
    "/",
    "+",
    "-",
    "="
    ]

NEGATE = "neg"

# Numeric constants
NUMERIC_CONSTANTS = {
    "pi": decimal.Decimal(math.pi),
    "e": decimal.Decimal(math.e),
    "oo": decimal.Decimal("inf"),
    "inf": decimal.Decimal("inf")
}

class NUMBER_FORMATTERS(Enum):
    """Formatting options for numbers
    """
    SMART = 1
    NUMBER = 2
    DECIMAL = 3
    SCIENTIFIC = 4

# Mappings between format strings and enum values
NUM_FORMATTER_STRS = {
    "num": NUMBER_FORMATTERS.NUMBER,
    "dec": NUMBER_FORMATTERS.DECIMAL,
    "sci": NUMBER_FORMATTERS.SCIENTIFIC
}
