"""Utils and fixtures to facilitate operation on file tree in file browser
in oneprovider web GUI.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import Optional


class Node:
    def __init__(self, name: str) -> None:
        self.nodes: list[Node] = []
        self.parent: Optional[Node] = None
        self.name: str = name
        self.path: str = ""
        self.content: Optional[str | int] = None

    def set_parent(self, parent: "Node") -> None:
        self.parent = parent
        self.path = self.parent.get_path() + self.name

    def get_items(self) -> list[str]:
        return list(map(lambda x: getattr(x, "name"), self.nodes))

    def get_path(self) -> str:
        if self.path == "":
            return "/"
        return self.path + "/"
