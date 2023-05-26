import numpy as np
from dataclasses import dataclass
import copy
import json
from utils import cartesian_to_polar


@dataclass
class BaseObject:
    # id: int = 0  # node id used in networkx graph
    i: int = 0  # index in array
    j: int = 0
    px: float = 0  # x position
    py: float = 0
    pz: float = 0
    # r: float = 0
    # theta: float = 0

    rx: float = 0  # x axis rotation
    ry: float = 0
    rz: float = 0
    sx: float = 1  # x scale
    sy: float = 1
    sz: float = 1
    R: float = 0.5  # Red color channel
    G: float = 0.5
    B: float = 0.5


@dataclass
class Sphere(BaseObject):
    obj_type: int = 'sphere'
    segments: int = 16
    radius: float = 5


@dataclass
class Cube(BaseObject):
    obj_type: int = 'cube'
    length: float = 10


@dataclass
class Tetrahedron(BaseObject):
    obj_type: int = 'tetrahedron'
    segments: int = 1
    radius: float = 10


@dataclass
class Pyramid(BaseObject):
    obj_type: int = 'pyramid'


def compute_attribute_arrays(params, func_dict):
    # pre compute a frame-based dictionary containing the arrays of object attributes at each frame
    frame_dict = {}

    xx, yy = np.meshgrid(np.linspace(-params['plot_length'] / 2, params['plot_length'] / 2, params['grid_length']),
                         np.linspace(-params['plot_height'] / 2, params['plot_height'] / 2, params['grid_height']))
    r, theta = cartesian_to_polar(xx, yy)  # meshgrid with polar coordinates. used as input to wave functions

    for t in range(params['N_frames']):
        attr_dict = {}  # must reinstantiate dict or it wont change for each iteration
        for attr_name in func_dict:
            attr_dict[attr_name] = func_dict[attr_name](r, theta, t)
        frame_dict[f"{t}"] = attr_dict

    return frame_dict, r, theta, xx, yy


def save_objects(objects, save_path):
    with open(f'{save_path}objects.json', 'w') as f:
        json.dump(objects, f, default=lambda x: x.__dict__)
