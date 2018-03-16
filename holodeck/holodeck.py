import os
import uuid
from copy import copy

from holodeck.environments import HolodeckEnvironment, AgentDefinition
from holodeck.exceptions import HolodeckException
from holodeck.packagemanager import _iter_packages


class GL_VERSION(object):
    OPENGL4 = 4
    OPENGL3 = 3


def _get_worlds_map():
    holodeck_worlds = dict()
    for config, path in _iter_packages():
        for level in config["maps"]:
            holodeck_worlds[level["name"]] = {
                "agent_definitions": [AgentDefinition(**x) for x in level["agents"]],
                "binary_path": os.path.join(path, config["path"]),
                "task_key": level["name"],
                "height": level["resy"],
                "width": level["resx"]}
    return holodeck_worlds


def make(world, gl_version=GL_VERSION.OPENGL4):
    holodeck_worlds = _get_worlds_map()
    if world not in holodeck_worlds:
        raise HolodeckException("Invalid World Name")

    param_dict = copy(holodeck_worlds[world])
    param_dict["start_world"] = True
    param_dict["uuid"] = str(uuid.uuid4())
    param_dict["gl_version"] = gl_version
    return HolodeckEnvironment(**param_dict)
