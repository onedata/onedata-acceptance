"""Module implements pytest-bdd steps for authorization and mounting oneclient."""

__author__ = "Jakub Kudzia"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.utils.acceptance_utils import make_arg_list
from tests.utils.bdd_utils import given, parsers, wt

from . import multi_auth_steps


@given(
    parsers.re(r"oneclient mounted using (?P<token>(token|bad token)) by (?P<user>\w+)")
)
def default_mount(user, token, hosts, users, env_desc):
    users[user].mount_client("oneclient-1", "client1", hosts, env_desc, token)


@wt(parsers.re(r"(?P<spaces>.*) is mounted for (?P<user>\w+)"))
@wt(parsers.re(r"(?P<spaces>.*) are mounted for (?P<user>\w+)"))
def check_spaces(spaces, user, users):
    multi_auth_steps.check_spaces(spaces, user, make_arg_list("client1"), users)
