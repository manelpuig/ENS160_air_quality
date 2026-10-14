import unittest

from ens160_serial import ENS160Reading, parse_reading


class ParseReadingTests(unittest.TestCase):
    def test_parses_firmware_record(self):
        line = "12345,CH2,eCO2=487,TVOC=19,AQI=1,R0=101,R1=202,R2=303,R3=404"
        self.assertEqual(
            parse_reading(line),
            ENS160Reading(12345, 2, 487, 19, 1, 101, 202, 303, 404),
        )

    def test_ignores_status_output(self):
        self.assertIsNone(parse_reading("Initializing all sensors..."))

    def test_rejects_incomplete_record(self):
        self.assertIsNone(parse_reading("12345,CH2,eCO2=487,TVOC=19"))


if __name__ == "__main__":
    unittest.main()
