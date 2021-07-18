"""Ensure that equations are solved correctly
"""

from .helpers import doOneSolutionEq, doManySolutionEq, equate

def test_basic():
    assert doOneSolutionEq("x - 1 = 0") == ["x=1"]
    assert doOneSolutionEq("x*2 = 2") == ["x=1"]

def test_complicated():
    assert doOneSolutionEq("3*x - 4 = 8*x - 3") == ["x=-1/5"]
    assert doOneSolutionEq("3/x + 2 = -4") == ["x=-1/2"]

def test_multiple_solutions():
    assert doManySolutionEq("x^2 = 4") == [["x=-2"], ["x=2"]]
    assert doManySolutionEq("6*x^2 + 2*x - 4 = 0") == [["x=-1"], ["x=2/3"]]
    
def test_simultaneous():
    assert doOneSolutionEq("2 * x = y; y + x = 6") == ["x=2", "y=4"]
    assert doOneSolutionEq("x + y + z = 12; 2*x - 3*y = 5*z; 4*y - x = 3*z")\
        == ["x=116/15", "y=44/15", "z=4/3"]

def test_no_solutions():
    assert equate("x - x = 2") == []
    assert equate("2 * x + 4 = 4 + 2*x") == []

def test_simultaneous_no_solutions():
    """Check that no solutions are given when there aren't any for simultaneous
    equations
    """
    assert equate("x + 2*y = 5; x/2 + y = 6") == []

def test_simultaneous_not_enough_constraints():
    """Check behaviour of displaying in terms of things when not enough
    constraints are placed on a system
    """
    assert doOneSolutionEq("y = x/2") == ["x=2*y"]
