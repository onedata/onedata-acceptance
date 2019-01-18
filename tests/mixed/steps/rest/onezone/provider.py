"""Utils and fixtures to facilitate operations on providers in Onezone
using REST API.
"""

from tests.mixed.utils.common import login_to_oz
from tests.mixed.steps.rest.onezone.common import get_provider_with_name
from tests.mixed.onezone_client import ProviderApi


def assert_provider_has_name_and_hostname_in_oz_rest(user, users, host_name,
                                                     hosts, provider_name,
                                                     domain):
    user_client = login_to_oz(user, users[user].password,
                              hosts[host_name]['hostname'])

    provider_api = ProviderApi(user_client)
    providers = provider_api.oz_providers_list().providers

    for pid in providers:
        provider = provider_api.get_provider_details(pid)
        if provider.name == provider_name:
            assert provider.domain == domain, 'Provider has domain {} instead' \
                                              ' of {}'.format(provider.domain, 
                                                              domain)
            break
    else:
        raise RuntimeError('Couldn\'t find provider '
                           'named "{}"'.format(provider_name))


def assert_there_is_no_provider_in_oz_rest(user, users, host_name, hosts,
                                           provider_alias):
    user_client = login_to_oz(user, users[user].password,
                              hosts[host_name]['hostname'])
    provider_name = hosts[provider_alias]['name']

    assert not get_provider_with_name(user_client, provider_name), \
        'There is provider {} in {} oz service'.format(provider_name,
                                                       host_name)
