""" This module contains tests of CRUD operations after environment upgrade
"""
__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import os

from tests.utils.client_utils import rm, create_file, mkdir, write, read, stat, CLIENT_CONF

CLIENT_CONF_1 = CLIENT_CONF('user1', '/home/user1/onedata',
                            'oneclient-1', 'client11', 'token')
TEXT = 'example_text'
TEXT2 = 'some_other_text'


def setup(tests_controller):
    client = tests_controller.mount_client(CLIENT_CONF_1)
    space_path = client.absolute_path('space1')
    file_path = os.path.join(space_path, 'file_name')
    mkdir(client, os.path.join(space_path, 'dir_name'))
    create_file(client, file_path)
    write(client, TEXT, file_path)


def verify(tests_controller):
    client = tests_controller.mount_client(CLIENT_CONF_1)
    space_path = client.absolute_path('space1')
    file_path = os.path.join(space_path, 'file_name')
    dir_path = os.path.join(space_path, 'dir_name')
    assert TEXT == read(client, file_path)
    write(client, TEXT2, file_path)
    assert TEXT2 == read(client, file_path)
    stat(client, dir_path)
    rm(client, file_path)
