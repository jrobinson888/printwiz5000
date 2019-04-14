from collections import OrderedDict

import numpy as np

class SensorManager(object):
    """
    Containter and interface to Sensors.

    """
    def __init__(self):
        """
        Initialize SensorManager.

        """
        self.sensors = OrderedDict()

    def activate_all(self):
        """
        Activate all sensors.

        """
        for sensor in self.sensors.values():
            sensor.activate()

    def add_sensor(self, sensor):
        """
        Add a sensor.

        """
        self.sensors[sensor.name] = sensor

    def get_sensors(self):
        """
        Get list of sensors.

        Returns
        --------
        sensors: list [Sensor]
           List of sensors.

        """
        return list(self.sensors.values())

    def poll_sensors(self):
        """
        Poll all of the sensors for their readings.

        """
        nsensors_active = sum(1 if sensor.active else 0 for sensor in self.sensors.values())
        if not nsensors_active:
            return
        xyzs_sensors = np.zeros((nsensors_active, 3))
        for i, sensor in enumerate(self.sensors.values()):
            try:
                xyzs_sensors[i, :] = sensor.get_location()
            except RuntimeError:
                pass
        return xyzs_sensors

    def sense_location(self, xyz_true):
        """
        Sense the location including random error.

        Parameters
        -----------
        xyz_true : ndarray
            <3,> array of true location.

        """
        for sensor in self.sensors.values():
            if sensor.active:
                sensor.sense_location(xyz_true)

