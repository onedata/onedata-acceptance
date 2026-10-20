"""Module implements common meta steps for operation on files (both regular filesand directories)."""

__author__ = "Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import Literal

import yaml

from tests.oneclient.conftest import Users
from tests.oneclient.steps.multi_file_steps import ls_absent, ls_present, stat_absent, stat_present
from tests.utils.bdd_utils import parsers, wt

type NodeState = Literal["present", "absent"]
type TreeConfig = dict[str, None | NodeState | TreeConfig]


def parse_tree_config(config: str) -> TreeConfig:
    loaded_config: object = yaml.safe_load(config)
    if loaded_config is None:
        return {}

    return _validate_tree_config(loaded_config)


def _validate_tree_config(config: object, path: str = "config") -> TreeConfig:
    if not isinstance(config, dict):
        raise ValueError(f"{path} must be a mapping")

    tree_config: TreeConfig = {}
    for name, children in config.items():
        if not isinstance(name, str):
            raise ValueError(f"node name at {path} must be a string")

        node_path = f"{path}.{name}"
        if children is None or children in ("present", "absent"):
            tree_config[name] = children
        elif isinstance(children, dict):
            tree_config[name] = _validate_tree_config(children, node_path)
        else:
            raise ValueError(f"{node_path} must be a mapping, null, 'present', or 'absent'")

    return tree_config


@wt(
    parsers.re(
        r'(?P<user>\w+) sees on "(?P<client_node>[^"]+)", that file tree rooted at'
        r' "(?P<root_path>[^\r\n]+)" contains following nodes:\n(?P<config>[\s\S]*)'
    ),
    converters={"config": parse_tree_config},
)
def assert_file_tree_nodes(
    user: str,
    config: TreeConfig,
    client_node: str,
    root_path: str,
    users: Users,
) -> None:
    # parent_path needs to be changed into pathlib in the future
    def assert_tree_node(parent_path: str, nodes: TreeConfig) -> None:
        for name, children in nodes.items():
            # current node is a file that is expected to be present or absent
            if children == "present":
                ls_present(user, name, parent_path, client_node, users)
                continue
            if children == "absent":
                ls_absent(user, name, parent_path, client_node, users)
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
        nodes=config,
    )


@wt(
    parsers.re(
        r"(?P<user>\w+) (?P<visibility>can|can't) see and "
        r"(?P<stat>can|can't) stat (?P<files>.*) in (?P<path>.*) on "
        r'"(?P<client_node>[^"]+)"'
    )
)
def assert_expected_result_for_visibility_and_stat(
    user: str,
    files: str,
    path: str,
    users: Users,
    visibility: str,
    stat: str,
    client_node: str,
) -> None:
    visible, can_stat = visibility == "can", stat == "can"
    ls_function = ls_present if visible else ls_absent
    stat_function = stat_present if can_stat else stat_absent

    stat_function(user, path, files, client_node, users)
    ls_function(user, files, path, client_node, users)
