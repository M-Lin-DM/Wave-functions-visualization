from generate_waves import compute_attribute_arrays
from typing import Optional
import numpy as np
from utils import get_random_base_color, cartesian_to_polar

params = dict()

params['base_color'] = get_random_base_color()

params['grid_length'] = 16  # number of grid points
params['grid_height'] = 9
params['plot_height'] = 4 * np.pi  # actual graph space
params['plot_length'] = params['plot_height'] * 16 / 9

params['fig_size'] = 9

# video params
params['fps'] = 30
params['video_duration'] = 1  # secs
params['N_frames'] = 2  # params['video_duration'] * params['fps']
params['dpi'] = 120

# wave function params
# scale params
params['s_A'] = 1
params['s_w'] = 0.6
params['s_v'] = 0.15
params['s_b'] = 0  # osc about 0 doubles the spatial freq

# rotation params
params['r_A'] = 1
params['r_w'] = 0.7
params['r_v'] = 0.1
params['r_b'] = 0


def polar_wave(A, w, v, b):
    # returns a function parametrized by the inputs but it accepts the array of coordinates and time
    def f(r, theta, t):
        # returns an array given arrays r and theta and scalar t
        return A * np.sin(r * w - v * t) + b

    return f


# define attribute functions
func_dict = {}
func_dict['scale'] = polar_wave(params['s_A'], params['s_w'], params['s_v'], params['s_b'])
func_dict['ry'] = polar_wave(params['r_A'], params['r_w'], params['r_v'], params['r_b'])
func_dict['rx'] = polar_wave(1.1 * params['r_A'], 1.1 * params['r_w'], params['r_v'], params['r_b'])
func_dict['rz'] = polar_wave(params['r_A'], params['r_w'], params['r_v'], params['r_b'])

xx, yy = np.meshgrid(np.linspace(-params['plot_length'] / 2, params['plot_length'] / 2, params['grid_length']),
                     np.linspace(-params['plot_height'] / 2, params['plot_height'] / 2, params['grid_height']))
r, theta = cartesian_to_polar(xx, yy)  # meshgrid with polar coordinates. used as input to wave functions

# print(func_dict['scale'](r, theta, 3))
frame_dict = {}
attr_dict = {}
for t in range(params['N_frames']):
    for attr_name in func_dict:
        attr_dict[attr_name] = func_dict[attr_name](r, theta, t)
    frame_dict[f"{t}"] = attr_dict
    # print(frame_dict[f"{t}"]['scale'][0])


def compute_attribute_arrays(params, func_dict):
    # pre compute a frame-based dictionary containing the arrays of object attributes at each frame
    frame_dict = {}

    xx, yy = np.meshgrid(np.linspace(-params['plot_length'] / 2, params['plot_length'] / 2, params['grid_length']),
                         np.linspace(-params['plot_height'] / 2, params['plot_height'] / 2, params['grid_height']))
    r, theta = cartesian_to_polar(xx, yy)  # meshgrid with polar coordinates. used as input to wave functions

    for t in range(params['N_frames']):
        attr_dict = {}
        for attr_name in func_dict:
            attr_dict[attr_name] = func_dict[attr_name](r, theta, t)
        frame_dict[f"{t}"] = attr_dict
        print(frame_dict[f"{t}"]['scale'][0])

    return frame_dict, r, theta, xx, yy


frame_dict, r, theta, xx, yy = compute_attribute_arrays(params, func_dict)

print(frame_dict.keys())
print(frame_dict['0']['scale'][0])
print(frame_dict['1']['scale'][0])
