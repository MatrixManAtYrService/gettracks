from dataclasses import dataclass
from typing import TypeAlias
from logging import Logger

from solver.log import get_logger


# (0,0): upper left corner

Location: TypeAlias = tuple[int, int]

Direction: TypeAlias = tuple[int, int]


def x(location: Location) -> int:
    return location[0]


def y(location: Location) -> int:
    return location[1]


def right(direction: Direction) -> int:
    return direction[0]


def down(direction: Direction) -> int:
    return direction[1]


class Directions:
    across: Direction = (1, 0)
    diagonal: Direction = (1, 1)
    other_diagonal: Direction = (1, -1)
    down: Direction = (0, 1)

class Grid:
    rows: list[str]

    def __init__(self, grid: str) -> None:
        self.rows = grid.split("\n")
        self.raise_if_not_rect()

    def in_bounds(self, location: Location) -> bool:
        if x(location) < 0 or y(location) < 0:
            return False
        if y(location) >= len(self.rows) or x(location) >= len(self.rows[0]):
            return False
        return True

    def raise_if_not_rect(self) -> None:
        lengths = set(map(len, self.rows))
        if len(lengths) != 1:
            raise ValueError(f"not a rectangle, got multiple row lengths: {lengths}")

    def left_side(self) -> set[Location]:
        return {(0, y) for y, _ in enumerate(self.rows)}

    def top_side(self) -> set[Location]:
        return {(x, 0) for x, _ in enumerate(self.rows[0])}

    def bottom_side(self) -> set[Location]:
        bottom = len(self.rows) - 1
        return {(x, bottom) for x, _ in enumerate(self.rows[0])}

    def adjacent(self, location: Location, direction: Direction) -> Location | None:
        new_location = (x(location) + right(direction)), (y(location) + down(direction))
        if self.in_bounds(new_location):
            return new_location

    def __str__(self) -> str:
        return "\n".join(self.rows)

    def __getitem__(self, key: Location):
        return self.rows[y(key)][x(key)]


@dataclass
class Track:
    letters: str
    coordinates: set[Location]

    def __eq__(self, other: "Track"):
        return self.coordinates == other.coordinates and self.letters == other.letters


def get_tracks(grid: Grid, log: Logger | None = None) -> list[Track]:
    if not log:
        log = get_logger(__file__)

    left = grid.left_side()
    top = grid.top_side()
    topleft = left.union(top)
    bottom = grid.bottom_side()
    bottomleft = left.union(bottom)

    tracks: list[Track] = []

    for direction, starts in {
        Directions.across: left,
        Directions.diagonal: topleft,
        Directions.down: top,
        Directions.other_diagonal: bottomleft
    }.items():
        for start in starts:
            letters = ""
            coordinates = set()
            current = start
            while True:
                letters += grid[current]
                coordinates.add(current)
                next = grid.adjacent(current, direction)
                track = Track(letters, coordinates)
                rtrack = Track("".join(reversed(letters)), coordinates)
                if next is None:
                    log.debug(str(track))
                    break
                current = next
            tracks.append(track)
            tracks.append(rtrack)
    return tracks
