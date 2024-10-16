"""Utils and fixtures to facilitate provider operations in Onepanel
using REST API.
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import yaml
from onepanel_client import OneproviderApi, ProviderDetails, ProviderRegisterRequest
from tests.mixed.utils.common import login_to_panel


def modify_provider_in_op_panel_using_rest(
    user, users, provider_host, hosts, new_provider_name, new_domain
):
    user_client = login_to_panel(
        user, users[user].password, hosts[provider_host]["hostname"]
    )

    provider_api = OneproviderApi(user_client)
    provider_mod_rq = ProviderDetails(
        name=new_provider_name, subdomain_delegation=False, domain=new_domain
    )
    provider_api.modify_provider(provider_mod_rq)


def deregister_provider_in_op_panel_using_rest(user, users, provider_host, hosts):
    user_client = login_to_panel(
        user, users[user].password, hosts[provider_host]["hostname"]
    )

    provider_api = OneproviderApi(user_client)
    provider_api.remove_provider()


def register_provider_in_op_using_rest(user, users, hosts, config):
    options = yaml.load(config, yaml.Loader)

    try:
        provider = options["provider name"]["of provider"]
    except KeyError:
        provider_name = options["provider_name"]

    else:
        provider_name = hosts[provider]["name"]

    user_client = login_to_panel(user, users[user].password, provider_name)
    provider_api = OneproviderApi(user_client)

    try:
        provider = options["domain"]["of provider"]
    except KeyError:
        domain = options["domain"]
    else:
        domain = hosts[provider]["hostname"]

    try:
        zone = options["zone domain"]["of zone"]
    except KeyError:
        onezone_domain_name = options["zone domain"]
    else:
        onezone_domain_name = hosts[zone]["hostname"]

    provider_register_rq = ProviderRegisterRequest(
        name=provider_name,
        subdomain_delegation=False,
        domain=domain,
        onezone_domain_name=onezone_domain_name,
        admin_email=options["admin email"],
    )
    provider_api.add_provider(provider_register_rq)

    storages_ids = provider_api.get_storages().ids
    storages = {
        provider_api.get_storage_details(
            storage_id
        ).name: provider_api.get_storage_details(storage_id)
        for storage_id in storages_ids
    }

    for storage_name, storage_options in options["storages"].items():
        assert (
            storage_name in storages
        ), f"No storage named: {storage_name} for provider {provider_name}"

        for field in ("type", "insecure", "readonly"):
            expected_val = storage_options.get(field, None)
            if expected_val:
                actual_val = getattr(storages[storage_name], field)
                assert expected_val == actual_val, (
                    f"Attribute {field} for storage named {storage_name} does"
                    f" not match expected value. Expected: {expected_val}, got:"
                    f" {actual_val}"
                )
