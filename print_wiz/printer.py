import numpy as np

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
