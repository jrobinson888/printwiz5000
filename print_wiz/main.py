import time

import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
import numpy as np
from prometheus_client import start_http_server

from print_wiz.controller import Controller
from print_wiz.desired_path import get_line_path
from print_wiz.printer import Printer
from print_wiz.sensor import Sensor
from print_wiz.sensor_manager import SensorManager

PORT_PROM = 8000 # port for prometheus server

class Simulator(object):
    """
    Simulation evironemt for printer job.

    """
    def __init__(self, xyz_initial):
        """
        Initialize Simulator.

        Parameters
        -----------
        xyz_initial : ndarray
            <3,> array of the printer's starting location.

        """
        self.timeout = 99999.

        self.printer = Printer(xyz_initial)
        self.printer.activate()

        self.sensor_manager = SensorManager()
        self.controller = Controller(self.sensor_manager)

    def run(self):
        frequency_controller = 1. # Hz
        time_increment = 1. / frequency_controller
        finished = False
        time_start = time.time()
        time_prev = time_start
        while not finished:
            # sensors update their locations
            self.sensor_manager.sense_location(self.printer.current_location)

            # check the timer to execute the controller loop at the correct frequency
            time_now = time.time()
            time_step = time_now - time_prev
            time_elapsed = time_now - time_start
            if time_elapsed > self.timeout:
                print('Timed out at %.0f sec' % time_elapsed)
                break
            if time_step >= time_increment:
                print('controller_loop: elapsed time: %s' % (time.time() - time_start))
                delta_xyz, finished = self.controller.execute()
                if delta_xyz is not None:
                    print('printer.move_by: %s' % delta_xyz)
                    self.printer.move_by(delta_xyz)
                    self.printer.move()
                    print('estimated_location: %s' % self.controller.estimate_current_location())
                    print('target_location: %s' % self.controller.target_location)
                    print('current_location: %s' % self.printer.current_location)
                time_prev = time.time()

def main():
    start_http_server(PORT_PROM)

    sensor_good = Sensor('sensor_good', error_scale=.0001)
    sensor_ok = Sensor('sensor_ok', error_scale=.05)
    sensor_bad = Sensor('sensor_bad', error_scale=.2)

    sensors = [sensor_good, sensor_ok, sensor_bad]

    xyz_initial = np.array([-1., 1., 0.2])
    sim = Simulator(xyz_initial)
    for sensor in sensors:
        sim.sensor_manager.add_sensor(sensor)
    sim.sensor_manager.activate_all()

    xyz_path = get_line_path()
    sim.controller.set_target_path(xyz_path)
    sim.controller.activate()

    sim.run()

if __name__ == '__main__':
    main()
