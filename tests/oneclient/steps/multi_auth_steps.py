"""Module implements pytest-bdd steps for authorization and mounting oneclient.
"""
__author__ = "Jakub Kudzia, Piotr Ociepka"
__copyright__ = "Copyright (C) 2015-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.utils.utils import assert_
from tests.utils.acceptance_utils import list_parser
from tests.utils.bdd_utils import given, then, parsers


@given(parsers.re('oneclients (?P<client_ids>.*)\n'
                  'mounted on client_hosts (?P<client_hosts>.*) respectively,\n'
                  'using (?P<tokens>.*) by (?P<user_names>.*)'))
def multi_mount(user_names, client_ids, client_hosts, tokens, hosts, users, env_desc):
    params = zip(list_parser(user_names), list_parser(client_ids),
                 list_parser(client_hosts), list_parser(tokens))

    for (username, client_id, client_host, token) in params:
        user = users.get(username)
        user.mount_client(client_host, client_id, hosts, env_desc, token)


@then(parsers.re('(?P<spaces>.*) are mounted for (?P<user_name>\w+) on '
                 '(?P<client_nodes>.*)'))
def check_spaces(spaces, user_name, client_nodes, users):
    spaces = list_parser(spaces)
    user_name = str(user_name)
    client_nodes = list_parser(client_nodes)

    for client_node in client_nodes:
        user = users.get(user_name)
        client = user.clients.get(client_node)

        def condition():
            spaces_in_client = client.list_spaces()
            for space in spaces:
                assert space in spaces_in_client, 'Space {} not found in spaces list {} ' \
                                                  'on client {}'.format(spaces, spaces_in_client,
                                                                        client_node)

        assert_(client.perform, condition)
