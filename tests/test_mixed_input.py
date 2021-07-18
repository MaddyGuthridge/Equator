"""Check results when given mixed input are correct
"""

from .helpers import simpleEquate

def test_simple_substitution():
    """Ensure that substituting variables works correctly
    """
    assert simpleEquate("3*x; x=2") == [(["x=2"], ["6"])]

def test_simultaneous_substitution():
    """Ensure that the results of simultaneous equations can be substituted
    into expressions
    """
    assert simpleEquate("y + 3*x = 7; 2*y = x; y + x")\
        == [(["x=2", "y=1"], ["3"])]
