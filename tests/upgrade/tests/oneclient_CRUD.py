""" This module contains tests of CRUD operations after environment upgrade
"""
__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import os


TEXT = 'example_text'
TEXT2 = 'some_other_text'


def setup(space_name):
    def fun(tests_controller):
        client = tests_controller.mount_client('user1', 'oneclient-1', 'client11')
        space_path = client.absolute_path(space_name)
        file_path = os.path.join(space_path, 'file_name')
        client.mkdir(os.path.join(space_path, 'dir_name'))
        client.create_file(file_path)
        client.write(TEXT, file_path)
    return fun


def verify(space_name):
    def fun(tests_controller):
        client = tests_controller.mount_client('user1', 'oneclient-1', 'client11')
        space_path = client.absolute_path(space_name)
        file_path = os.path.join(space_path, 'file_name')
        dir_path = os.path.join(space_path, 'dir_name')
        assert TEXT == client.read(file_path)
        client.write(TEXT2, file_path)
        assert TEXT2 == client.read(file_path)
        client.stat(dir_path)
        client.rm(file_path)
    return fun
