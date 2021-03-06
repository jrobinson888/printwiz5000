# -'''- coding: utf-8 -'''-
from threading import Thread
import sys

from PySide2 import QtCore, QtWidgets

from print_wiz.controller import Controller
from print_wiz.desired_path import get_line_path
from print_wiz.simulator import get_simulation
from print_wiz.server import start_server

HOST = 'localhost'
PORT_SIM = 9999

class PrintViewWidget(QtWidgets.QWidget):
    """
    Widget to control the state of the controller and sensors.

    """
    def __init__(self, controller):
        """
        Initialize widget with controller.

        Parameters
        -----------
        controller : Controller
            Controller.

        """
        QtWidgets.QWidget.__init__(self)

        self.controller = controller

        self.sensors = []
        self.layout = None

    def set_sensors(self, sensors):
        """
        Set the sensors and update the layout.

        Parameters
        -----------
        sensors : list [Sensor, ...]
           List of Sensors.

        """
        self.sensors = sensors
        self._reset_layout()

    def _reset_layout(self):
        """
        Reset the layout.

        """
        self.layout = QtWidgets.QGridLayout()

        text = QtWidgets.QLabel('Controller')
        button = QtWidgets.QCheckBox('Active')
        button.clicked.connect(self.controller.set_active)
        button.setChecked(self.controller.active)
        self.layout.addWidget(text, 0, 0)
        self.layout.addWidget(button, 0, 1)

        for isensor, sensor in enumerate(self.sensors):
            text = QtWidgets.QLabel(sensor.name)
            button = QtWidgets.QCheckBox('Active')
            button.clicked.connect(sensor.set_active)
            button.setChecked(sensor.active)
            self.layout.addWidget(text, isensor + 1, 0)
            self.layout.addWidget(button, isensor + 1, 1)
        self.setLayout(self.layout)

def main_test():
    """
    Standalone gui test with dummy controller and sensors.

    """
    app = QtWidgets.QApplication([])
    from print_wiz import __name__ as name
    app.setApplicationName(name)

    class DummyController(object):
        def set_active(self, active):
            print('DummyController.set_active %s' % str(active))

    class DummySensor(object):
        def __init__(self, name):
            self.name = name

        def set_active(self, active):
            print('%s.set_active %s' % (self.name, str(active)))

    controller = DummyController()
    widget = PrintViewWidget(controller)
    sensors = [DummySensor('sensor_1'), DummySensor('sensor_2')]
    widget.set_sensors(sensors)
    widget.show()
    sys.exit(app.exec_())

def main():
    """
    Main entry point.

    """
    app = QtWidgets.QApplication([])
    from print_wiz import __name__ as name
    app.setApplicationName(name)

    simulator, sensors, run_function = get_simulation()

    thread_simulator = Thread(target=run_function, daemon=True)
    thread_simulator.start()

    thread_server = Thread(target=start_server, daemon=True, args=(HOST, PORT_SIM, simulator))
    thread_server.start()

    xyz_path = get_line_path()
    controller = Controller(HOST, PORT_SIM)
    controller.set_target_path(xyz_path)
    #controller.activate()

    thread_controller = Thread(target=controller.run, daemon=True)
    thread_controller.start()

    widget = PrintViewWidget(controller)
    widget.set_sensors(sensors)
    widget.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
    #main_test()
