import re

NOTE_NAME = [
    "C",
    "D",
    "E",
    "F",
    "G",
    "A",
    "B",
]

NOTE_NAME_TO_SEMITONE = {
    "C": 0,
    "D": 2,
    "E": 4,
    "F": 5,
    "G": 7,
    "A": 9,
    "B": 11,
}

NOTE_SEMITONE_TO_COMPONENTS = {
    0: ("C", 0),
    1: ("C", 1),
    2: ("D", 0),
    3: ("D", 1),
    4: ("E", 0),
    5: ("F", 0),
    6: ("F", 1),
    7: ("G", 0),
    8: ("G", 1),
    9: ("A", 0),
    10: ("A", 1),
    11: ("B", 0),
}

ACCIDENTAL_NAME_TO_VALUE = {"##": 2, "#": 1, None: 0, "b": -1, "bb": -2}

ACCIDENTAL_VALUE_TO_NAME = {
    2: "##",
    1: "#",
    0: "",
    -1: "b",
    -2: "bb",
}

INTERVAL_NAME_TO_VALUE = {
    "P1": 0,
    "m2": 1,
    "M2": 2,
    "m3": 3,
    "M3": 4,
    "P4": 5,
    "A4": 6,
    "d5": 6,
    "P5": 7,
    "m6": 8,
    "M6": 9,
    "m7": 10,
    "M7": 11,
}

INTERVAL_VALUE_TO_COMPONENTS = {
    0: ("P", 1),
    1: ("m", 2),
    2: ("M", 2),
    3: ("m", 3),
    4: ("M", 3),
    5: ("P", 4),
    6: ("d", 5),
    7: ("P", 5),
    8: ("m", 6),
    9: ("M", 6),
    10: ("m", 7),
    11: ("M", 7),
}

NOTE_DEFAULT_OCTAVE: int = 4

SEMITONES_PER_OCTAVE: int = 12
# Gbb to F
NOTE_NAME_RE: re.Pattern = re.compile(r"^([CDEFGAB])(#{1,2}|b{1,2})?([0-9]+)?$")

INTERVAL_NAME_RE: re.Pattern = re.compile(r"^([mMdAP])([0-9]+)$")

CHORD_NAME_RE: re.Pattern = re.compile(
    r"^([CDEFGAB])(#{1,2}|b{1,2})?(maj|m|aug|dim)?([0-9]+)?((?:(?:#{1,2}|b{1,2})(?:[0-9]+))*)(sus2|sus4)?((?:(?:add|omit)(?:[0-9]+))*)(\/([CDEFGAB])(#{1,2}|b{1,2})?)?$"
)

ALTERATION_RE : re.Pattern = re.compile(
    r"(?:#{1,2}|b{1,2})[0-9]+"
)


ALTERATION_ACCIDENTAL_EXTENSION_RE : re.Pattern = re.compile(
    r"(#{1,2}|b{1,2})([0-9]+)"
)

ADD_OMIT_RE : re.Pattern = re.compile(
    r"((?:add|omit)[0-9]+)*"
)

ADD_OMIT_NOTE_RE : re.Pattern = re.compile(
    r"(add|omit)([0-9]+)"
)

BASS_NOTE_RE : re.Pattern = re.compile(
    r"(\/)([CDEFGAB])(#{1,2}|b{1,2})?"
)
C0_FREQUENCY: int = 16.351597831287375  # A = 440
"The frequency for C0 in A4=440Hz"
