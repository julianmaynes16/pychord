from fractions import Fraction
from typing import Union

from pychord.const import *


class Ratio:
    """
    Describes an abstract interval between two `Tone`s, the ratio between their frequencies
    """

    ratio: Union[float, Fraction]
    "Simple mathematical ratio between `Tone`s"

    def __init__(self, ratio: Union[float, Fraction]):
        self.ratio = ratio

    def __repr__(self):
        return f"<Ratio {self.ratio:.4f}>"

    def __str__(self):
        return self.__repr__()

    def __neg__(self) -> "Ratio":
        return self.inversion()

    def __add__(self, other: "Ratio"):
        if not isinstance(other, Ratio):
            return NotImplemented
        return Ratio(self.ratio * other.ratio)

    def __sub__(self, other: "Ratio"):
        if not isinstance(other, Ratio):
            return NotImplemented
        return Ratio(self.ratio / other.ratio)

    def __mul__(self, other: Union[int, float, Fraction]) -> "Ratio":
        if not isinstance(other, (int, float, Fraction)):
            return NotImplemented
        return Ratio(self.ratio**other)

    def __eq__(self, other: "Ratio"):
        return isinstance(other, Ratio) and self.ratio == other.ratio

    def __ne__(self, other: "Ratio"):
        return not isinstance(other, Ratio) or self.ratio != other.ratio

    def __ge__(self, other: "Ratio") -> bool:
        if not isinstance(other, (Ratio)):
            return NotImplemented
        return self.ratio >= other.ratio

    def __gt__(self, other: "Ratio") -> bool:
        if not isinstance(other, (Ratio)):
            return NotImplemented
        return self.ratio > other.ratio

    def __le__(self, other: "Ratio") -> bool:
        if not isinstance(other, (Ratio)):
            return NotImplemented
        return self.ratio <= other.ratio

    def __lt__(self, other: "Ratio") -> bool:
        if not isinstance(other, (Ratio)):
            return NotImplemented
        return self.ratio < other.ratio

    def compliment(self) -> "Ratio":
        """
        Compliment of `Ratio`, when added to the original `Ratio` will equal an octave
        """

        return -(self - OCTAVE_RATIO)

    def inversion(self) -> "Ratio":
        """
        Inversion of `Ratio` e.g. up a fifth becomes down a fifth
        """

        return Ratio(1.0 / self.ratio)


OCTAVE_RATIO = Ratio(Fraction(2, 1))
"Constant octave `Ratio` (2:1)"

SEMITONE_RATIO = Ratio(2 ** (1 / 12))
"Constant ratio for a 12TET semitone"
