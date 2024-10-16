"""This module contains utility functions for data management."""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import os

from tests.gui.utils.generic import parse_seq
from tests.gui.utils.oneservices.cdmi import get_item_type


def check_files_tree(subtree, children, cwd, ls_fun, assert_file_content_fun):
    """This function recursively checks files tree:
    - for directory it checks if all elements listed in children are
    present. Then if any directory listed in children has description of
    its file tree, function make recursive call for that subdirectory.
    - for file if description is specified function checks if content
    of file is the same as provided
    """
    for item in subtree:
        try:
            [(item_name, item_desc)] = item.items()
        except AttributeError:
            assert_msg = f"{item} not found in {cwd}"
            assert item in children, assert_msg
            if item.startswith("dir"):
                item_children = ls_fun(os.path.join(cwd, item))
                assert_msg = f"Directory {item} in {cwd} is not empty"
                assert len(item_children) == 0, assert_msg

        else:
            assert_msg = f"{item_name} not found in {cwd}"
            assert item_name in children, assert_msg

            # if item is directory go deeper
            if item_name.startswith("dir"):
                item_children = ls_fun(os.path.join(cwd, item_name))
                if isinstance(item_desc, int):
                    assert_msg = (
                        f"Directory {item_name} in {cwd} has wrong number of "
                        f"children. Expected: {item_desc}, got: {len(children)}"
                    )
                    assert len(item_children) == item_desc, assert_msg

                else:
                    check_files_tree(
                        item_desc,
                        item_children,
                        os.path.join(cwd, item_name),
                        ls_fun,
                        assert_file_content_fun,
                    )
            else:
                assert_file_content_fun(os.path.join(cwd, item_name), str(item_desc))


def create_content(user, users, cwd, content, create_item_fun, host, hosts, request):
    for item in content:
        try:
            [(name, content)] = item.items()
        except AttributeError:
            name = item
            content = None
        create_item_fun(
            user,
            users,
            cwd,
            name,
            content,
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


def assert_ace(priv, item_type, ace, name, num, path):
    priv = parse_seq(priv)
    if "deny" in priv:
        acetype = "0x1"
        priv.remove("deny")
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
    assert set_priv == sorted(priv), f"Privileges in {num} ACE are not correct"


def get_acl_metadata(curr_acl, priv, item_type, groups, name, users, path):
    acl = list(curr_acl)
    acl.append({})
    ace = acl[-1]
    priv = parse_seq(priv)
    if "deny" in priv:
        acetype = "0x1"
        priv.remove("deny")
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
        if ACL_MASK[cdmi_item_type][p] in priv:
            acemask |= p
    ace["acemask"] = hex(acemask)
    ace["aceflags"] = aceflags
    return acl
