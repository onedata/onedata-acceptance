"""Utils and fixtures to facilitate common operations in Onezone using
REST API.
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from onezone_client import (ProviderApi, UserApi,
                            GroupApi, SpaceApi)

def get_provider_with_name(client, provider_name):
    provider_api = ProviderApi(client)
    providers = provider_api.oz_providers_list().providers

    for pid in providers:
        provider = provider_api.get_provider_details(pid)
        if provider.name == provider_name:
            return provider
    else:
        return None


def get_user_space_with_name(client, space_name):
    user_api = UserApi(client)
    user_spaces = user_api.list_user_spaces().spaces
    for sid in user_spaces:
        space = user_api.get_user_space(sid)
        if space.name == space_name:
            return space
    else:
        return None


def get_space_with_name(client, space_name):
    space_api = SpaceApi(client)
    spaces = space_api.oz_spaces_list().spaces
    for sid in spaces:
        space = space_api.get_space(sid)
        if space.name == space_name:
            return space
    else:
        return None


def get_group(group_name, user_client):
    group_api = GroupApi(user_client)
    groups = UserApi(user_client).list_user_groups().groups
    for group in groups:
        g = group_api.get_group(group)
        if g.name == group_name:
            return g
    else:
        return None
