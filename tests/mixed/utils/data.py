"""This module contains utility functions for data management."""

from __future__ import annotations

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from collections.abc import Callable, Iterable, Mapping, MutableMapping, Sequence
from typing import Protocol

import yaml

from tests.gui.meta_steps.oneprovider.files_tree import build_tree_config
from tests.gui.utils.generic import parse_seq
from tests.gui.utils.oneservices.cdmi import get_item_type


class FileTreeNode(Protocol):
    path: str
    content: str | int | None

    @property
    def nodes(self) -> Iterable[FileTreeNode]: ...

    def get_items(self) -> Iterable[str]: ...


class UserLike(Protocol):
    user_id: str


ContentItem = str | Mapping[str, object]
AclEntry = MutableMapping[str, str]
Acl = list[AclEntry]
ItemType = str
IsDir = Callable[[str], bool]
ListDir = Callable[[str], Sequence[str]]
AssertFileContent = Callable[[str, str], object]
CreateItem = Callable[..., object]


def _check_files_tree(
    parent: FileTreeNode,
    is_dir_fun: IsDir,
    ls_fun: ListDir,
    assert_file_content_fun: AssertFileContent,
) -> None:
    children = ls_fun(parent.path)
    err_msg = (
        f"expected item {parent.path} to have children {parent.get_items()} but got"
        f" {children}"
    )
    assert set(parent.get_items()) == set(children), err_msg
    for child in parent.nodes:
        if is_dir_fun(child.path):
            if child.content is not None:
                # checking only number of children
                n_items = len(ls_fun(child.path))
                err_msg = (
                    f"expected item {parent.path} to have children"
                    f" {int(child.content)} but got {n_items}"
                )
                assert n_items == int(child.content), err_msg
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
    users: object,
    cwd: str,
    content: Iterable[ContentItem],
    create_item_fun: CreateItem,
    host: str,
    hosts: object,
    request: object,
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
    priv: str,
    item_type: ItemType,
    ace: Mapping[str, str],
    name: str,
    num: int | str,
    path: str,
) -> None:
    parsed_priv = parse_seq(priv)
    if "deny" in parsed_priv:
        acetype = "0x1"
        parsed_priv.remove("deny")
    else:
        acetype = "0x0"
    aceflags = "0x40" if item_type == "group" else "0x0"
    item_type = get_item_type(path)
    mask = int(ace["acemask"], 16)
    keys = ACL_MASK[item_type].keys()
    set_priv = [ACL_MASK[item_type][key] for key in keys if mask & key == key]
    set_priv.sort()
    assert ace["identifier"].startswith(name), f"Identifier in {num} ACE is not {name}"
    assert ace["acetype"] == acetype, f"Type in {num} ACE is not {acetype}"
    assert (
        ace["aceflags"] == aceflags
    ), f"{num} ACE is set for {'group' if aceflags else 'user'}"
    assert set_priv == sorted(parsed_priv), f"Privileges in {num} ACE are not correct"


def get_acl_metadata(
    curr_acl: Iterable[AclEntry],
    priv: str,
    item_type: ItemType,
    groups: Mapping[str, str],
    name: str,
    users: Mapping[str, UserLike],
    path: str,
) -> Acl:
    acl = list(curr_acl)
    acl.append({})
    ace = acl[-1]
    parsed_priv = parse_seq(priv)
    if "deny" in parsed_priv:
        acetype = "0x1"
        parsed_priv.remove("deny")
    else:
        acetype = "0x0"
    if item_type == "group":
        aceflags = "0x40"
        name_id = groups[name]
    else:
        aceflags = "0x0"
        name_id = users[name].user_id
    cdmi_item_type = get_item_type(path)
    ace["identifier"] = f"{name}#{name_id}"
    ace["acetype"] = acetype
    acemask = 0
    for p in ACL_MASK[cdmi_item_type]:
        if ACL_MASK[cdmi_item_type][p] in parsed_priv:
            acemask |= p
    ace["acemask"] = hex(acemask)
    ace["aceflags"] = aceflags
    return acl
