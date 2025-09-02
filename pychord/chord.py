from typing import Union

from pychord.const import *
from pychord.interval import Interval, OCTAVE, MINOR_THIRD, DIMINISHED_FIFTH, MAJOR_SIXTH, SEMITONE, MAJOR_SECOND, PERFECT_FOURTH, PERFECT_FIFTH
from pychord.note import Note
from pychord.mode import IONIAN, AEOLIAN, MIXOLYDIAN, DORIAN
from pychord.scale import Scale


class Chord:
    """
    Describes a collection of `Note`s in 12TET
    """

    root: Note
    """
    Root `Note` of `Chord`
    """

    notes: list[Note]
    """
    `Note`s that make up the chord
    """

    def __init__(self, chord: Union[set[Note], str], 
                 root: Note = None):
        """
        `chord` can either be a set of `Note`s or a string definition
        `root` is the root `Note` of the set of `Note`s; only required for passing in a set
        """ 


        if isinstance(chord, set):
            self.root = root
            self.notes = chord

        elif isinstance(chord, str):
            # Verify root is valid if provided
            self.notes = []
            name = chord
            m = CHORD_NAME_RE.match(name)

            if m is None:
                raise ValueError(f"Invalid chord name '{name}'!")

            note = m.group(1)
            accidental = "" if m.group(2) == None else m.group(2)
            self.root = Note(f"{note}{accidental}") # Gbb

            quantity = int(m.group(4)) if m.group(4) != None else 5

            quality = m.group(3)
            

            if quality == None:
                if m.group(4) == None: # major chord
                    self.notes  = [self.root + IONIAN[i - 1] for i in range(1, quantity+2, 2)]
                elif m.group(4) == "5": # two note chord
                    self.notes = [self.root, self.root + PERFECT_FIFTH]
                else: # dominant chord
                    self.notes = [self.root + MIXOLYDIAN[i - 1] for i in range(1, quantity+2, 2)]
                scale = MIXOLYDIAN
            elif quality == "maj": # major chord
                self.notes = [self.root + IONIAN[i - 1] for i in range(1, quantity+2, 2)]
                scale = IONIAN
            elif quality == "m": # minor chord
                self.notes = [self.root + DORIAN[i - 1] for i in range(1, quantity+2, 2)]
                scale = DORIAN
            elif quality == "dim": # diminished chord
                self.notes = [self.root + DORIAN[i - 1] for i in range(1, quantity+2, 2)]
                self.notes[2] = self.notes[2] - SEMITONE
                scale = DORIAN
            elif quality == "aug": # augmented chord
                self.notes = [self.root + MIXOLYDIAN[m.group(3)][i - 1] for i in range(1, quantity+2, 2)]
                self.notes[2] = self.notes[2] + SEMITONE
                scale = MIXOLYDIAN

            if m.group(5) != None or m.group(5) == "": # alterations like #5 or bb7
                alteration_list = re.findall(ALTERATION_RE, m.group(5))
                for alteration in alteration_list:
                    alteration_m = ALTERATION_ACCIDENTAL_EXTENSION_RE.match(alteration)
                    self.notes[(int(alteration_m.group(2)) - 1) // 2] += Interval(ACCIDENTAL_NAME_TO_VALUE[alteration_m.group(1)])

            if m.group(6) != None: # suspend 
                #remove third
                self.notes.pop(1)
    
                #add 
                self.note += MAJOR_SECOND if m.group(6) == "sus2" else PERFECT_FOURTH

            if m.group(7) != None and m.group(7) != "": # add / omit
                adds_omits = re.findall(ADD_OMIT_RE, m.group(7))

                for add_omit in adds_omits:
                    if add_omit.startswith("add"):
                        scale_degree = int(add_omit.lstrip("add"))
                        self.notes.append(scale.to_scale(self.root)[scale_degree - 1]) # adds scale note 

                    elif add_omit.startswith("omit"):
                        scale_degree = int(add_omit.lstrip("omit"))
                        for i in range(len(self.notes)):
                            if self.notes[i] == scale.to_scale(self.root)[scale_degree - 1]: # removes scale note 
                                self.notes.pop(i)
            
            #sort
            self.notes.sort(key= lambda x: x.semitone)

            if m.group(8) != None: # slash note
                #adds preceding bass note before root
                self.notes.insert(0, Note(m.group(8)).preceding(self.root))

    def __repr__(self) -> str:
        return f"<Chord {' '.join([n.name() for n in self.notes])}>"

    def __str__(self) -> str:
        return self.__repr__()
    
    def __eq__(self, other: "Chord"):
        return (
            isinstance(other, Chord)
            and len(self.notes) == len(other.notes)
            and all(x == y for x,y in zip(self.notes, other.notes))
        )
    
    def __ne__(self, other: "Chord"):
        return (
            not isinstance(other, Chord)
            or len(self.notes) != len(other.notes)
            or any(x != y for x, y in zip(self.notes, other.notes))
        )

    def __getitem__(self, key: int) -> "Note":
        if not isinstance(key, int):
            return NotImplemented
        return self.notes[key]