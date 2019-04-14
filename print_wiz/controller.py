# -'''- coding: utf-8 -'''-
import numpy as np
from prometheus_client import Gauge

class Controller(object):
    """
    Controller that recieves sensor information and gives move commands.

    """
    def __init__(self, sensor_manager, tol_target=0.05):
        """
        Initialize Controller.

        Parameters
        -----------
        tol_target : float, optional, defai;t : 0.05
            Tolerance in absolute distance at which the target is considered reached.

        """
        self.sensor_manager = sensor_manager
        self.tol_target = tol_target

        self.target_location = None
        self.target_path = None
        self.index = None
        self.index_max = None

        self.estimator = SimpleEstimator()

        self._gauge_x_est = Gauge('controller_estimated_x', 'Controller estimated x location')
        self._gauge_y_est = Gauge('controller_estimated_y', 'Controller estimated y location')
        self._gauge_z_est = Gauge('controller_estimated_z', 'Controller estimated z location')
        self._gauge_x_tar = Gauge('controller_target_x', 'Controller target x location')
        self._gauge_y_tar = Gauge('controller_target_y', 'Controller target y location')
        self._gauge_z_tar = Gauge('controller_target_z', 'Controller target z location')

        self.active = False
        self.finished = False

    def activate(self):
        """
        Activate the printer.

        """
        self.set_active(True)

    def deactivate(self):
        """
        Deactivate the printer.

        """
        self.set_active(False)

    def estimate_current_location(self):
        """
        Estimate the printer's current location by passing sensor readings to estimator.

        Returns
        --------
        xyz_estimate : ndarray
            <3,> array of extimated xyz location.

        """
        xyzs_sensors = self.poll_sensors()
        xyz_estimated = self.estimator.estimate(xyzs_sensors)
        self._gauge_x_est.set(xyz_estimated[0])
        self._gauge_y_est.set(xyz_estimated[1])
        self._gauge_z_est.set(xyz_estimated[2])
        return xyz_estimated

    def execute(self):
        """
        Execute the Controller loop.

        Returns
        --------
        delta_xyz : ndarray or None
            <3,> array of the move command if there is one.
        finished : bool
            True if the printer has reached the final location successfully.

        """
        delta_xyz = None
        finished = False
        if self.hit_target():
            self.index += 1
            if self.index == self.index_max:
                print('Done printing')
                finished = True
                return delta_xyz, finished
            self.target_location = self.target_path[self.index, :]
            self._gauge_x_tar.set(self.target_location[0])
            self._gauge_y_tar.set(self.target_location[1])
            self._gauge_z_tar.set(self.target_location[2])
            print('controller.set_target_location: %s' % self.target_location)
        else:
            delta_xyz = self.get_move_command()
        return delta_xyz, finished

    def get_move_command(self):
        """
        Get the commanded delta to move to the desired location.

        Returns
        --------
        delta_xyz_move : ndarray
            <3,> array of the offset from the current location to the desired location.

        """
        if not self.active: # don't move if the controler is off
            print('Controller is not active. No move command computed.')
            return np.zeros(3)
        location_estimated = self.estimate_current_location()
        delta_xyz_move = self.target_location - location_estimated
        return delta_xyz_move

    def hit_target(self):
        """
        Determine if the current targert location has been hit.

        """
        return np.linalg.norm(self.estimate_current_location() - self.target_location) < self.tol_target

    def poll_sensors(self):
        """
        Poll all of the sensors for their readings.

        """
        return self.sensor_manager.poll_sensors()

    def set_active(self, active):
        """
        Set the active state of the controller.

        Parameters
        -----------
        active : bool
            State to set the controller.

        """
        self.active = active

    def set_target_path(self, target_path):
        """
        Set the target path of the controller.

        Parameters
        -----------
        target_path : ndarray
            <n,3> array of xyz points of the target path.

        """
        self.target_path = target_path
        self.target_location = target_path[0, :]
        self.index_max = self.target_path.shape[0]
        self.index = 0

class SimpleEstimator(object):
    """
    Location estimator by the taking average from multiple sensors.

    """
    def __init__(self):
        self.xyz_previous = None

    def estimate(self, xyzs_sensors):
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
        if xyzs_sensors is None:
            if self.xyz_previous is None:
                msg = 'SimpleEstimator.estimate: No postion has been estimated and no sensor data has been provided.'
                raise RuntimeError(msg)
            return self.xyz_previous
        return np.average(xyzs_sensors, axis=0)
