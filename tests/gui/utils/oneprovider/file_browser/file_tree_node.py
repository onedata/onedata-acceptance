"""Utils and fixtures to facilitate operation on file tree in file browser
in oneprovider web GUI.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)


class Node:
    def __init__(self, name):
        self.nodes = []
        self.parent = None
        self.name = name
        self.path = None
        self.content = None

    def set_parent(self, parent):
        self.parent = parent
        self.path = self.parent.get_path() + self.name

    def get_items(self):
        return list(map(lambda x: getattr(x, "name"), self.nodes))

    def get_path(self):
        if self.path == "":
            return "/"
        else:
            return self.path + "/"
