from typing import Union

from pychord.ratio import Ratio


class Tone:
    """
    Describes an abstract musical frequency
    """

    frequency: Union[int, float]
    "The frequency of the tone in hertz"

    def __init__(self, frequency: Union[int, float]):
        self.frequency = frequency

    def __repr__(self) -> str:
        return f"<Tone ({self.frequency:.4f})>"

    def __str__(self) -> str:
        return self.__repr__()

    def __add__(self, other: Ratio) -> "Tone":
        if not isinstance(other, Ratio):
            return NotImplemented
        return self.transposed(other)

    def __sub__(self, other: Union[Ratio, "Tone"]) -> Union[Ratio, "Tone"]:
        if isinstance(other, Ratio):
            return self.transposed(-other)
        elif isinstance(other, Tone):
            return Ratio(self.frequency / other.frequency)

        return NotImplemented

    def __eq__(self, other: "Tone"):
        return isinstance(other, Tone) and self.frequency == other.frequency

    def __ne__(self, other: "Tone"):
        return not isinstance(other, Tone) or self.frequency != other.frequency

    def __ge__(self, other: "Tone") -> bool:
        if not isinstance(other, Tone):
            return NotImplemented
        return self.frequency >= other.frequency

    def __gt__(self, other: "Tone") -> bool:
        if not isinstance(other, Tone):
            return NotImplemented
        return self.frequency > other.frequency

    def __le__(self, other: "Tone") -> bool:
        if not isinstance(other, Tone):
            return NotImplemented
        return self.frequency <= other.frequency

    def __lt__(self, other: "Tone") -> bool:
        if not isinstance(other, Tone):
            return NotImplemented
        return self.frequency < other.frequency

    def transposed(self, ratio: "Ratio") -> "Tone":
        """
        Multiply the tone frequency by the input ratio
        """

        if not isinstance(ratio, Ratio):
            raise TypeError()
        return Tone(self.frequency * ratio.ratio)
