""" A class for math operations and utilities """
from dataclasses import dataclass
from typing import Iterator
from typing_extensions import Self

class InclusiveRange:
    """ A class for inclusive ranges """
    def __init__(self, start: int, stop: int, step: int=1) -> Self:
        self._range = range(start, stop + 1, step)
        self._stop = stop

    def __getattr__(self, name: str):
        """ Passes calls through to underlying range object """
        return getattr(self._range, name)

    def __iter__(self) -> Iterator[int]:
        return self._range.__iter__()

    def __str__(self) -> str:
        return f"[{self._range.start}, {self._stop}]"

    def __repr__(self) -> str:
        return self.__str__()

    def __len__(self) -> int:
        return len(self._range)

    @property
    def start(self) -> int:
        """ The start of the range """
        return self._range.start
    @property
    def stop(self) -> int:
        """ The stop of the range """
        return self._stop
    @property
    def step(self) -> int:
        """ The step of the range """
        return self._range.step

    


@dataclass
class Point:
    """ A point in 2D space """
    x: int
    y: int

    def __add__(self, other: Self):
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other) -> Self:
        return Point(self.x - other.x, self.y - other.y)

    def __eq__(self, other: Self):
        if isinstance(other, Point):
            return self.x == other.x and self.y == other.y
        return False
    
    def __lt__(self, other: Self):
        if isinstance(other, Point):
            if self.x < other.x:
                return True
            elif self.x == other.x:
                if self.y < other.y:
                    return True
        return False
    
    def __le__(self, other: Self):
        if isinstance(other, Point):
            if self.x < other.x:
                return True
            elif self.x == other.x:
                if self.y <= other.y:
                    return True
        return False

    def __hash__(self):
        return hash((self.x, self.y))

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __repr__(self):
        return str(self)

    def up(self) -> Self:
        """ Get the point directly above this one """
        return self + Point(0, -1)

    def down(self) -> Self:
        """ Get the point directly below this one """
        return self + Point(0, 1)

    def left(self) -> Self:
        """ Get the point directly left of this one """
        return self + Point(-1, 0)

    def right(self) -> Self:
        """ Get the point directly right of this one """
        return self + Point(1, 0)

    def manhatten(self, other: Self) -> int:
        """ Get the manhatten distance between two points """
        return abs(self.x - other.x) + abs(self.y - other.y)
