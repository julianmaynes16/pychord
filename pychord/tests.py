import unittest

from pychord.const import *
from pychord.interval import *
from pychord.note import *
from pychord.ratio import *
from pychord.tone import *
from pychord.mode import *
from pychord.scale import *


class PyChordUnitTests(unittest.TestCase):
    def test_note_name_parsing(self):
        self.assertEqual(Note("A").octave, NOTE_DEFAULT_OCTAVE)

        self.assertAlmostEqual(Note("A4").frequency, 440, delta=0.001)
        self.assertAlmostEqual(Note("A5").frequency, 880, delta=0.001)

        self.assertAlmostEqual(Note("C4").frequency, 261.625, delta=0.001)

        self.assertAlmostEqual(Note("Cb4").frequency, Note("B3").frequency, delta=0.001)
        self.assertAlmostEqual(Note("B#2").frequency, Note("C3").frequency, delta=0.001)
        self.assertAlmostEqual(Note("C##1").frequency, Note("D1").frequency, delta=0.001)

        self.assertEqual(Note("C#1"), Note("Db1"))

        with self.assertRaises(ValueError):
            Note("Hb3")

        with self.assertRaises(ValueError):
            Note("A-3")

        with self.assertRaises(ValueError):
            Note("Abbb3")

        with self.assertRaises(ValueError):
            Note("G#b")

    def test_12tet_interval_name_parsing(self):
        self.assertEqual(Interval("P1").semitones, 0)
        self.assertEqual(Interval("m2").semitones, 1)
        self.assertEqual(Interval("M2").semitones, 2)
        self.assertEqual(Interval("m3").semitones, 3)
        self.assertEqual(Interval("M3").semitones, 4)
        self.assertEqual(Interval("P4").semitones, 5)
        self.assertEqual(Interval("A4").semitones, 6)
        self.assertEqual(Interval("d5").semitones, 6)
        self.assertEqual(Interval("P5").semitones, 7)
        self.assertEqual(Interval("m6").semitones, 8)
        self.assertEqual(Interval("M6").semitones, 9)
        self.assertEqual(Interval("m7").semitones, 10)
        self.assertEqual(Interval("M7").semitones, 11)
        self.assertEqual(Interval("P8").semitones, 12)
        self.assertEqual(Interval("m9").semitones, 13)
        self.assertEqual(Interval("M9").semitones, 14)
        self.assertEqual(Interval("P15").semitones, 24)

        self.assertEqual(Interval("M3").name(), "M3")
        self.assertEqual((-Interval("M3")).name(), "-M3")
        self.assertEqual(Interval("m10").name(), "m10")
        self.assertEqual(Interval("P15").name(), "P15")

    def test_12tet_interval_ratio(self):
        self.assertAlmostEqual(Interval("P1").ratio, 1, delta=0.001)
        self.assertAlmostEqual(Interval("m2").ratio, 1.0595, delta=0.001)
        self.assertAlmostEqual(Interval("M2").ratio, 1.1225, delta=0.001)
        self.assertAlmostEqual(Interval("m3").ratio, 1.1892, delta=0.001)
        self.assertAlmostEqual(Interval("M3").ratio, 1.2599, delta=0.001)
        self.assertAlmostEqual(Interval("P4").ratio, 1.3348, delta=0.001)
        self.assertAlmostEqual(Interval("d5").ratio, 1.4142, delta=0.001)
        self.assertAlmostEqual(Interval("P5").ratio, 1.4983, delta=0.001)
        self.assertAlmostEqual(Interval("m6").ratio, 1.5874, delta=0.001)
        self.assertAlmostEqual(Interval("M6").ratio, 1.6818, delta=0.001)
        self.assertAlmostEqual(Interval("m7").ratio, 1.7818, delta=0.001)
        self.assertAlmostEqual(Interval("M7").ratio, 1.8877, delta=0.001)
        self.assertAlmostEqual(Interval("P8").ratio, 2, delta=0.001)

    def test_12tet_interval_arithmetic(self):
        self.assertEqual(Interval(1), -Interval(-1))
        self.assertNotEqual(Interval(1), Interval(2))
        self.assertGreater(Interval(2), Interval(1))
        self.assertLess(Interval(1), Interval(2))
        self.assertEqual(Interval(5) + Interval(6), Interval(11))
        self.assertEqual(Interval(5) - Interval(6), Interval(-1))
        self.assertEqual(Interval(5) * 2, Interval(10))

        self.assertEqual(Note(12) + Interval(12), Note(24))
        self.assertEqual(Note(12) - Interval(12), Note(0))

        self.assertEqual(Note("A4") + Interval("P8"), Note("A5"))
        self.assertEqual(Note("A4") + Interval("P5"), Note("E5"))
        self.assertEqual(Note("A4") - Interval("m3"), Note("F#4"))
        self.assertEqual(Note("C0") - Interval("P1"), Note("C0"))
        self.assertEqual(Note("C0") + Interval("P1"), Note("C0"))
        self.assertEqual(
            Note("C0") + (Interval("m2") + Interval("m2")),
            (Note("C0") + Interval("m2")) + Interval("m2"),
        )

    def test_inversions(self):
        self.assertEqual((-Interval(5)).name(), "-P4")
        self.assertAlmostEqual((-Interval(5)).ratio, 1 / 1.3348, delta=0.001)

        self.assertEqual(Interval("P5").compliment(), Interval("P4"))
        self.assertEqual(Interval("m3").compliment(), Interval("M6"))
        self.assertEqual((-Interval("m3")).compliment(), Interval("m10"))
        self.assertEqual(Interval("P1").compliment(), Interval("P8"))
        self.assertEqual(Interval("P8").compliment(), Interval("P1"))

        self.assertEqual((-Ratio(1.5)), Ratio(1 / 1.5))
        self.assertEqual(Ratio(1.25).compliment(), Ratio(1.6))

    def test_modes_scales(self):
        self.assertEqual(
            IONIAN.to_scale(Note("C")),
            Scale([Note("C"), Note("D"), Note("E"), Note("F"), Note("G"), Note("A"), Note("B")]),
        )
        self.assertEqual(
            AEOLIAN.to_scale(Note("C")),
            Scale([Note("C"), Note("D"), Note("Eb"), Note("F"), Note("G"), Note("Ab"), Note("Bb")]),
        )
        self.assertEqual(
            IONIAN << 1,
            Mode(
                [
                    Interval("P1"),
                    Interval("M2"),
                    Interval("m3"),
                    Interval("P4"),
                    Interval("P5"),
                    Interval("M6"),
                    Interval("m7"),
                ]
            ),
        )

        self.assertEqual(IONIAN, IONIAN)
        self.assertEqual(IONIAN, PHRYGIAN >> 2)
        self.assertNotEqual(IONIAN, DORIAN)

        self.assertEqual(AEOLIAN.to_scale(Note("A3")), IONIAN.to_scale(Note("C")) >> 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
