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
from tests.mixed.onepanel_client import (
    OneproviderApi, SpaceModifyRequest, SpaceSupportRequest,
    AutoStorageImportConfig, StorageImport)
from tests.utils.utils import repeat_failed


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
        max_depth = storage_import_options.get('max depth', None)
        continuous_scan = storage_import_options.get('continuous scan', True)
        modifications = storage_import_options.get('detect modifications', True)
        deletions = storage_import_options.get('detect deletions', True)
        interval = storage_import_options.get('scan interval [s]', 60)
        sync_acl = storage_import_options.get('synchronize ACL', False)

        storage_import = StorageImport(
            mode='auto',
            auto_storage_import_config=AutoStorageImportConfig(
                max_depth=max_depth,
                sync_acl=sync_acl,
                continuous_scan=continuous_scan,
                scan_interval=interval,
                detect_modifications=modifications,
                detect_deletions=deletions))
    else:
        storage_import = None

    storages = provider_api.get_storages().ids
    storage_name = re.sub(r' \(.*\)', '', options['storage'])
    for storage_id in storages:
        storage = provider_api.get_storage_details(storage_id)
        if storage.name == storage_name:
            space_support_rq = SpaceSupportRequest(
                token=tmp_memory[user]['mailbox']['token'],
                size=options['size'], storage_id=storage_id,
                storage_import=storage_import)
            provider_api.support_space(space_support_rq)
            break
    else:
        raise RuntimeError(f'No storage named "{storage_name}"')

    import pdb
    pdb.set_trace()


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

    max_depth = options.get('max depth', None)
    continuous_scan = options.get('continuous scan', True)
    modifications = options.get('detect modifications', True)
    deletions = options.get('detect deletions', True)
    interval = options.get('scan interval [s]', 60)
    sync_acl = options.get('synchronize ACL', False)

    auto_storage_import_config = AutoStorageImportConfig(
        max_depth=max_depth,
        sync_acl=sync_acl,
        continuous_scan=continuous_scan,
        scan_interval=interval,
        detect_modifications=modifications,
        detect_deletions=deletions)

    space_modify_rq = SpaceModifyRequest(
        auto_storage_import_config=auto_storage_import_config)

    space = get_space_with_name(user_client_oz, space_name)
    provider_api.modify_space(space.space_id, space_modify_rq)


@repeat_failed(timeout=WAIT_BACKEND * 4)
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

    storage_sync = space_details.storage_import.auto_storage_import_config

    for attr, expected_val in yaml.load(conf).items():
        import pdb
        pdb.set_trace()
        actual_val = getattr(storage_sync, '_'.join(attr.lower().split()))
        assert expected_val == actual_val, (f'Storage sync value for attribute '
                                            f'"{attr}" does not match. '
                                            f'Expected: '
                                            f'{expected_val}, '
                                            f'got: {actual_val}')
