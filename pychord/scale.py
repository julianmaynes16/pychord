from pychord.note import Note
from pychord.interval import OCTAVE

class Scale:
    """
    A musical `Scale` consisting of a list of ordered `Note`s
    """

    notes: list[Note]
    "List of `Note`s in the `Scale`"

    def __init__(self, notes: list[Note]):
        if not isinstance(notes, list):
            raise TypeError()
        self.notes = notes

    def __repr__(self) -> str:
        return f"[Scale {' '.join([n.name() for n in self.notes])}]"

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, other: "Scale"):
        return (
            isinstance(other, Scale)
            and len(self.notes) == len(other.notes)
            and all(x == y for x, y in zip(self.notes, other.notes))
        )

    def __ne__(self, other: "Scale"):
        return (
            not isinstance(other, Scale)
            or len(self.notes) != len(other.notes)
            or any(x != y for x, y in zip(self.notes, other.notes))
        )

    def __lshift__(self, other: int) -> "Scale":
        if not isinstance(other, int):
            return NotImplemented
        return self.shifted(other)

    def __rshift__(self, other: int) -> "Scale":
        if not isinstance(other, int):
            return NotImplemented
        return self.shifted(-other)

    def __getitem__(self, index: int) -> Note:
        return self.notes[index % len(self.notes)] + OCTAVE * (index // len(self.notes))

    def shifted(self, steps: int) -> "Scale":
        """
        Return a shifted version of this `Scale` essentially the same `Scale` but starting on step `steps`
        """

        if not isinstance(steps, int):
            raise TypeError()

        shifted_notes = self.notes.copy()

        for _ in range(abs(steps)):
            if steps < 0:
                shifted_notes.insert(0, shifted_notes.pop(-1).preceding(shifted_notes[0]))
            elif steps > 0:
                shifted_notes.append(shifted_notes.pop(0).following(shifted_notes[-1]))

        return Scale(shifted_notes)

    def tonic(self) -> Note:
        """
        Return the tonic of the scale as a `Note`
        """
        return self.notes[0]
