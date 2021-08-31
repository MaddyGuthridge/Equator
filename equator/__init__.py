"""Equator

An advanced symbolic calculator built using SymPy

This project is licensed under the GNU General Public License v3.0

Author: Miguel Guthridge
"""

from .lib import equate, Expression
from .lib.tokens import Token, Operator, Number, Constant, Symbol, BadToken
from .lib.eq_except import *

from .equator import main
