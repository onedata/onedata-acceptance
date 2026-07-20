"""This module contains utility functions for data management."""

from __future__ import annotations

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from collections.abc import Iterable, Mapping
from typing import Optional, Protocol

import pytest
import yaml

from tests.gui.meta_steps.oneprovider.files_tree import build_tree_config
from tests.gui.utils.oneservices.cdmi import get_item_type
from tests.mixed.type_definitions import (
    Acl,
    AclEntry,
    AssertFileContent,
    Content,
    ContentItem,
    IsDir,
    ListDir,
)
from tests.type_definitions import Hosts
from tests.utils.user_utils import Users


class FileTreeNode(Protocol):
    path: str
    content: Optional[str | int]

    @property
    def nodes(self) -> Iterable[FileTreeNode]: ...

    def get_items(self) -> Iterable[str]: ...


class CreateItem(Protocol):
    def __call__(
        self,
        user: str,
        users: Users,
        cwd: str,
        name: str,
        content: Content,
        create_item_fun: CreateItem,
        host: str,
        hosts: Hosts,
        request: pytest.FixtureRequest,
    ) -> None: ...


def _check_files_tree(
    parent: FileTreeNode,
    is_dir_fun: IsDir,
    ls_fun: ListDir,
    assert_file_content_fun: AssertFileContent,
) -> None:
    children = ls_fun(parent.path)
    error_message = (
        f"expected item {parent.path} to have children {parent.get_items()} but got"
        f" {children}"
    )
    assert set(parent.get_items()) == set(children), error_message
    for child in parent.nodes:
        if is_dir_fun(child.path):
            if child.content is not None:
                # checking only number of children
                n_items = len(ls_fun(child.path))
                error_message = (
                    f"expected item {parent.path} to have children"
                    f" {int(child.content)} but got {n_items}"
                )
                assert n_items == int(child.content), error_message
            else:
                _check_files_tree(child, is_dir_fun, ls_fun, assert_file_content_fun)
        elif child.content is not None:
            assert_file_content_fun(child.path, str(child.content))


def check_files_tree(
    config: str,
    cwd: str,
    is_dir_fun: IsDir,
    ls_fun: ListDir,
    assert_file_content_fun: AssertFileContent,
) -> None:
    tree = yaml.load(config, yaml.Loader)
    root = build_tree_config(tree, root_path=cwd)
    _check_files_tree(root, is_dir_fun, ls_fun, assert_file_content_fun)


def create_content(
    user: str,
    users: Users,
    cwd: str,
    content: Iterable[ContentItem],
    create_item_fun: CreateItem,
    host: str,
    hosts: Hosts,
    request: pytest.FixtureRequest,
) -> None:
    for item in content:
        if isinstance(item, Mapping):
            [(name, item_content)] = item.items()
        else:
            name = item
            item_content = None
        create_item_fun(
            user,
            users,
            cwd,
            name,
            item_content,
            create_item_fun,
            host,
            hosts,
            request,
        )


ACL_MASK = {
    "object": {
        0x00001: "read",
        0x00002: "write",
        0x00004: "append data",
        0x00008: "read metadata",
        0x00010: "write metadata",
        0x00020: "execute",
        0x00040: "delete element",
        0x00080: "read attributes",
        0x00100: "write attributes",
        0x10000: "delete",
        0x20000: "read acl",
        0x40000: "change acl",
        0x80000: "change owner",
    },
    "container": {
        0x00001: "list files",
        0x00002: "add files",
        0x00004: "add subdirectory",
        0x00008: "read metadata",
        0x00010: "write metadata",
        0x00020: "traverse directory",
        0x00040: "delete subdirectory",
        0x00080: "read attributes",
        0x00100: "write attributes",
        0x10000: "delete",
        0x20000: "read acl",
        0x40000: "change acl",
        0x80000: "change owner",
    },
}


def assert_ace(
    privileges: list[str],
    item_type: str,
    ace: Mapping[str, str],
    name: str,
    entry_number: int | str,
    path: str,
) -> None:
    if "deny" in privileges:
        ace_type = "0x1"
        privileges.remove("deny")
    else:
        ace_type = "0x0"
    ace_flags = "0x40" if item_type == "group" else "0x0"
    item_type = get_item_type(path)
    mask = int(ace["acemask"], 16)
    keys = ACL_MASK[item_type].keys()
    set_privileges = [ACL_MASK[item_type][key] for key in keys if mask & key == key]
    set_privileges.sort()
    assert ace["identifier"].startswith(
        name
    ), f"Identifier in {entry_number} ACE is not {name}"
    assert ace["acetype"] == ace_type, f"Type in {entry_number} ACE is not {ace_type}"
    assert (
        ace["aceflags"] == ace_flags
    ), f"{entry_number} ACE is set for {'group' if ace_flags else 'user'}"
    assert set_privileges == sorted(
        privileges
    ), f"Privileges in {entry_number} ACE are not correct"


def get_acl_metadata(
    current_acl: Iterable[AclEntry],
    privileges: list[str],
    item_type: str,
    groups: Mapping[str, str],
    name: str,
    users: Users,
    path: str,
) -> Acl:
    acl = list(current_acl)
    acl.append({})
    ace = acl[-1]
    if "deny" in privileges:
        ace_type = "0x1"
        privileges.remove("deny")
    else:
        ace_type = "0x0"
    if item_type == "group":
        ace_flags = "0x40"
        name_id = groups[name]
    else:
        ace_flags = "0x0"
        name_id = users[name].user_id
    cdmi_item_type = get_item_type(path)
    ace["identifier"] = f"{name}#{name_id}"
    ace["acetype"] = ace_type
    ace_mask = 0
    for permission_bit in ACL_MASK[cdmi_item_type]:
        if ACL_MASK[cdmi_item_type][permission_bit] in privileges:
            ace_mask |= permission_bit
    ace["acemask"] = hex(ace_mask)
    ace["aceflags"] = ace_flags
    return acl
