import socket
import sys

import numpy as np

HOST, PORT = 'localhost', 9999
def main():
    data = np.array([[1., 3., 0.],
                     [2., 66., 5.]])
    requests = [
        ('poll', None),
        ('move', np.array([1., 3., 0.])),
    ]
    for command, data in requests:
        send_request(command, data=data)

def send_request(host, port, command, data=None):
    allowed_commnads = ['poll', 'move']
    if command not in allowed_commnads:
        msg = 'Command %s must be one of %s' % (command, allowed_commnads)
        raise ValueError(msg)

    message = encode_message(command, data)

    # Create a socket (SOCK_STREAM means a TCP socket)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        # Connect to server and send data
        #print('connecting...')
        sock.connect((host, port))
        print('sending %s' % command)
        sock.sendall(message)

        # Receive data from the server and shut down
        received = sock.recv(1024)
        state, data_recieved = decode_returned(command, received)

    #print('Sent: %s %s' % (command, data))
    #print('Received: %s %s' % (state, data_recieved))
    return data_recieved

def decode_returned(command, received):
    state = int(received[0:1])
    data = None
    if command == 'poll':
        data = np.frombuffer(received[1:]).reshape(-1, 3)
    return state, data

def encode_message(command, data=None):
    message = command.encode()
    if command == 'move':
        data_encoded = np.asarray(data).tobytes()
        message += data_encoded
    return message

if __name__ == '__main__':
    main()
