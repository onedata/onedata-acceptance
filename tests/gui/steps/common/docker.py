"""This module contains gherkin steps to run acceptance tests featuring
interaction with docker in onezone web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import os.path
import subprocess
from typing import Any

import yaml

from tests.conftest import Hosts
from tests.gui.utils.generic import parse_seq
from tests.utils.bdd_utils import given, parsers, wt

PROVIDER_CONTAINER_NAME = "oneprovider-1"
MOUNT_POINT = "/volumes/posix"


@given(
    parsers.parse(
        "there is following users configuration in storage's mount point:\n{config}"
    )
)
def docker_configure_users(config: Any, hosts: Hosts) -> Any:
    """
    unix_group_name:
      GID: gid
      users:
        unix_user_name1: uid
        unix_user_name2: uid
        ...
    """
    _docker_configure_users(config, hosts)


def _docker_configure_users(config: Any, hosts: Hosts) -> Any:
    groups_cfg = yaml.load(config, yaml.Loader)
    for group, group_cfg in groups_cfg.items():
        gid = group_cfg["GID"]
        try:
            docker_create_group(group, gid, hosts)
        except subprocess.CalledProcessError as e:
            # if group exists
            if e.returncode == 9:
                pass
            else:
                raise e
        users_cfg = group_cfg["users"]
        for user, uid in users_cfg.items():
            try:
                docker_create_user_with_group(user, uid, group, hosts)
            except subprocess.CalledProcessError as e:
                # if user exists
                if e.returncode == 9:
                    pass
                else:
                    raise e


def docker_create_group(group_name: Any, gid: Any, hosts: Hosts) -> Any:
    cmd = [
        "docker",
        "exec",
        hosts[PROVIDER_CONTAINER_NAME]["container-id"],
        "groupadd",
        group_name,
        "-g",
        str(gid),
    ]
    subprocess.check_call(cmd)


def docker_create_user_with_group(
    user_name: Any, uid: Any, group_name: Any, hosts: Hosts
) -> Any:
    cmd = [
        "docker",
        "exec",
        hosts[PROVIDER_CONTAINER_NAME]["container-id"],
        "useradd",
        "-u",
        str(uid),
        user_name,
        "-G",
        group_name,
    ]
    subprocess.check_call(cmd)


def _docker_cp(
    tmpdir: Any, browser_id: Any, src_path: Any, hosts: Hosts, dst_path: Any = None
) -> Any:
    src_path = os.path.join(str(tmpdir), browser_id, src_path)
    if dst_path:
        cmd = [
            "docker",
            "exec",
            hosts[PROVIDER_CONTAINER_NAME]["container-id"],
            "mkdir",
            "-p",
            dst_path,
        ]
        subprocess.call(cmd)
    else:
        dst_path = MOUNT_POINT

    cmd = [
        "docker",
        "cp",
        src_path,
        f"{hosts[PROVIDER_CONTAINER_NAME]['container-id']}:{dst_path}",
    ]
    subprocess.check_call(cmd)


def _docker_rm(path: Any, hosts: Hosts) -> Any:
    cmd = [
        "docker",
        "exec",
        hosts[PROVIDER_CONTAINER_NAME]["container-id"],
        "rm",
        "-rf",
        path,
    ]
    subprocess.check_call(cmd)


def _docker_mv(path: Any, new_path: Any, hosts: Hosts) -> Any:
    cmd = [
        "docker",
        "exec",
        hosts[PROVIDER_CONTAINER_NAME]["container-id"],
        "mv",
        path,
        new_path,
    ]
    subprocess.check_call(cmd)


def _docker_cat(path: Any, hosts: Hosts) -> Any:
    cmd = [
        "docker",
        "exec",
        hosts[PROVIDER_CONTAINER_NAME]["container-id"],
        "cat",
        path,
    ]
    output = subprocess.check_output(cmd)
    return output


def _docker_ls(path: Any, hosts: Hosts) -> Any:
    cmd = [
        "docker",
        "exec",
        hosts[PROVIDER_CONTAINER_NAME]["container-id"],
        "ls",
        "-a",
        path,
    ]
    output = subprocess.check_output(cmd)
    return output


def _docker_mkdir(path: Any, hosts: Hosts) -> Any:
    cmd = [
        "docker",
        "exec",
        hosts[PROVIDER_CONTAINER_NAME]["container-id"],
        "mkdir",
        "-p",
        path,
    ]
    subprocess.check_call(cmd)


def _docker_append_text_to_file(text: Any, path: Any, hosts: Hosts) -> Any:
    cmd = [
        "docker",
        "exec",
        hosts[PROVIDER_CONTAINER_NAME]["container-id"],
        "sh",
        "-c",
        f"echo {text} >> {path}",
    ]
    subprocess.check_call(cmd)


@wt(
    parsers.parse(
        "user {user} sets {ownership} as {file} owner on provider's storage mount point"
    )
)
def docker_set_file_uid(hosts: Hosts, file: Any, ownership: Any) -> Any:
    cmd = [
        "docker",
        "exec",
        hosts[PROVIDER_CONTAINER_NAME]["container-id"],
        "chown",
        ownership,
        os.path.join(MOUNT_POINT, file),
    ]
    subprocess.check_call(cmd)


@given(parsers.parse('ownership "{ownership}" is granted for storage\'s mount point'))
def docker_set_mount_point_ownership(ownership: Any, hosts: Hosts) -> Any:
    cmd = [
        "docker",
        "exec",
        hosts[PROVIDER_CONTAINER_NAME]["container-id"],
        "chown",
        ownership,
        MOUNT_POINT,
    ]
    subprocess.check_call(cmd)


@wt(
    parsers.parse(
        "user of {browser_id} copies {src_path} to provider's storage mount point"
    )
)
def wt_cp_files_to_storage_mount_point(
    browser_id: Any, src_path: Any, tmpdir: Any, hosts: Hosts
) -> Any:
    _docker_cp(tmpdir, browser_id, src_path, hosts)


@wt(
    parsers.parse(
        "user of {browser_id} copies {src_path} "
        "to {dst_path} in provider's storage mount point"
    )
)
def wt_cp_files_to_dir_in_storage_mount_point(
    browser_id: Any, src_path: Any, tmpdir: Any, hosts: Hosts, dst_path: Any
) -> Any:
    _docker_cp(tmpdir, browser_id, src_path, hosts, os.path.join(MOUNT_POINT, dst_path))


@wt(
    parsers.parse(
        "user of {browser_id} copies {src_path} "
        'to the root directory of "{space}" space'
    )
)
def wt_cp_files_to_space_root_dir(
    browser_id: Any,
    src_path: Any,
    space: Any,
    tmpdir: Any,
    tmp_memory: Any,
    hosts: Hosts,
) -> Any:
    _docker_cp(
        tmpdir,
        browser_id,
        src_path,
        hosts,
        os.path.join(MOUNT_POINT, tmp_memory["spaces"][space]),
    )


@wt(
    parsers.parse(
        "user of {browser_id} copies {src_path} "
        'to {dst_path} directory of "{space}" space'
    )
)
def wt_cp_files_to_dst_path_in_space(
    browser_id: Any,
    src_path: Any,
    dst_path: Any,
    space: Any,
    tmpdir: Any,
    tmp_memory: Any,
    hosts: Hosts,
) -> Any:
    _docker_cp(
        tmpdir,
        browser_id,
        src_path,
        hosts,
        os.path.join(MOUNT_POINT, tmp_memory["spaces"][space], dst_path),
    )


@wt(
    parsers.parse('user of {browser_id} copies "{space}" space directory to {dst_path}')
)
def wt_cp_space_to_dst_path(
    dst_path: Any, space: Any, hosts: Hosts, spaces: Any
) -> Any:
    cmd = [
        "docker",
        "exec",
        hosts[PROVIDER_CONTAINER_NAME]["container-id"],
        "cp",
        "-r",
        f"/volumes/posix/{spaces[space]}/",
        dst_path,
    ]
    subprocess.check_call(cmd)


@wt(
    parsers.parse(
        "user of {browser_id} copies {src_path} to {dst_path} directory on docker"
    )
)
def wt_cp_files_to_dst_path(
    browser_id: Any, src_path: Any, dst_path: Any, tmpdir: Any, hosts: Hosts
) -> Any:
    _docker_cp(tmpdir, browser_id, src_path, hosts, dst_path)


@wt(
    parsers.parse(
        "user of {browser_id} removes {src_path} from provider's storage mount point"
    )
)
def wt_rm_files_to_storage_mount_point(src_path: Any, hosts: Hosts) -> Any:
    _docker_rm(os.path.join(MOUNT_POINT, src_path), hosts)


@given(parsers.parse("there is no {elems} in provider's storage mount point"))
def g_rm_many_files_from_storage_mount_point(elems: Any, hosts: Hosts) -> Any:
    for elem in parse_seq(elems):
        _docker_rm(os.path.join(MOUNT_POINT, elem), hosts)


@wt(
    parsers.parse(
        'user of {browser_id} appends "{text}" to {path} file '
        "in provider's storage mount point"
    )
)
def wt_append_text_to_files_in_storage_mount_point(
    path: Any, text: Any, hosts: Hosts
) -> Any:
    _docker_append_text_to_file(text, os.path.join(MOUNT_POINT, path), hosts)


@wt(
    parsers.parse(
        "user of {browser_id} removes {src_path} "
        'from the root directory of "{space}" space'
    )
)
def wt_rm_files_to_space_root_dir(
    src_path: Any, space: Any, tmp_memory: Any, hosts: Hosts
) -> Any:
    _docker_rm(os.path.join(MOUNT_POINT, tmp_memory["spaces"][space], src_path), hosts)


@wt(parsers.parse("using docker, {user} renames {src_path} path to {new_src_path}"))
def wt_mv_file(src_path: Any, new_src_path: Any, hosts: Hosts) -> Any:
    _docker_mv(src_path, new_src_path, hosts)


@wt(parsers.parse("user creates directory (mkdir) {path} on oneprovider-1 docker"))
def wt_mkdir(path: Any, hosts: Hosts) -> Any:
    _docker_mkdir(path, hosts)


def wt_assert_file_in_path_with_content(path: Any, content: Any, hosts: Hosts) -> Any:
    if path[0] == "/":
        path = path[1::]
    output = _docker_cat(os.path.join(MOUNT_POINT, path), hosts)
    output = output.decode("utf-8")
    err_msg = f"content of the file {path} is expected to be {content} but is {output}"
    assert output == content, err_msg


def docker_ls(path: Any, hosts: Hosts) -> Any:
    files = (
        _docker_ls(os.path.join(MOUNT_POINT, path), hosts).decode("utf-8").split("\n")
    )
    try:
        files.remove("")
        files.remove(".")
        files.remove("..")
    except ValueError:
        pass
    return files
