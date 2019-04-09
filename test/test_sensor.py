import unittest

import numpy as np

from print_wiz.sensor import Sensor

class Test_Sensor(unittest.TestCase):
    """
    Tests for Sensor.

    """
    def test_init(self):
        """
        Test Sensor initialization.

        """
        sensor = Sensor()

        error_scale = 0.2
        sensor = Sensor(error_scale=0.2)
        self.assertEqual(sensor.error_scale, error_scale)

    def test_get_location(self):
        """
        Test Printer.get_location.

        """
        sensor = Sensor(error_scale=1.e-8)
        xyz_true = np.array([0., 2., 1.])
        sensor.sense_location(xyz_true)
        location = sensor.get_location()
        self.assertTrue(
            np.allclose(location, xyz_true),
            msg='location:%s\nxyz_true:%s' % (location, xyz_true)
        )

        sensor2 = Sensor()
        with self.assertRaises(RuntimeError):
            location = sensor2.get_location()

    def test_sense_location(self):
        """
        Test Printer.sense_location.

        """
        sensor = Sensor(error_scale=1.e-8)
        self.assertIsNone(sensor.xyz_location)

        xyz_true = np.array([0., 2., 1.])
        sensor.sense_location(xyz_true)
        self.assertTrue(np.allclose(sensor.xyz_location, xyz_true))

if __name__ == '__main__':
    unittest.main()
