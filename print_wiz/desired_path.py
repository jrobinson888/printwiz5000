import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
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

    fig = plt.figure()
    axes = fig.add_subplot(111, projection='3d')
    axes.plot3D(x_path, y_path, z_path, 'k-')
    axes.plot3D(x_path, y_path, z_path, 'ro')
    fig.savefig('path.png')

    return x_path, y_path, z_path
