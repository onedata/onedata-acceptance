"""Utils and fixtures to facilitate operations on spaces in Onezone using
REST API.
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from tests.mixed.onezone_client import (UserApi, SpaceCreateRequest,
                                        SpaceApi, DefaultSpace,
                                        SpaceInviteToken, ProviderApi)
from tests.mixed.utils.common import login_to_oz
from tests.mixed.steps.rest.onezone.common import (get_user_space_with_name,
                                                   get_provider_with_name,
                                                   get_space_with_name)
from tests.gui.utils.generic import parse_seq


def create_spaces_in_oz_using_rest(user, users, hosts, zone_name, space_list):
    user_client = login_to_oz(user, users[user].password,
                              hosts[zone_name]['hostname'])
    user_api = UserApi(user_client)

    for space_name in parse_seq(space_list):
        user_api.create_user_space(SpaceCreateRequest(name=space_name))


def leave_spaces_in_oz_using_rest(user, users, zone_name, hosts, space_list,
                                  spaces):
    user_client = login_to_oz(user, users[user].password,
                              hosts[zone_name]['hostname'])
    user_api = UserApi(user_client)

    for space_name in parse_seq(space_list):
        user_api.remove_user_space(spaces[space_name])


def rename_spaces_in_oz_using_rest(user, users, zone_name, hosts, space_list,
                                   new_names_list, spaces):
    user_client = login_to_oz(user, users[user].password,
                              hosts[zone_name]['hostname'])

    user_api = UserApi(user_client)
    space_api = SpaceApi(user_client)

    for space_name, new_space_name in zip(parse_seq(space_list),
                                          parse_seq(new_names_list)):
        space = user_api.get_user_space(spaces[space_name])
        space.name = new_space_name
        space_api.modify_space(spaces[space_name], space)


def set_space_as_home_in_oz_using_rest(user, users, zone_name, hosts,
                                       space_name, spaces):
    user_client = login_to_oz(user, users[user].password,
                              hosts[zone_name]['hostname'])

    user_api = UserApi(user_client)
    default_space = DefaultSpace(spaces[space_name])
    user_api.set_default_space(default_space)


def remove_spaces_in_oz_using_rest(user, users, zone_name, hosts, space_list,
                                   spaces):
    user_client = login_to_oz(user, users[user].password,
                              hosts[zone_name]['hostname'])
    space_api = SpaceApi(user_client)

    for space_name in parse_seq(space_list):
        if space_name in spaces:
            space_api.remove_space(spaces[space_name])
        else:
            space = get_user_space_with_name(user_client, space_name)
            space_api.remove_space(space.space_id)


def delete_users_from_space_in_oz_using_rest(user_list, users, zone_name, hosts,
                                             space_name, spaces,
                                             user):
    user_client = login_to_oz(user,
                              users[user].password,
                              hosts[zone_name]['hostname'])
    space_api = SpaceApi(user_client)

    for user in parse_seq(user_list):
        space_api.remove_space_user(spaces[space_name], users[user].id)


def remove_provider_support_for_space_in_oz_using_rest(user, users, zone_name,
                                                       hosts, provider_alias,
                                                       space_name, spaces,
                                                       admin_credentials):
    admin_client = login_to_oz(admin_credentials.username,
                               admin_credentials.password,
                               hosts[zone_name]['hostname'])
    provider_name = hosts[provider_alias]['name']
    provider = get_provider_with_name(admin_client, provider_name)
    user_client = login_to_oz(user, users[user].password,
                              hosts[zone_name]['hostname'])
    space_api = SpaceApi(user_client)
    space_api.remove_provider_supporting_space(spaces[space_name],
                                               provider.provider_id)


def add_users_to_space_in_oz_using_rest(user_list, users, zone_name, hosts,
                                        space_name, spaces, user):
    user_client = login_to_oz(user,
                              users[user].password,
                              hosts[zone_name]['hostname'])
    space_api = SpaceApi(user_client)

    for user in parse_seq(user_list):
        space_api.add_space_user(spaces[space_name], users[user].id)


def invite_otehr_users_to_space_using_rest(user, users, zone_name, hosts,
                                           space_name, spaces, tmp_memory,
                                           receiver):
    user_client = login_to_oz(user, users[user].password,
                              hosts[zone_name]['hostname'])
    space_api = SpaceApi(user_client)
    token = space_api.create_space_user_invite_token(spaces[space_name])
    tmp_memory[receiver]['mailbox']['space invitation token'] = token.token


def request_space_support_using_rest(user, users, space_name, zone_alias,
                                     hosts, tmp_memory, receiver):
    user_client = login_to_oz(user, users[user].password,
                              hosts[zone_alias]['hostname'])

    space_api = SpaceApi(user_client)
    space = get_user_space_with_name(user_client, space_name)
    token = space_api.create_space_support_token(space.space_id).token
    tmp_memory[receiver]['mailbox']['token'] = token


def join_space_in_oz_using_rest(user_list, users, zone_name, hosts, space_name,
                                tmp_memory):
    for user in parse_seq(user_list):
        user_client = login_to_oz(user, users[user].password,
                                  hosts[zone_name]['hostname'])
        user_api = UserApi(user_client)
        token = SpaceInviteToken(tmp_memory[user]['mailbox'][space_name])
        user_api.join_space(token)


def assert_spaces_have_appeared_in_oz_rest(user, users, hosts, zone_name,
                                           space_list):
    user_client = login_to_oz(user, users[user].password,
                              hosts[zone_name]['hostname'])

    for space_name in parse_seq(space_list):
        assert get_user_space_with_name(user_client, space_name), 'There is no ' \
                                            'space named {}'.format(space_name)


def assert_there_are_no_spaces_in_oz_rest(user, users, zone_name, hosts,
                                          space_list, spaces):
    user_client = login_to_oz(user, users[user].password,
                              hosts[zone_name]['hostname'])
    user_api = UserApi(user_client)
    user_spaces = user_api.list_user_spaces()

    for space_name in parse_seq(space_list):
        assert spaces[space_name] not in user_spaces.spaces, 'There is ' \
                                            'space named {}'.format(space_name)


def assert_spaces_have_been_renamed_in_oz_rest(user, users, zone_name, hosts,
                                               space_list, new_names_list,
                                               spaces):
    user_client = login_to_oz(user, users[user].password,
                              hosts[zone_name]['hostname'])
    user_api = UserApi(user_client)

    for space_name, new_space_name in zip(parse_seq(space_list),
                                          parse_seq(new_names_list)):
        space_name = user_api.get_user_space(spaces[space_name]).name
        assert space_name == new_space_name,\
            'Space should has name {} but it has name {}'.format(new_space_name,
                                                                 space_name)


def assert_space_is_home_space_in_oz_rest(user, users, zone_name, hosts,
                                          space_name, spaces):
    user_client = login_to_oz(user, users[user].password,
                              hosts[zone_name]['hostname'])
    user_api = UserApi(user_client)
    home_space_id = user_api.get_default_space()
    assert home_space_id.space_id == spaces[space_name], \
        'Space {} is not set as home space'.format(space_name)


def assert_there_is_no_provider_for_space_in_oz_rest(user, users, zone_name,
                                                     hosts, space_name, spaces,
                                                     providers_alias_list,
                                                     admin_credentials):
    user_client = login_to_oz(user,
                              users[user].password,
                              hosts[zone_name]['hostname'])
    space_api = SpaceApi(user_client)
    space_providers = space_api.list_space_providers(spaces[space_name])
    admin_client = login_to_oz(admin_credentials.username,
                               admin_credentials.password,
                               hosts[zone_name]['hostname'])

    for provider_alias in parse_seq(providers_alias_list):
        provider_name = hosts[provider_alias]['name']
        assert_msg = ('Space {} is supported by provider {} while it should '
                      'not be'.format(space_name, provider_name))
        assert (get_provider_with_name(admin_client, provider_name) not in
                space_providers.providers), assert_msg


def assert_user_is_member_of_space_rest(space_name, spaces, user, users,
                                        user_list, zone_name, hosts):
    user_client = login_to_oz(user,
                              users[user].password,
                              hosts[zone_name]['hostname'])
    space_api = SpaceApi(user_client)
    space_users = space_api.list_space_users(spaces[space_name]).users

    for username in parse_seq(user_list):
        assert users[username].id in space_users, \
            'There is no user {} in space {}'.format(username, space_name)


def assert_space_is_supported_by_provider_in_oz_rest(user, users, zone_host,
                                                     hosts, space_name,
                                                     provider_alias):
    user_client = login_to_oz(user, users[user].password,
                              hosts[zone_host]['hostname'])
    provider_name = hosts[provider_alias]['name']

    provider_api = ProviderApi(user_client)
    space = get_user_space_with_name(user_client, space_name)

    providers = [provider_api.get_provider_details(pid).name
                 for pid in space.providers]
    assert provider_name in providers, 'Provider {} does not support space {}'.\
        format(provider_name, space_name)


def assert_provider_does_not_support_space_in_oz_rest(user, users, zone_host,
                                                      hosts, space_name,
                                                      provider_alias):
    user_client_oz = login_to_oz(user, users[user].password,
                                 hosts[zone_host]['hostname'])

    space = get_user_space_with_name(user_client_oz, space_name)
    provider_name = hosts[provider_alias]['name']
    assert provider_name not in space.providers, \
        'Provider {} supports space {}'.format(provider_name, space_name)


def copy_id_of_space_rest(user, users, hosts, space_name, tmp_memory):
    user_client = login_to_oz(user, users[user].password,
                              hosts['onezone']['hostname'])
    space = get_space_with_name(user_client, space_name)
    tmp_memory['spaces'][space_name] = space.space_id
