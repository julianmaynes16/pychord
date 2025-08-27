from typing import Union

from pychord.const import *
from pychord.interval import Interval, OCTAVE, MINOR_THIRD, DIMINISHED_FIFTH, MAJOR_SIXTH, SEMITONE, MAJOR_SECOND, PERFECT_FOURTH, PERFECT_FIFTH
from pychord.note import Note
from pychord.mode import IONIAN, AEOLIAN, MIXOLYDIAN, DORIAN, QUALITIES_TO_MODE


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
                 root: Note = None, 
                 enharmonic: str = None):
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
            print(f"{note}{accidental}")
            self.root = Note(f"{note}{accidental}") # Gbb
        
            #self.notes.append(self.root)
            
            # group3 and 4 = maj7

            quantity = int(m.group(4)) if m.group(4) != None else 5

            print(m.group(3))
            if m.group(3) == None:
                if m.group(4) == None:
                    self.notes  = [self.root + IONIAN[i - 1] for i in range(1, quantity+2, 2)]
                elif m.group(4) == "5":
                    self.notes = [self.root, self.root + PERFECT_FIFTH]
                else:
                    print( "Quantity: " + m.group(4))
                    self.notes = [self.root + MIXOLYDIAN[i - 1] for i in range(1, quantity+2, 2)]
            else:
                self.notes = [self.root + QUALITIES_TO_MODE[m.group(3)][i - 1] for i in range(1, quantity+2, 2)]



            if m.group(5) != None or m.group(5) == "":
                alteration_list = re.findall(ALTERATION_RE, m.group(5))
                for alteration in alteration_list:
                    alteration_m = ALTERATION_ACCIDENTAL_EXTENSION_RE.match(alteration)
                    self.notes[(int(alteration_m.group(2)) - 1) // 2] += Interval(ACCIDENTAL_NAME_TO_VALUE[alteration_m.group(1)])
            
            if len(self.notes) >= 4:
                seventh = self.notes[3]

            # sus
            if m.group(6) != None:
                #remove third
                self.notes.pop(1)
                self.note += MAJOR_SECOND if m.group(6) == "sus2" else PERFECT_FOURTH

            #add/omit
            if m.group(7) != None and m.group(7) != "":
                add_omit_list = re.findall(ADD_OMIT_RE, m.group(7))
                for add_omit in add_omit_list:
                    add_omit_m = ADD_OMIT_NOTE_RE.match(add_omit)
                    if add_omit_m.group(1) == "add":
                        # remove 7
                        for i in range(len(self.notes)):
                            if self.notes[i] == seventh:
                                self.notes.pop(i)
                        self.notes.append(QUALITIES_TO_MODE[m.group(3)].to_scale(self.root)[int(add_omit_m.group(2)) - 1])

                    elif add_omit_m.group(1) == "omit":
                        #omit
                        for i in range(len(self.notes)):
                            if self.notes[i] == QUALITIES_TO_MODE[m.group(3)].to_scale(self.root)[int(add_omit_m.group(2)) - 1]:
                                self.notes.pop(i)
            #sort list
            self.notes.sort(key= lambda x: x.semitone)

            # slash chord
            if m.group(8) != None:
                bass_note_m = BASS_NOTE_RE.match(m.group(8))
                self.notes.insert(0, Note(f"{bass_note_m.group(2)}{bass_note_m.group(3)}"))




            if enharmonic != None:
                for i in range(len(self.notes)):
                    note_enharmonic_m = CHORD_NAME_RE.match(self.notes[i].name())
                    print(note_enharmonic_m)
                    if (note_enharmonic_m is not None) and (
                        note_enharmonic_m.group(2) is not None) and (
                        note_enharmonic_m.group(2) != enharmonic):
    
                        self.notes[i] += Interval(ACCIDENTAL_NAME_TO_VALUE[note_enharmonic_m.group(2)])
                        self.notes[i].accidental = -1 if enharmonic == "b" else 1

            print(self.notes)




            # number 
            # majoe
           # self.note  =  # major7


            # Eb7/Bb
            # Bbdim11add4omit3/G#
            # Cmaj7
            # C#11
            # Fmaj7b5/G
            # Fmaj7add2omit3add4omit5/G##
            # G7#11
            # Gbb13#2b5#3b12b11##23##12sus4add2omit4/Gbb
            # Gbb13 chord move two up a half step
            # Amaj7
            # Fm7b5
            # Fdim7
            # Fdim7#5
            # B7
            # Cb6
            # Cb5
            # Cbb5
            # A5
            # Bm9
            # Cm11

if __name__ == "__main__":
    chord = Chord("B7")