"""Module implements pytest-bdd steps for authorization and mounting oneclient.
"""
__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from pytest_bdd import given, parsers

import multi_auth_steps
from tests.utils.client_utils import mount_users
from tests.utils.acceptance_utils import wt, make_arg_list


@given(parsers.re('(?P<user>\w+) mounts oneclient in (?P<mount_path>.*) '
                  'using (?P<token>.*)'))
def default_mount(user, mount_path, token, request, hosts, users,
                  clients, env_desc):
    mount_users(clients, [user], [mount_path], ['oneclient-1'],
                ['client1'], [token], hosts, request, users, env_desc)


@wt(parsers.re('(?P<spaces>.*) is mounted for (?P<user>\w+)'))
@wt(parsers.re('(?P<spaces>.*) are mounted for (?P<user>\w+)'))
def check_spaces(spaces, user, clients, users):
    multi_auth_steps.check_spaces(spaces, user, make_arg_list('client1'),
                                  users, clients)
