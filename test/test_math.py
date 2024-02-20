"""Test module for verifying logger functionality"""
import pytest
from pymccool.math import InclusiveRange, Point
from pymccool.logging import Logger, LoggerKwargs

logger = Logger(LoggerKwargs(
    app_name="Test Math",
))

def test_inclusive_range():
    """ Test the inclusive range Class """
    r = InclusiveRange(1, 10)
    assert r.start == 1
    assert r.stop == 10
    assert r.step == 1
    for i in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
        assert i in r
        assert r.__getattr__("__contains__")(i) # pylint: disable=unnecessary-dunder-call
    assert len(r) == 10
    assert repr(r) == "[1, 10]"
    assert str(r) == "[1, 10]"


@pytest.mark.parametrize(
    ("p1", "p2"),
    [
        (Point(1, 1), Point(2, 2)),
        (Point(0, 0), Point(0, 0)),
        (Point(-1, -1), Point(-2, -2)),
    ]
)
class TestPoint:
    """ Tests related to pymccool.math.Point"""

    def test_add(self, p1, p2):
        """ Test the add method """
        assert p1 + p2 == Point(p1.x + p2.x, p1.y + p2.y)

    def test_sub(self, p1, p2):
        """ Test the sub method """
        assert p1 - p2 == Point(p1.x - p2.x, p1.y - p2.y)

    def test_eq(self, p1, p2):
        """ Test the eq method """
        assert p1 == Point(p1.x,     p1.y    )
        assert p1 != Point(p1.x,     p1.y + 1)
        assert p2 == Point(p2.x,     p2.y    )
        assert p2 != Point(p2.x + 1, p2.y    )
        assert p1 != (p1.x, p1.y)
        assert p2 != (p2.x, p2.y)

    def test_lt(self, p1, p2):
        """ Test the lt method """
        assert p1 < Point(p1.x + 1, p1.y - 1)
        assert p1 < Point(p1.x, p1.y + 1)
        assert p1 < Point(p1.x + 1, p1.y + 1)
        assert p2 < Point(p2.x + 1, p2.y - 1)
        assert p2 < Point(p2.x, p2.y + 1)
        assert p2 < Point(p2.x + 1, p2.y + 1)

    def test_gt(self, p1, p2):
        """ Test the gt method """
        assert p1 > Point(p1.x - 1, p1.y + 1)
        assert p1 > Point(p1.x, p1.y - 1)
        assert p1 > Point(p1.x - 1, p1.y - 1)
        assert p2 > Point(p2.x - 1, p2.y + 1)
        assert p2 > Point(p2.x, p2.y - 1)
        assert p2 > Point(p2.x - 1, p2.y - 1)

    def test_hash(self, p1, p2):
        """ Test the hash method """
        d = {p1: p2}
        assert d[p1] == p2

    def test_str(self, p1, p2):
        """ Test the str method """
        assert str(p1) == f"({p1.x}, {p1.y})"
        assert str(p2) == f"({p2.x}, {p2.y})"

    def test_repr(self, p1, p2):
        """ Test the repr method """
        assert repr(p1) == f"({p1.x}, {p1.y})"
        assert repr(p2) == f"({p2.x}, {p2.y})"

    def test_up(self, p1, p2):
        """ Test the up method """
        assert p1.up() == Point(p1.x, p1.y - 1)
        assert p2.up() == Point(p2.x, p2.y - 1)

    def test_down(self, p1, p2):
        """ Test the down method """
        assert p1.down() == Point(p1.x, p1.y + 1)
        assert p2.down() == Point(p2.x, p2.y + 1)

    def test_left(self, p1, p2):
        """ Test the left method """
        assert p1.left() == Point(p1.x - 1, p1.y)
        assert p2.left() == Point(p2.x - 1, p2.y)

    def test_right(self, p1, p2):
        """ Test the right method """
        assert p1.right() == Point(p1.x + 1, p1.y)
        assert p2.right() == Point(p2.x + 1, p2.y)

    def test_manhatten(self, p1, p2):
        """ Test the manhatten method """
        assert p1.manhatten(p2) == abs(p1.x - p2.x) + abs(p1.y - p2.y)
