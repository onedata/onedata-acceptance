"""Utils and fixtures to facilitate operation on file tree in file browser
in oneprovider web GUI.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import Any, List, Optional


class Node:
    def __init__(self, name: str) -> None:
        self.nodes: List[Node] = []
        self.parent: Optional[Node] = None
        self.name: str = name
        self.path: str = ""
        self.content: Any = None

    def set_parent(self, parent: Any) -> Any:
        self.parent = parent
        self.path = self.parent.get_path() + self.name

    def get_items(self) -> Any:
        return list(map(lambda x: getattr(x, "name"), self.nodes))

    def get_path(self) -> Any:
        if self.path == "":
            return "/"
        return self.path + "/"
