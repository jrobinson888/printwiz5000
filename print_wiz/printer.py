# -'''- coding: utf-8 -'''-
import numpy as np
from prometheus_client import Gauge

class Printer(object):
    def __init__(self, xyz_initial):
        """
        Initialize Printer.

        Parameters
        -----------
        xyz_initial : ndarray
            <3,> array of the printer's starting location.

        """
        self.current_location = xyz_initial.copy()
        self.next_location = xyz_initial.copy()

        self.active = False
        self.error_rate = 0.2
        self.error_std = 0.5

        self._gauge_x = Gauge('printer_x', 'Printer x location')
        self._gauge_y = Gauge('printer_y', 'Printer y location')
        self._gauge_z = Gauge('printer_z', 'Printer z location')

    def activate(self):
        """
        Activate the printer.

        """
        self.active = True

    def deactivate(self):
        """
        Deactivate the printer.

        """
        self.active = False

    def move(self):
        """
        Move the printer to the next location if it is active.

        """
        if self.active:
            self.current_location = self.next_location.copy()
            self._gauge_x.set(self.current_location[0])
            self._gauge_y.set(self.current_location[1])
            self._gauge_z.set(self.current_location[2])
        else:
            print('Printer not active. Not moving.')

    def move_by(self, delta_xyz):
        """
        Set the location for the next move.

        Parameters
        -----------
        delta_xyz : ndarray
           <3,> array of the offset from the current location to set the next location.

        """
        index_error = 1 # y axis error
        if np.random.random() < self.error_rate:
            delta_xyz[index_error] += np.random.normal(scale=self.error_std)
        self.next_location += delta_xyz
        #TODO: check the next location is within bounds
