# -'''- coding: utf-8 -'''-
import unittest

import numpy as np

from print_wiz.controller import SimpleEstimator

class Test_SimpleEstimator(unittest.TestCase):
    """
    Tests for SimpleEstimator.

    """
    def test_init(self):
        """
        Test SimpleEstimator initialization.

        """
        est = SimpleEstimator()
        self.assertIsNone(est.xyz_previous)

    def test_estimate(self):
        """
        Test SimpleEstimator.estimate.

        """
        xyzs_sensors = np.array([[1., 1., 1.],
                                 [0., 0., 0.]])
        xyz_estimate_expected = np.array([.5, .5, .5])

        est = SimpleEstimator()
        xyz_estimate = est.estimate(xyzs_sensors)
        self.assertTrue(np.allclose(xyz_estimate, xyz_estimate_expected))

if __name__ == '__main__':
    unittest.main()
