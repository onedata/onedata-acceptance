"""This module contains gherkin steps to run acceptance tests featuring
storage parameter modifications in Onepanel using REST API in Oneclient tests.
"""
from tests.gui.meta_steps.onezone.provider import \
    send_copied_invite_token_in_oz_gui

__author__ = "Bartek Kryza"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

# from tests.gui.conftest import WAIT_BACKEND
# from tests.utils.entities_setup.spaces import force_start_storage_scan
from tests.utils.bdd_utils import wt, then, parsers
# from tests.utils.utils import repeat_failed
# from tests.mixed.utils.common import NoSuchClientException


@wt(parsers.parse('using REST, {user} changes storage "{type}" named "{storage}" '
                  'parameter "{parameter}" to "{value}" at provider "{provider}"'))
def modify_storage_parameter(user, type, storage, parameter, value, provider,
                             storages, hosts, onepanel_credentials):
    from tests.oneclient.steps.rest.onepanel.storages import \
        modify_storage_parameters

    storage_id = storages[provider][storage]

    for host in hosts:
        if 'name' in hosts[host] and hosts[host]['name'] == provider:
            onepanel_host = hosts[host]['hostname']

    modify_params = {'type': type, parameter: value}
    modify_storage_parameters(user, provider, storage_id, storage,
                              modify_params, onepanel_host,
                              onepanel_credentials)
    pass
