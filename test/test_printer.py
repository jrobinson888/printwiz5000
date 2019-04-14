# -'''- coding: utf-8 -'''-
import unittest

import numpy as np

from print_wiz.printer import Printer

class Test_Printer(unittest.TestCase):
    """
    Tests for Printer.

    """
    def test_init(self):
        """
        Test Printer initialization.

        """
        xyz_initial = np.array([0., 0., 0.])
        printer = Printer(xyz_initial)
        self.assertTrue(np.allclose(printer.current_location, xyz_initial))
        self.assertTrue(np.allclose(printer.next_location, xyz_initial))
        self.assertFalse(printer.active)

    def test_activate(self):
        """
        Test Printer.activate.

        """
        xyz_initial = np.array([0., 0., 0.])
        printer = Printer(xyz_initial)
        self.assertFalse(printer.active)
        printer.activate()
        self.assertTrue(printer.active)

    def test_dectivate(self):
        """
        Test Printer.deactivate.

        """
        xyz_initial = np.array([0., 0., 0.])
        printer = Printer(xyz_initial)

        self.assertFalse(printer.active)

        printer.deactivate()
        self.assertFalse(printer.active)

        printer.activate()
        self.assertTrue(printer.active)

        printer.deactivate()
        self.assertFalse(printer.active)

    def test_move(self):
        """
        Test Printer.move.

        """
        xyz_initial = np.array([0., 0., 0.])
        printer = Printer(xyz_initial)

        next_location = np.array([1., 1., 0.])
        printer.next_location = next_location

        printer.move()
        self.assertFalse(
            np.allclose(printer.next_location, printer.current_location),
            msg='next:%s\ncurrent%s' % (printer.next_location, printer.current_location)
        )

        printer.activate()
        printer.move()
        self.assertTrue(
            np.allclose(printer.next_location, printer.current_location),
            msg='next:%s\ncurrent%s' % (printer.next_location, printer.current_location)
        )

    def test_move_by(self):
        """
        Test Printer.move_by.

        """
        xyz_initial = np.array([0., 0., 0.])
        printer = Printer(xyz_initial)

        delta_xyz = np.array([1., 1., 0.])
        printer.move_by(delta_xyz)
        self.assertFalse(
            np.allclose(printer.next_location, printer.current_location),
            msg='next:%s\ncurrent%s' % (printer.next_location, printer.current_location)
        )
        self.assertFalse(np.allclose(printer.next_location, xyz_initial))

        delta = printer.next_location - printer.current_location
        self.assertEqual(delta[0], delta_xyz[0])
        self.assertEqual(delta[2], delta_xyz[2])

if __name__ == '__main__':
    unittest.main()
