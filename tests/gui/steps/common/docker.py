"""This module contains gherkin steps to run acceptance tests featuring
interaction with docker in onezone web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import os.path
import subprocess

from tests.gui.utils.generic import parse_seq
from tests.utils.bdd_utils import given, parsers, wt

PROVIDER_CONTAINER_NAME = 'oneprovider-1'
MOUNT_POINT = '/volumes/posix'


def _docker_cp(tmpdir, browser_id, src_path, hosts, dst_path=None):
    src_path = os.path.join(str(tmpdir), browser_id, src_path)
    if dst_path:
        cmd = ['docker', 'exec', hosts[PROVIDER_CONTAINER_NAME]['container-id'],
               'mkdir', '-p', dst_path]
        subprocess.call(cmd)
    else:
        dst_path = MOUNT_POINT

    cmd = ["docker", "cp", src_path, "{0}:{1}".format(hosts[PROVIDER_CONTAINER_NAME]['container-id'],
                                                      dst_path)]
    subprocess.check_call(cmd)


def _docker_rm(path, hosts):
    cmd = ['docker', 'exec', hosts[PROVIDER_CONTAINER_NAME]['container-id'], 'rm', '-rf', path]
    subprocess.check_call(cmd)


def _docker_mv(path, new_path, hosts):
    cmd = ['docker', 'exec', hosts[PROVIDER_CONTAINER_NAME]['container-id'], 'mv', path, new_path]
    subprocess.check_call(cmd)


def _docker_append_text_to_file(text, path, hosts):
    cmd = ['docker', 'exec', hosts[PROVIDER_CONTAINER_NAME]['container-id'],
           'sh', '-c', f'echo {text} >> {path}']
    subprocess.check_call(cmd)


@wt(parsers.parse('user of {browser_id} copies {src_path} '
                  'to provider\'s storage mount point'))
def wt_cp_files_to_storage_mount_point(browser_id, src_path, tmpdir, hosts):
    _docker_cp(tmpdir, browser_id, src_path, hosts)


@wt(parsers.parse('user of {browser_id} copies {src_path} '
                  'to {dst_path} in provider\'s storage mount point'))
def wt_cp_files_to_dir_in_storage_mount_point(browser_id, src_path, tmpdir,
                                              hosts, dst_path):
    _docker_cp(tmpdir, browser_id, src_path, hosts,
               os.path.join(MOUNT_POINT, dst_path))


@wt(parsers.parse('user of {browser_id} copies {src_path} '
                  'to the root directory of "{space}" space'))
def wt_cp_files_to_space_root_dir(browser_id, src_path, space,
                                  tmpdir, tmp_memory, hosts):
    _docker_cp(tmpdir, browser_id, src_path, hosts,
               os.path.join(MOUNT_POINT, tmp_memory['spaces'][space]))


@wt(parsers.parse('user of {browser_id} copies {src_path} '
                  'to {dst_path} directory of "{space}" space'))
def wt_cp_files_to_dst_path_in_space(browser_id, src_path, dst_path,
                                     space, tmpdir, tmp_memory, hosts):
    _docker_cp(tmpdir, browser_id, src_path, hosts,
               os.path.join(MOUNT_POINT, tmp_memory['spaces'][space],
                            dst_path))


@wt(parsers.parse('user of {browser_id} copies {src_path} '
                  'to {dst_path} directory on docker'))
def wt_cp_files_to_dst_path(browser_id, src_path, dst_path, tmpdir, hosts):
    _docker_cp(tmpdir, browser_id, src_path, hosts, dst_path)


@wt(parsers.parse('user of {browser_id} removes {src_path} '
                  'from provider\'s storage mount point'))
def wt_rm_files_to_storage_mount_point(src_path, hosts):
    _docker_rm(os.path.join(MOUNT_POINT, src_path), hosts)


@given(parsers.parse('there is no {elems} in provider\'s storage mount point'))
def g_rm_many_files_from_storage_mount_point(elems, hosts):
    for elem in parse_seq(elems):
        _docker_rm(os.path.join(MOUNT_POINT, elem), hosts)


@wt(parsers.parse('user of {browser_id} appends "{text}" to {path} file '
                  'in provider\'s storage mount point'))
def wt_append_text_to_files_in_storage_mount_point(path, text, hosts):
    _docker_append_text_to_file(text, os.path.join(MOUNT_POINT, path), hosts)


@wt(parsers.parse('user of {browser_id} removes {src_path} '
                  'from the root directory of "{space}" space'))
def wt_rm_files_to_space_root_dir(src_path, space, tmp_memory, hosts):
    _docker_rm(os.path.join(MOUNT_POINT, tmp_memory['spaces'][space],
                            src_path), hosts)


@wt(parsers.parse('using docker, {user} renames {src_path} path '
                  'to {new_src_path}'))
def wt_mv_file(src_path, new_src_path, hosts):
    _docker_mv(src_path, new_src_path, hosts)


@wt(parsers.parse('elasticsearch plugin stops working'))
def pause_elasticsearch_container(hosts):
    pause_cmd = ['docker', 'pause']
    container_id = hosts['elasticsearch']['container-id']
    subprocess.call(pause_cmd + [container_id])


@wt(parsers.parse('elasticsearch plugin starts working'))
def unpause_elasticsearch_container(hosts):
    unpause_cmd = ['docker', 'unpause']
    container_id = hosts['elasticsearch']['container-id']
    subprocess.call(unpause_cmd + [container_id])
