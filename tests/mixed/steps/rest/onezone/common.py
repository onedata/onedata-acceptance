"""Utils and fixtures to facilitate common operations in Onezone using
REST API.
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from onezone_client import (
    ApiClient,
    Group,
    GroupApi,
    ProviderApi,
    Space,
    SpaceApi,
    UserApi,
)
from onezone_client.models.provider_details import ProviderDetails


def get_provider_with_name(client: ApiClient, provider_name: str) -> ProviderDetails:
    provider_api = ProviderApi(client)
    providers = provider_api.oz_providers_list().providers

    for pid in providers:
        provider = provider_api.get_provider_details(pid)
        if provider.name == provider_name:
            return provider
    raise AssertionError(f'provider "{provider_name}" not found')


def get_user_space_with_name(client: ApiClient, space_name: str) -> Space:
    user_api = UserApi(client)
    user_spaces = user_api.list_user_spaces().spaces
    for sid in user_spaces:
        space = user_api.get_user_space(sid)
        if space.name == space_name:
            return space
    raise AssertionError(f'user space "{space_name}" not found')


def get_space_with_name(client: ApiClient, space_name: str) -> Space:
    space_api = SpaceApi(client)
    spaces = space_api.list_spaces().spaces
    for sid in spaces:
        space = space_api.get_space(sid)
        if space.name == space_name:
            return space
    raise AssertionError(f'space "{space_name}" not found')


def get_group(group_name: str, user_client: ApiClient) -> Group:
    group_api = GroupApi(user_client)
    groups = UserApi(user_client).list_user_groups().groups
    for group in groups:
        g = group_api.get_group(group)
        if g.name == group_name:
            return g
    raise AssertionError(f'group "{group_name}" not found')
