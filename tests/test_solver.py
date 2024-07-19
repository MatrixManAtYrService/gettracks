import sys
from dataclasses import dataclass
from logging import Logger
from textwrap import dedent, indent

from pytest import fixture, mark, raises
from solver.log import get_logger
from solver.solver import Directions, Grid, Location, Track, get_tracks


@fixture(scope="function")
def log() -> Logger:
    # the newline makes for prettier pytest log output
    # otherwise the log paths don't line up because the test names get in the way
    sys.stderr.write("\n")
    return get_logger(__file__, from_pytest=True)


def clean(pretty: str):
    "remove extra lines and indent whitespace"
    return dedent(pretty).strip()


def show(grid: str | Grid):
    if isinstance(grid, Grid):
        grid = str(grid)
    print(indent(grid, prefix="---------| "), file=sys.stderr)


def test_raise_if_not_rect(log: Logger):
    bad = clean("""
                xxxx
                yy
                xxxx
                """)
    log.info("Trying bad grid:")
    show(bad)
    with raises(ValueError) as e_info:
        Grid(bad)
    log.info(f"As expected, got exception: {e_info}")


@fixture
def abc(log: Logger) -> Grid:
    g = Grid(
        clean(
            """
            abcd
            efgh
            ijkl
            """
        )
    )
    show(g)
    return g


def test_left(abc: Grid, log: Logger):
    side = abc.left_side()
    log.info(f"got left side coordinates: {side}")
    assert side == set([(0, 0), (0, 1), (0, 2)])


def test_top(abc: Grid, log: Logger):
    top = set([(0, 0), (1, 0), (2, 0), (3, 0)])
    log.info(f"got top side coordinates: {top}")
    assert top == set([(0, 0), (1, 0), (2, 0), (3, 0)])


def test_move_right(abc: Grid, log: Logger):
    origin: Location = (0, 0)
    moved = abc.adjacent(location=origin, direction=Directions.across)
    log.info(f"one right from the origin: {moved}")
    assert moved == (1, 0)


def test_move_down(abc: Grid, log: Logger):
    origin: Location = (0, 0)
    moved = abc.adjacent(location=origin, direction=Directions.down)
    log.info(f"one down from the origin: {moved}")
    assert moved == (0, 1)


def test_diagonal(abc: Grid, log: Logger):
    origin: Location = (0, 0)
    moved = abc.adjacent(location=origin, direction=Directions.diagonal)
    log.info(f"one down and right from the origin: {moved}")
    assert moved == (1, 1)


def test_too_far(abc: Grid, log: Logger):
    def check(step: int, value: Location | None, expected: Location | None):
        log.info(f"moved {step} times to the right, got: {value}")
        assert value == expected

    origin: Location = (0, 0)
    value = abc.adjacent(location=origin, direction=Directions.across)
    check(1, value, (1, 0))
    value = abc.adjacent(location=value, direction=Directions.across)
    check(2, value, (2, 0))
    value = abc.adjacent(location=value, direction=Directions.across)
    check(3, value, (3, 0))
    value = abc.adjacent(location=value, direction=Directions.across)
    check(4, value, None)


def test_get_tracks(abc: Grid, log: Logger):
    tracks = get_tracks(abc, log=log)

    for track in [
        Track(letters="afk", coordinates=set([(0, 0), (1, 1), (2, 2)])),
        Track(letters="bgl", coordinates=set([(1, 0), (2, 1), (3, 2)])),
        Track(letters="abcd", coordinates=set([(0,0), (1, 0), (2, 0), (3, 0)])),
        Track(letters="dcba", coordinates=set([(0,0), (1, 0), (2, 0), (3, 0)]))
    ]:
        assert track in tracks



@dataclass
class Case:
    input: str
    words: list[str]
    output: str


@mark.parametrize(
    "case",
    [
        Case(
            input=dedent(
                """
                xxxfooxxx
                yyyyyyyyy
                """
            ),
            words=["foo"],
            output=dedent(
                """
                xxxFOOxxx
                yyyyyyyyy
                """
            ),
        )
    ],
)
def test_examples(case: Case):
    # I lost interest before getting this far
    pass
