"""Module implements common meta steps for operation on files (both regular filesand directories)."""

__author__ = "Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import Any, Literal

import yaml

from tests.oneclient.conftest import Users
from tests.oneclient.steps.multi_file_steps import stat_absent, stat_present
from tests.utils.bdd_utils import parsers, wt

type NodeState = Literal["present", "absent"]
type TreeConfig = dict[str, None | NodeState | TreeConfig]


@wt(
    parsers.re(
        r'(?P<user>\w+) sees on "(?P<client_node>.*)", that file tree rooted at path (?P<root_path>.*) contains following nodes:\n(?P<config>(.|\s)*)'
    )
)
def assert_file_tree_nodes(user: str, config: str, client_node: str, root_path: str, users: Users):
    file_tree = yaml.safe_load(config) or {}

    # parent_path needs to be changed into pathlib in the future
    def assert_tree_node(parent_path: str, nodes: Any):
        for name, children in nodes.items():
            # current node is a file that is expected to be present or absent
            if isinstance(children, NodeState):
                if children == "present":
                    stat_present(user, parent_path, name, client_node, users)
                else:
                    stat_absent(user, parent_path, name, client_node, users)
                continue

            # current node is a not an empty directory, otherwise we skip
            if children is not None:
                new_parent_path = f"{parent_path}/{name}"
                assert_tree_node(new_parent_path, children)

    # parent path parameter is usually initially a space_name,
    # nodes parameter is initially whole yaml config,
    # that will be narrowed down to yaml subnodes during recursive calls
    assert_tree_node(
        parent_path=root_path,
        nodes=file_tree,
    )
