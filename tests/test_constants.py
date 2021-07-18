"""Make sure that constants work correctly
"""

from .helpers import doOneSolutionExp

def test_pi():
    assert doOneSolutionExp("pi -> dec")[0].startswith("3.14")
    assert doOneSolutionExp("PI -> dec")[0].startswith("3.14")

def test_e():
    assert doOneSolutionExp("e -> dec")[0].startswith("2.718")
    assert doOneSolutionExp("E -> dec")[0].startswith("2.718")
