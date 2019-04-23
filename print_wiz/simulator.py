# -'''- coding: utf-8 -'''-
import time

import numpy as np
from prometheus_client import start_http_server

from print_wiz.controller import Controller
from print_wiz.desired_path import get_line_path
from print_wiz.printer import Printer
from print_wiz.sensor import Sensor
from print_wiz.sensor_manager import SensorManager
from print_wiz.server import create_simulator_server_handler

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

        self._current_move_command = None
        self._finished = False

    def poll_sensors(self):
        """
        Poll sensors for their locations.

        """
        return self.sensor_manager.poll_sensors()

    def run(self):
        """
        Primary run loop of the simulator.

        """
        self._finished = False
        frequency_controller = 1. # Hz
        time_increment = 1. / frequency_controller
        time_start = time.time()
        time_prev = time_start
        while not self._finished:
            time.sleep(.1)

            # sensors update their locations
            self.sensor_manager.sense_location(self.printer.current_location)

            # check the timer to execute the controller loop at the correct frequency
            time_now = time.time()
            time_elapsed = time_now - time_start
            if time_elapsed > self.timeout:
                print('Timed out at %.0f sec' % time_elapsed)
                break
            if self._current_move_command is not None:
                #print('printer.move_by: %s' % self._current_move_command)
                self.printer.move_by(self._current_move_command)
                self.printer.move()
                #print('current_location: %s' % self.printer.current_location)
                self._current_move_command = None

    def set_move_command(self, delta_xyz_move):
        """
        Set the next movement command. Each command is completed once.

        """
        self._current_move_command = delta_xyz_move

    def finish(self):
        """
        Tell the simulator that the print is finished.

        """
        self._finished = True

def get_simulation():
    """
    Standalone printer loop test with no gui.

    """
    start_http_server(PORT_PROM)

    sensor_good = Sensor('sensor_good', error_scale=.0001)
    sensor_ok = Sensor('sensor_ok', error_scale=.05)
    sensor_bad = Sensor('sensor_bad', error_scale=.2)

    #sensors = [sensor_good, sensor_ok, sensor_bad]
    sensors = [sensor_ok]

    xyz_initial = np.array([-1., 1., 0.2])
    sim = Simulator(xyz_initial)
    for sensor in sensors:
        sim.sensor_manager.add_sensor(sensor)
    sim.sensor_manager.activate_all()
    return sim, sim.sensor_manager.get_sensors(), sim.run

def main_test():
    """
    Standalone printer loop test with no gui.

    """
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
    main_test()
