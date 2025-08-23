from fractions import Fraction
from typing import Union

from pychord.const import *
from pychord.ratio import Ratio, OCTAVE_RATIO, SEMITONE_RATIO


class Interval(Ratio):
    """
    Describes a musical interval as a ratio quantized to a 12TET semitone
    """

    semitones: int
    "Integer number of 12TET semitones"

    quality: str
    "Quality of `Interval`, 'M' for major, 'm' for minor, 'P' for perfect, 'A' for augmented, 'd' for diminished"

    quantity: int
    "Quantity of `Interval` as an integer number of major scale steps, for example M10 quality is 10"

    def __init__(self, interval: Union[int, str]):
        """
        `interval` can be either an interval name like "M5" "m2" "d5" "A2" "P5" or an integer number of semitones
        """

        assert isinstance(interval, (int, str))

        if isinstance(interval, int):
            self.semitones = interval

            abs_semitones = abs(self.semitones)

            self.quality = INTERVAL_VALUE_TO_COMPONENTS[abs_semitones % SEMITONES_PER_OCTAVE][0]

            self.quantity = INTERVAL_VALUE_TO_COMPONENTS[abs_semitones % SEMITONES_PER_OCTAVE][1] + (
                7 * (abs_semitones // SEMITONES_PER_OCTAVE)
            )

        elif isinstance(interval, str):
            m = INTERVAL_NAME_RE.match(interval)

            assert m is not None, f"Invalid 12TET interval name: '{interval}'!"

            self.quality = m.group(1)
            self.quantity = int(m.group(2))
            octave = 0
            offset_quantity = self.quantity

            if offset_quantity > 7:
                octave = (self.quantity - 1) // 7
                offset_quantity = ((self.quantity - 1) % 7) + 1

            offset_name = f"{self.quality}{offset_quantity}"

            if offset_name not in INTERVAL_NAME_TO_VALUE:
                raise ValueError(f"Invalid 12TET interval name: '{interval}'!")

            self.semitones = octave * SEMITONES_PER_OCTAVE + INTERVAL_NAME_TO_VALUE[offset_name]

        interval = (SEMITONE_RATIO * (abs(self.semitones) % SEMITONES_PER_OCTAVE)) + (
            OCTAVE_RATIO * (abs(self.semitones) // SEMITONES_PER_OCTAVE)
        )
        super().__init__((interval if self.semitones >= 0 else -interval).ratio)

    def __repr__(self) -> str:
        return f"[Interval {self.name()} ({self.ratio:.4f})]"

    def __str__(self) -> str:
        return self.__repr__()

    def __add__(self, other: Union["Interval", Ratio]) -> Union["Interval", Ratio]:
        if not isinstance(other, (Interval, Ratio)):
            return NotImplemented

        if isinstance(other, Interval):
            return Interval(self.semitones + other.semitones)
        elif isinstance(other, Ratio):
            return Ratio(self.ratio) + other

    def __sub__(self, other: Union["Interval", Ratio]) -> Union["Interval", Ratio]:
        if not isinstance(other, (Interval, Ratio)):
            return NotImplemented

        if isinstance(other, Interval):
            return Interval(self.semitones - other.semitones)
        elif isinstance(other, Ratio):
            return Ratio(self.ratio) - other

    def __mul__(self, other: Union[int, float, Fraction]) -> Union["Interval", Ratio]:
        if not isinstance(other, (int, float, Fraction)):
            return NotImplemented

        if isinstance(other, int):
            return Interval(self.semitones * other)
        else:
            return Ratio(self.ratio) * other

    def __neg__(self) -> "Ratio":
        """
        Inversion of `Interval` e.g. up an octave becomes down an octave
        """
        return Interval(-self.semitones)

    def compliment(self) -> "Interval":
        """
        Compliment of `Interval`, when added to the original interval will equal an octave
        """
        return -(self - Interval(SEMITONES_PER_OCTAVE))

    def name(self) -> str:
        """
        Return name of `Interval` like P5 or m7 or -M3
        """
        return f"{'-' if self.semitones < 0 else ''}{self.quality}{self.quantity}"

    def decompound(self) -> "Interval":
        """
        Returns the same `Interval` without any octave offset
        """
        return Interval(self.semitones % SEMITONES_PER_OCTAVE)


MINOR_SECOND = SEMITONE = Interval(1)

MAJOR_SECOND = WHOLETONE = Interval(2)

MINOR_THIRD = Interval(3)

MAJOR_THIRD = Interval(4)

PERFECT_FOURTH = Interval(5)

AUGMENTED_FOURTH = Interval("A4")

DIMINISHED_FIFTH = TRITONE = Interval("d5")

PERFECT_FIFTH = Interval(7)

MINOR_SIXTH = Interval(8)

MAJOR_SIXTH = Interval(9)

MINOR_SEVENTH = Interval(10)

MAJOR_SEVENTH = Interval(11)

OCTAVE = Interval(12)
