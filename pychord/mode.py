from pychord.interval import Interval
from pychord.note import Note
from pychord.scale import Scale


class Mode:
    """
    A musical `Mode` consisting of intervals making up an abstract tonicless `Scale`
    """

    intervals: list[Interval]
    "List of `Interval`'s from the tonic of the `Mode`"

    def __init__(self, intervals: list[Interval]):
        if not isinstance(intervals, list):
            raise TypeError()
        self.intervals = intervals

    def __repr__(self) -> str:
        return f"[Mode {' '.join([i.name() for i in self.intervals])}]"

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, other: "Mode"):
        return (
            isinstance(other, Mode)
            and len(self.intervals) == len(other.intervals)
            and all(x == y for x, y in zip(self.intervals, other.intervals))
        )

    def __ne__(self, other: "Mode"):
        return (
            not isinstance(other, Mode)
            or len(self.intervals) != len(other.intervals)
            or any(x != y for x, y in zip(self.intervals, other.intervals))
        )

    def __lshift__(self, other: int) -> "Mode":
        if not isinstance(other, int):
            return NotImplemented
        return self.shifted(other)

    def __rshift__(self, other: int) -> "Mode":
        if not isinstance(other, int):
            return NotImplemented
        return self.shifted(-other)

    def shifted(self, steps: int) -> "Mode":
        """
        Return a shifted version of this `Mode` essentially the same `Mode` but starting on step `steps`
        """

        if not isinstance(steps, int):
            raise TypeError()

        steps = steps % len(self.intervals)

        shifted_intervals = []

        for i in range(len(self.intervals)):
            shifted_intervals.append(
                (self.intervals[(i + steps) % len(self.intervals)] - self.intervals[steps]).decompound()
            )

        return Mode(shifted_intervals)

    def to_scale(self, tonic: Note) -> "Scale":
        return Scale([tonic + interval for interval in self.intervals])


IONIAN = Mode(
    [Interval("P1"), Interval("M2"), Interval("M3"), Interval("P4"), Interval("P5"), Interval("M6"), Interval("M7")]
)

DORIAN = IONIAN << 1
PHRYGIAN = IONIAN << 2
LYDIAN = IONIAN << 3
MIXOLYDIAN = IONIAN << 4
AEOLIAN = IONIAN << 5
LOCRIAN = IONIAN << 6
