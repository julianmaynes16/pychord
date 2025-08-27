from typing import Union

from pychord.const import *
from pychord.interval import Interval, OCTAVE
from pychord.ratio import Ratio
from pychord.tone import Tone


class Note(Tone):
    """
    Describes a musical note as a `Tone` quantized to 12TET with A4 = 440Hz, where note 0 = C0
    """

    letter: str
    "The alphabet letter of the note, A-G"

    octave: int
    "The octave of the note, octaves start at C and end at B"

    accidental: int
    "The accidental semitone value, 0 for natural, 1 for sharp, -1 for flat, 2 for double sharp, -2 for double flat"

    semitone: int
    "The absolute semitone of the note starting at C0=0"

    def __init__(self, note: Union[int, str]):
        """
        `note` can either be a note name like "Ab4" "G2" "C#6" "F" or an integer number of semitones from C0
        """

        if not isinstance(note, (int, str)):
            raise TypeError()

        if isinstance(note, int):
            self.semitone = note
            self.octave = self.semitone // SEMITONES_PER_OCTAVE
            self.letter = NOTE_SEMITONE_TO_COMPONENTS[self.semitone % SEMITONES_PER_OCTAVE][0]
            self.accidental = NOTE_SEMITONE_TO_COMPONENTS[self.semitone % SEMITONES_PER_OCTAVE][1]

        elif isinstance(note, str):
            name = note
            m = NOTE_NAME_RE.match(name)

            if m is None:
                raise ValueError(f"Invalid note name '{name}'!")

            self.letter = m.group(1)
            self.accidental = ACCIDENTAL_NAME_TO_VALUE[m.group(2)]
            self.octave = int(m.group(3) or NOTE_DEFAULT_OCTAVE)

            c_based_note_semitone = NOTE_NAME_TO_SEMITONE[self.letter]

            self.semitone = c_based_note_semitone + self.accidental + SEMITONES_PER_OCTAVE * self.octave

        super().__init__(
            (
                Tone(C0_FREQUENCY)
                + Interval(self.semitone % SEMITONES_PER_OCTAVE)
                + (OCTAVE * (self.semitone // SEMITONES_PER_OCTAVE))
            ).frequency
        )

    def __repr__(self) -> str:
        return f"<Note {self.name()} ({self.frequency:.4f})>"

    def __str__(self) -> str:
        return self.__repr__()

    def __add__(self, other: Union[Interval, Ratio]):
        if not isinstance(other, (Ratio, Interval)):
            return NotImplemented
        return self.transposed(other)

    def __sub__(self, other: Union[Interval, Ratio, "Note"]):
        if isinstance(other, Ratio):
            return self.transposed(-other)
        elif isinstance(other, Note):
            return Interval(self.semitone - other.semitone)
        else:
            return NotImplemented

    def name(self) -> str:
        """
        Return name of note like Ab4 or G6
        """

        return f"{self.letter}{ACCIDENTAL_VALUE_TO_NAME[self.accidental]}{self.octave}"

    def transposed(self, interval: Union[Ratio, Interval]) -> Union["Note", "Tone"]:
        """
        Transpose a note by an `Interval` or `Ratio`. Passing in an `Interval` will return a `Note` while passing in a `Ratio` will return a `Tone`
        """

        if not isinstance(interval, (Ratio, Interval)):
            raise TypeError()

        if isinstance(interval, Interval):
            return Note(self.semitone + interval.semitones)
        else:
            return Tone(self.frequency) + interval

    def following(self, note: "Note") -> "Note":
        """
        Return the higher octave of this `Note` following `note`
        """

        i = (self - note).decompound()

        i = Interval("P8") if i.semitones == 0 else i

        return note + i

    def preceding(self, note: "Note") -> "Note":
        """
        Return the lower octave of this `Note` preceding `note`
        """

        i = -(note - self).decompound()

        i = -Interval("P8") if i.semitones == 0 else i

        return note + i
