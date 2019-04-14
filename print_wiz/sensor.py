# -'''- coding: utf-8 -'''-
import numpy as np
from prometheus_client import Gauge

class Sensor(object):
    """
    A simple sensor model with normal random error.

    """
    def __init__(self, name, error_scale=0.05):
        """
        Initialize Sensor.

        Parameters
        -----------
        error_scale : float, optional, default : 0.05
            Standard deviation of the normal sensor random error.

        """
        self.name = name
        self.error_scale = error_scale

        self.active = False
        self.xyz_location = None

        self._gauge_x = Gauge('%s_x' % self.name, 'Sensor %s x location' % self.name)
        self._gauge_y = Gauge('%s_y' % self.name, 'Sensor %s y location' % self.name)
        self._gauge_z = Gauge('%s_z' % self.name, 'Sensor %s z location' % self.name)

    def activate(self):
        """
        Activate the sensor.

        """
        self.set_active(True)

    def get_location(self):
        """
        Get the current estimate of th location from the sensor.

        Returns
        --------
        xyz : ndarray
           <3,> array of location.

        """
        if not self.active:
            msg = 'Sensor %s is not active' % (self.name)
            raise RuntimeError(msg)
        if self.xyz_location is None:
            msg = 'Sensor %s has not recieved a location.' % (self.name)
            raise RuntimeError(msg)
        return self.xyz_location

    def sense_location(self, xyz_true):
        """
        Sense the location including random error.

        Parameters
        -----------
        xyz_true : ndarray
            <3,> array of true location.

        """
        if not self.active:
            msg = 'Sensor %s is not active' % (self.name)
            raise RuntimeError(msg)
        self.xyz_location = xyz_true + np.ones_like(xyz_true) * np.random.normal(scale=self.error_scale)
        self._gauge_x.set(self.xyz_location[0])
        self._gauge_y.set(self.xyz_location[1])
        self._gauge_z.set(self.xyz_location[2])

    def set_active(self, active):
        """
        Set the active state of the sensor.

        Parameters
        -----------
        active : bool
            State to set the sensor.

        """
        self.active = active
