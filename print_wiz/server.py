# -'''- coding: utf-8 -'''-
import socketserver

import numpy as np

BUFFER_SIZE = 1024
STATE_BAD = 1
STATE_GOOD = 0

def create_simulator_server_handler(simulator):

    class SimulatorServerHandler(socketserver.BaseRequestHandler):
        """
        The request handler class for Simulator.

        It is instantiated once per connection to the server, and must
        override the handle() method to implement communication to the
        client.

        """
        allowed_commands = ['poll', 'move']
        def handle(self):
            # self.request is the TCP socket connected to the client
            self.data = self.request.recv(BUFFER_SIZE).strip()
            message = self.data
            #print('%s  wrote:' % (self.client_address[0]))
            #print(message)
            if self.data:
                command = self.data[0:4].decode().lower()
                if command == 'poll':
                    state = STATE_GOOD
                    data_return = simulator.poll_sensors().tobytes()
                elif command == 'move':
                    try:
                        xyz_move = np.frombuffer(self.data[4:])
                    except:
                        state = STATE_BAD
                        data_return = None
                    else:
                        state = STATE_GOOD
                        data_return = simulator.set_move_command(xyz_move)
                else:
                    state = STATE_BAD
                    data_return = None

                message_return = b'%i' % (state)
                #print(len(message_return))
                if data_return is not None:
                    message_return += data_return
                    #print(len(message_return))

                self.request.sendall(message_return)

    return SimulatorServerHandler

def start_server(host, port, simulator):
    print('starting simulator server at %s:%s' % (host, port))
    simulator_server_handler = create_simulator_server_handler(simulator)
    server = socketserver.TCPServer((host, port), simulator_server_handler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

if __name__ == '__main__':
    HOST, PORT = 'localhost', 9999

    class DummySimulator(object):
        def __init__(self):
            pass
        def poll_sensors(self):
            return np.zeros((4, 3))

        def set_move_command(self, xyz_move):
            print('set_move_command: %s %s' % (xyz_move, str(xyz_move.shape)))


    simulator = DummySimulator()
    # Create the server, binding to localhost on port 9999
    start_server(host, port, simulator)
