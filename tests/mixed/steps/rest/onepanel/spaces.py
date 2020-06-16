"""Utils and fixtures to facilitate spaces operations in Onepanel
using REST API.
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import re

import yaml

from tests.gui.conftest import WAIT_BACKEND
from tests.mixed.utils.common import (login_to_panel, login_to_oz)
from tests.mixed.steps.rest.onezone.common import get_space_with_name
from tests.mixed.onepanel_client import (OneproviderApi,
                                         StorageUpdateDetails,
                                         SpaceModifyRequest,
                                         StorageImportDetails,
                                         SpaceSupportRequest)
from tests.utils.utils import repeat_failed

attrs_mapping = {
        'Delete enabled': 'Delete enable',
        'Scan interval [s]': 'Scan interval',
        'Import strategy': 'strategy',
        'Update strategy': 'strategy',
    }


def revoke_space_support_in_op_panel_using_rest(user, users, provider_host,
                                                hosts, space_name,
                                                admin_credentials,
                                                onepanel_credentials,
                                                zone_host='onezone'):
    user_client_op = login_to_panel(user, users[user].password,
                                    hosts[provider_host]['hostname'])
    if user == onepanel_credentials.username:
        user = admin_credentials.username
    user_client_oz = login_to_oz(user, users[user].password,
                                 hosts[zone_host]['hostname'])

    provider_api = OneproviderApi(user_client_op)
    space = get_space_with_name(user_client_oz, space_name)
    provider_api.revoke_space_support(space.space_id)


def support_space_in_op_panel_using_rest(user, provider_host, hosts, users,
                                         tmp_memory, config):
    user_client = login_to_panel(user, users[user].password,
                                 hosts[provider_host]['hostname'])

    provider_api = OneproviderApi(user_client)

    options = yaml.load(config)

    storage_import_options = options.get('storage import', None)
    if storage_import_options:
        strategy = '_'.join(storage_import_options['strategy'].lower().
                            split())
        max_depth = storage_import_options.get('max depth', None)
        storage_import = StorageImportDetails(strategy, max_depth)
    else:
        storage_import = None
    storage_update = StorageUpdateDetails(strategy='no_update')

    storages = provider_api.get_storages().ids
    storage_name = re.sub(r' \(.*\)', '', options['storage'])
    for storage_id in storages:
        storage = provider_api.get_storage_details(storage_id)
        if storage.name == storage_name:
            space_support_rq = SpaceSupportRequest(
                token=tmp_memory[user]['mailbox']['token'],
                size=options['size'],
                storage_id=storage_id,
                storage_import=storage_import,
                storage_update=storage_update)
            provider_api.support_space(space_support_rq)
            break
    else:
        raise RuntimeError('No storage named "{}"'.format(storage_name))


def configure_sync_parameters_for_space_in_op_panel_rest(user, users,
                                                         provider_host, hosts,
                                                         conf, space_name,
                                                         sync_type,
                                                         onepanel_credentials,
                                                         admin_credentials):
    user_client_op = login_to_panel(user, users[user].password,
                                    hosts[provider_host]['hostname'])
    if user == onepanel_credentials.username:
        user = admin_credentials.username
    user_client_oz = login_to_oz(user, users[user].password,
                                 hosts['onezone']['hostname'])

    provider_api = OneproviderApi(user_client_op)
    options = yaml.load(conf)
    if options['{} strategy'.format(
            sync_type.capitalize())].lower() == 'disabled':
        strategy = 'no_{}'.format(sync_type.lower())
    else:
        strategy = '_'.join(options['{} strategy'.
                            format(sync_type.capitalize())].lower().split())

    if sync_type.lower() == 'import':
        storage_import = StorageImportDetails(strategy, options['Max depth'])
        space_modify_rq = SpaceModifyRequest(storage_import=storage_import)
    else:
        storage_update = StorageUpdateDetails(
            strategy,
            options.get('Max depth', None),
            options.get('Scan interval [s]', None),
            options.get('Write once', None),
            options.get('Delete enabled', None)
        )
        space_modify_rq = SpaceModifyRequest(storage_update=storage_update)

    space = get_space_with_name(user_client_oz, space_name)
    provider_api.modify_space(space.space_id, space_modify_rq)


@repeat_failed(timeout=WAIT_BACKEND*4)
def assert_proper_space_configuration_in_op_panel_rest(space_name, user, users,
                                                       provider_host, hosts,
                                                       conf, sync_type,
                                                       onepanel_credentials,
                                                       admin_credentials,
                                                       zone_host='onezone'):
    user_client_op = login_to_panel(user, users[user].password,
                                    hosts[provider_host]['hostname'])
    if user == onepanel_credentials.username:
        user = admin_credentials.username
    user_client_oz = login_to_oz(user, users[user].password,
                                 hosts[zone_host]['hostname'])

    provider_api = OneproviderApi(user_client_op)
    space = get_space_with_name(user_client_oz, space_name)
    space_details = provider_api.get_space_details(space.space_id)

    sync_type = sync_type.lower()
    storage_sync = getattr(space_details,
                           'storage_{}'.format(sync_type))

    for attr, expected_val in yaml.load(conf).items():
        if 'strategy' in attr:
            if expected_val.lower() == 'disabled':
                expected_val = 'no_{}'.format(sync_type)
            else:
                expected_val = '_'.join(expected_val.lower().split())
        try:
            actual_val = getattr(
                storage_sync, '_'.join(attrs_mapping[attr].lower().split()))
        except KeyError:
            actual_val = getattr(storage_sync,
                                 '_'.join(attr.lower().split()))
        assert expected_val == actual_val, \
            'Storage sync value for attribute "{}" does not match. ' \
            'Expected: {}, got: {}'.format(attr, expected_val, actual_val)
