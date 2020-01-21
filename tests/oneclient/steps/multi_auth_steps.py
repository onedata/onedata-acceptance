"""Module implements pytest-bdd steps for authorization and mounting oneclient.
"""
__author__ = "Jakub Kudzia, Piotr Ociepka"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.utils.utils import assert_
from tests.utils.client_utils import mount_users, ls
from tests.utils.acceptance_utils import list_parser
from tests.utils.bdd_utils import given, then, parsers


@given(parsers.re('oneclients (?P<client_instances>.*)\n'
                  'mounted in (?P<mount_paths>.*)\n'
                  'on client_hosts (?P<client_hosts>.*) respectively,\n'
                  'using (?P<tokens>.*) by (?P<user_names>.*)'))
def multi_mount(user_names, client_instances, mount_paths, client_hosts,
                tokens, clients, hosts, request, users, env_desc):
    mount_users(clients, list_parser(user_names), list_parser(mount_paths),
                list_parser(client_hosts), list_parser(client_instances),
                list_parser(tokens), hosts, request, users, env_desc)


@then(parsers.re('(?P<spaces>.*) are mounted for (?P<user_name>\w+) on '
                 '(?P<client_nodes>.*)'))
def check_spaces(spaces, user_name, client_nodes, users, clients):
    spaces = list_parser(spaces)
    user_name = str(user_name)
    client_nodes = list_parser(client_nodes)

    for client_node in client_nodes:
        user = users.get(user_name)
        client = user.clients.get(client_node)

        def condition():
            spaces_in_client = ls(client, path=client.mount_path)
            for space in spaces:
                assert space in spaces_in_client

        assert_(client.perform, condition)
