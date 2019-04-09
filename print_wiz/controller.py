import numpy as np

class Controller(object):
    def __init__(self):
        self.location_desired = None
        self.estimator = SimpleEstimator()
        self.sensors = []

        self.active = False

    @property
    def nsensors(self):
        return len(self.sensors)

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

    def estimate_current_location(self):
        xyzs_sensors = self.poll_sensors()
        return self.estimator.estimate(xyzs_sensors)

    def get_move_command(self):
        """
        Get the commanded delta to move to the desired location.

        Returns
        --------
        delta_xyz_move : ndarray
            <3,> array of the offset from the current location to the desired location.

        """
        if not self.active: # don't move if the controler is off
            return np.zeros(3)
        location_estimated = self.estimate_current_location()
        delta_xyz_move = location_estimated - self.location_desired
        return delta_xyz_move

    def poll_sensors(self):
        nsensors = self.nsensors
        xyzs_sensors = np.zeros((nsensors, 3))
        for i in range(nsensors):
            xyzs_sensors[i, :] = self.sensors[i].get_location()
        return xyzs_sensors

class SimpleEstimator(object):
    """
    Location estimator by the taking average from multiple sensors.

    """
    def estimate_current_location(self, xyzs_sensors):
        """
        Estimate the current location based on sesnor inputs.

        Parameters
        -----------
        xyzs_sensors : ndarray
            <n, 3> array of sensor locations inputs.

        Returns
        --------
        xyz_estimate : ndarray
            <3,> array of location estimate.

        """
        return np.average(xyzs_sensors)
