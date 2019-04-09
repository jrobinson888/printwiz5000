import numpy as np

class Sensor(object):
    """
    A simple sensor model with normal random error.

    """
    def __init__(self, error_scale=0.05):
        """
        Initialize Sensor.

        Parameters
        -----------
        error_scale : float, optional, default : 0.05
            Standard deviation of the normal sensor random error.

        """
        self.error_scale = error_scale

        self.xyz_location = None

    def get_location(self):
        """
        Get the current estimate of th location from the sensor.

        Returns
        --------
        xyz : ndarray
           <3,> array of location.

        """
        if self.xyz_location is None:
            msg = 'Sensor has not recieved a location.'
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
        self.xyz_location = xyz_true + np.ones_like(xyz_true) * np.random.normal(scale=self.error_scale)
