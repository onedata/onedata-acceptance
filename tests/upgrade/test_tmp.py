""" fixme
"""
__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import os

from tests.utils.client_utils import rm, create_file, mkdir, write, read
from tests.upgrade.utils.upgrade_utils import UpgradeTestsController
from tests.performance import CLIENT_CONF

CLIENT_CONF_1 = CLIENT_CONF('user1', '/home/user1/onedata',
                            'oneclient-1', 'client11', 'token')
TEXT = 'example_text'


# fixme admin user as fixture
def test_tmp(test_config, hosts, clients, request, users, env_desc,
             scenario_abs_path):

    a = UpgradeTestsController(**locals())

    a.add_test(
        simple_crud_setup, simple_crud_check)

    a.run_tests()


def simple_crud_setup(test_object):
    client = test_object.mount_client(CLIENT_CONF_1)
    space_path = client.absolute_path('space1')
    file_path = os.path.join(space_path, 'osiem')
    mkdir(client, os.path.join(space_path, 'dupa'))
    create_file(client, file_path)
    write(client, TEXT, file_path)


def simple_crud_check(test_object):
    client = test_object.mount_client(CLIENT_CONF_1)
    space_path = client.absolute_path('space1')
    file_path = os.path.join(space_path, 'osiem')
    assert TEXT == read(client, file_path)
    rm(client, file_path)
