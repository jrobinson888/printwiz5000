import unittest

import numpy as np

from print_wiz.sensor import Sensor

class Test_Sensor(unittest.TestCase):
    """
    Tests for Sensor.

    """
    def test_init_01(self):
        """
        Test Sensor initialization.

        """
        name = 'test_init_01'
        sensor = Sensor(name)

    def test_init_01(self):
        """
        Test Sensor initialization.

        """
        name = 'test_init_02'
        error_scale = 0.2
        sensor = Sensor(name, error_scale=0.2)
        self.assertEqual(sensor.error_scale, error_scale)

    def test_get_location(self):
        """
        Test Printer.get_location.

        """
        name = 'test_get_location'
        sensor = Sensor(name, error_scale=1.e-8)
        sensor.set_active(True)

        xyz_true = np.array([0., 2., 1.])
        sensor.sense_location(xyz_true)

        location = sensor.get_location()
        self.assertTrue(
            np.allclose(location, xyz_true),
            msg='location:%s\nxyz_true:%s' % (location, xyz_true)
        )

    def test_get_location_fails_01(self):
        """
        Test Printer.get_location.

        """
        name = 'test_get_location_fails_01'
        sensor = Sensor(name)

        xyz_true = np.array([0., 2., 1.])
        sensor.set_active(True)
        sensor.sense_location(xyz_true)
        sensor.set_active(False)

        with self.assertRaises(RuntimeError):
            location = sensor.get_location()

    def test_get_location_fails_02(self):
        """
        Test Printer.get_location.

        """
        name = 'test_get_location_fails_02'
        sensor = Sensor(name)
        with self.assertRaises(RuntimeError):
            location = sensor.get_location()

    def test_sense_location(self):
        """
        Test Printer.sense_location.

        """
        name = 'test_sense_location'
        sensor = Sensor(name, error_scale=1.e-8)
        self.assertIsNone(sensor.xyz_location)
        sensor.set_active(True)

        xyz_true = np.array([0., 2., 1.])
        sensor.sense_location(xyz_true)
        self.assertTrue(np.allclose(sensor.xyz_location, xyz_true))

    def test_sense_location_fails(self):
        """
        Test Printer.sense_location.

        """
        name = 'test_sense_location_fails'
        xyz_true = np.array([0., 2., 1.])
        sensor = Sensor(name)
        with self.assertRaises(RuntimeError):
            location = sensor.sense_location(xyz_true)

if __name__ == '__main__':
    unittest.main()
