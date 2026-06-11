"""Utils and fixtures to facilitate operation on file tree in file browser
in oneprovider web GUI.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import List, Optional

from tests.gui.types import GuiObject


class Node:
    def __init__(self, name: str) -> None:
        self.nodes: List[Node] = []
        self.parent: Optional[Optional[Node]] = None
        self.name: str = name
        self.path: str = ""
        self.content: Optional[GuiObject] = None

    def set_parent(self, parent: GuiObject) -> None:
        self.parent = parent
        self.path = self.parent.get_path() + self.name

    def get_items(self) -> GuiObject:
        return list(map(lambda x: getattr(x, "name"), self.nodes))

    def get_path(self) -> GuiObject:
        if self.path == "":
            return "/"
        return self.path + "/"
