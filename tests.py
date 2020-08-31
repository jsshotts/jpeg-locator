import unittest
import util
import parsing
from math import isclose

class Tests(unittest.TestCase):

    def test_decimal_from_dms_0(self):
        lat = util.decimal_from_dms((42, 22, 48.7164), "N")
        lon = util.decimal_from_dms((108, 14, 14.1648), "W")
        correct = (42.380199, -108.237268)
        self.assertTrue(isclose(lat, correct[0]))
        self.assertTrue(isclose(lon, correct[1]))

    def test_decimal_from_dms_1(self):
        lat = util.decimal_from_dms((30, 45, 4.6332), "S")
        lon = util.decimal_from_dms((132, 42, 33.246), "E")
        correct = (-30.751287, 132.709235)
        self.assertTrue(isclose(lat, correct[0]))
        self.assertTrue(isclose(lon, correct[1]))

    def test_empty(self):
        with self.assertRaises(parsing.ParsingError) as e:
            parsing.parse_JPG("tests/empty.jpg")
            self.assertListEqual(e.message, EMPTY)
    
    def test_not_jpg(self):
        with self.assertRaises(parsing.ParsingError) as e:
            parsing.parse_JPG("tests/png.png")
            self.assertListEqual(e.message, NOT_JPG)

    def test_no_exif_0(self):
        with self.assertRaises(parsing.ParsingError) as e:
            parsing.parse_JPG("tests/jfif.jfif")
            self.assertListEqual(e.message, NO_EXIF)

    def test_no_exif_1(self):
        with self.assertRaises(parsing.ParsingError) as e:
            parsing.parse_JPG("tests/start.jpg")
            self.assertListEqual(e.message, NO_EXIF)

    def test_no_GPS_0(self):
        with self.assertRaises(parsing.ParsingError) as e:
            parsing.parse_JPG("tests/jfifAtStart.jpg")
            self.assertListEqual(e.message, NO_GPS)
    
    def test_no_GPS_1(self):
        with self.assertRaises(parsing.ParsingError) as e:
            parsing.parse_JPG("tests/exifnoGPS.jpg")
            self.assertListEqual(e.message, NO_GPS)
    
    def test_intel_byteorder(self):
        correct = {
            'GPSInfo': 4060, 
            'GPSLatitudeRef': 'N', 
            'GPSLatitude': [51.0, 10.6969, 0.0], 
            'GPSLongitudeRef': 'W', 
            'GPSLongitude': [1.0, 49.5984, 0.0]
        }
        JPG_Info = parsing.parse_JPG("tests/stonehenge.jpg")
        self.assertEqual(JPG_Info, correct)

    def test_motorola_byteorder(self):
        correct = {
            'GPSInfo': 2046, 
            'GPSLatitudeRef': 'N', 
            'GPSLatitude': [35.0, 16.0, 38.99], 
            'GPSLongitudeRef': 'W', 
            'GPSLongitude': [120.0, 39.0, 18.13]
        }
        JPG_Info = parsing.parse_JPG("tests/slo.jpg")
        self.assertEqual(JPG_Info, correct)

if __name__ == '__main__':
    unittest.main()