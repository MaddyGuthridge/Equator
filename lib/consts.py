
import math
import decimal

NAME = "Equator"
VERSION = "0.5.0"

# Get 15 decimal places of precision - the max given by sympy
MAX_PRECISION = 14
FRACTION_DENOM_LIMITER = 1_000_000_000

# The minimum of abs(log_10(d)) for exponent to be presented using
# exponent notation
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

CONSTANTS = {
    "pi": decimal.Decimal(math.pi),
    "e": decimal.Decimal(math.e),
    "oo": decimal.Decimal("inf"),
    "inf": decimal.Decimal("inf")
}
