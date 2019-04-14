# -'''- coding: utf-8 -'''-
import numpy as np

def get_cylinder_path():
    thickness_layer = .01
    radius = 4.

    theta = np.linspace(0., 2 * np.pi)
    x_path = radius * np.cos(theta)
    y_path = radius * np.sin(theta)
    z_path = np.ones_like(theta)

    nlayers = 5
    x_path = np.tile(x_path, (1, nlayers)).ravel()
    y_path = np.tile(y_path, (1, nlayers)).ravel()
    z_path = np.hstack((z_path * thickness_layer * i for i in range(nlayers)))

    print('x_path: %s' % str(x_path.shape))
    print('y_path: %s' % str(y_path.shape))
    print('z_path: %s' % str(z_path.shape))

    return x_path, y_path, z_path

def get_line_path():
    thickness_layer = .01
    nlayers = 10
    length = 5.

    nwaypoints = 20

    x_path = np.tile(np.hstack((np.linspace(0., length, nwaypoints), np.linspace(length, 0., nwaypoints))), (1, nlayers)).ravel()
    y_path = np.zeros_like(x_path).ravel()
    z_path = np.hstack((np.ones(nwaypoints) * thickness_layer * i for i in range(2 * nlayers)))

    print('x_path: %s' % str(x_path.shape))
    print('y_path: %s' % str(y_path.shape))
    print('z_path: %s' % str(z_path.shape))

    return np.hstack((x_path.reshape(-1, 1), y_path.reshape(-1, 1), z_path.reshape(-1, 1)))
