
import math
import decimal

NAME = "Equator"
VERSION = "0.3.0"

# Get 15 decimal places of precision - the max given by sympy
MAX_PRECISION = 14
FRACTION_DENOM_LIMITER = 1_000_000_000

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
    "pi": decimal.Decimal(math.pi)
}
