"""This module contains gherkin steps to run acceptance tests featuring
basic operations in Onepanel using REST API mixed with web GUI.
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from pytest_bdd import when, given, then, parsers
from tests.gui.conftest import WAIT_BACKEND
from tests.gui.utils.generic import repeat_failed
from tests.gui.meta_steps.oneprovider.data import assert_space_content_in_op_gui
from tests.mixed_swaggers.utils.common import NoSuchClientException


@when(parsers.re('using (?P<client>.*), (?P<user>.+?) changes his '
                 'password to "(?P<new_password>.+?)" in "(?P<host>.+?)" '
                 'Onezone panel service'))
def change_user_password_in_oz_panel(client, request, user, new_password, host,
                                     selenium, onepage, users, hosts, popups):

    if client.lower() == 'web gui':
        from tests.gui.meta_steps.onepanel.account_management import \
                                    change_user_password_in_oz_panel_using_gui
        change_user_password_in_oz_panel_using_gui(selenium, user, onepage,
                                                   users, new_password, popups)
    elif client.lower() == 'rest':
        from tests.mixed_swaggers.utils.onepanel.account_management import \
                                    change_user_password_in_oz_panel_using_rest
        change_user_password_in_oz_panel_using_rest(user, new_password, host,
                                                    users, hosts)
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>.+?) logs out from '
                 '"(?P<host>.+?)" Onezone panel service'))
def log_out_from_oz_panel(client, request, user, host, selenium, onepage,
                          panel_login_page, popups):

    if client.lower() == 'web gui':
        from tests.gui.meta_steps.onepanel.account_management import \
                                    log_out_from_oz_panel_gui
        log_out_from_oz_panel_gui(user, selenium, onepage, panel_login_page,
                                  popups)
    elif client.lower() == 'rest':
        pass
        # pytest.skip('This step is not required using {} client'.format(client))
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@then(parsers.re('using (?P<client>.*), (?P<user>.+?) successfully '
                 'logs in to "(?P<host>.+?)" Onezone panel service using '
                 'password "(?P<password>.+?)"'))
def login_to_oz_panel_using_new_password(client, request, user, host, selenium,
                                         panel_login_page, hosts, password):

    if client.lower() == 'web gui':
        from tests.gui.meta_steps.onepanel.account_management import \
                                    login_to_oz_panel_using_new_password_gui
        login_to_oz_panel_using_new_password_gui(selenium, user, password,
                                                 panel_login_page)
    elif client.lower() == 'rest':
        from tests.mixed_swaggers.utils.onepanel.account_management import \
                                    login_to_oz_panel_using_new_password_rest
        login_to_oz_panel_using_new_password_rest(user, password, hosts,
                                                  host)
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>.+?) modifies '
                 'provider "(?P<provider_name>.+?)" changing his name to '
                 '"(?P<new_provider_name>.+?)" and domain to test domain in '
                 '"(?P<host>.+?)" Oneprovider panel service'))
def modify_provider_using_test_hostname_in_op_panel(client, request, user,
                                                    provider_name,
                                                    new_provider_name,
                                                    host, users, hosts,
                                                    selenium, onepanel,
                                                    panel_login_page,
                                                    modals):

    test_domain = '{}.test'.format(hosts[provider_name]['hostname'])

    if client.lower() == 'rest':
        from tests.mixed_swaggers.utils.onepanel.provider import \
                                    modify_provider_in_op_panel_using_rest
        modify_provider_in_op_panel_using_rest(user, users, host, hosts,
                                               new_provider_name, test_domain)
    elif client.lower() == 'web gui':
        from tests.gui.meta_steps.onepanel.provider import \
                                    modify_provider_with_given_name_in_op_panel_using_gui
        modify_provider_with_given_name_in_op_panel_using_gui(
            selenium, user, onepanel, hosts[provider_name]['name'],
            new_provider_name, test_domain, panel_login_page, users,
            hosts, user, modals)
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@then(parsers.re('using (?P<client>.*), (?P<user>.+?) modifies provider named '
                 '"(?P<provider_name>.+?)" changing his name and '
                 'domain to match that of "(?P<target_provider>.+?)" provider '
                 'in "(?P<host>.+?)" Oneprovider panel service'))
def modify_provider_using_known_hostname_in_op_panel(client, request, user,
                                                     provider_name,
                                                     target_provider, host,
                                                     users, hosts, selenium,
                                                     onepanel, panel_login_page,
                                                     modals):

    if client.lower() == 'rest':
        from tests.mixed_swaggers.utils.onepanel.provider import \
                                    modify_provider_in_op_panel_using_rest
        modify_provider_in_op_panel_using_rest(user, users, host, hosts,
                                               hosts[target_provider]['name'],
                                               hosts[target_provider]['hostname'])
    elif client.lower() == 'web gui':
        from tests.gui.meta_steps.onepanel.provider import \
                                    modify_provider_with_given_name_in_op_panel_using_gui
        modify_provider_with_given_name_in_op_panel_using_gui(
            selenium, user, onepanel, provider_name,
            hosts[target_provider]['name'],
            hosts[target_provider]['hostname'], panel_login_page, users, hosts,
            user, modals)
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@then(parsers.re('using (?P<client>.*), (?P<user>.+?) sees provider named '
                 '"(?P<provider_name>.+?)" with test hostname of provider '
                 '"(?P<provider>.+?)" in "(?P<host>.+?)" Onezone service'))
def assert_provider_has_given_name_and_test_hostname_in_oz(client, request, user,
                                                           provider_name, provider,
                                                           host, users, hosts,
                                                           selenium, oz_page):

    test_domain = '{}.test'.format(hosts[provider]['hostname'])

    if client.lower() == 'rest':
        from tests.mixed_swaggers.utils.onezone.provider import \
                                assert_provider_has_name_and_hostname_in_oz_rest
        assert_provider_has_name_and_hostname_in_oz_rest(user, users, host,
                                                         hosts, provider_name,
                                                         test_domain)
    elif client.lower() == 'web gui':
        from tests.gui.meta_steps.onezone.provider import \
                                assert_provider_has_name_and_hostname_in_oz_gui
        assert_provider_has_name_and_hostname_in_oz_gui(selenium, user, oz_page,
                                                        provider_name, provider,
                                                        hosts, with_refresh=True,
                                                        test_domain=True)
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>.+?) deregisters '
                 'provider in "(?P<host>.+?)" Oneprovider panel service'))
def deregister_provider_in_op_panel(client, request, user, host, hosts, 
                                    selenium, onepanel, popups, users):

    if client.lower() == 'rest':
        from tests.mixed_swaggers.utils.onepanel.provider import \
                                    deregister_provider_in_op_panel_using_rest
        deregister_provider_in_op_panel_using_rest(user, users, host, hosts)
    elif client.lower() == 'web gui':
        from tests.gui.meta_steps.onepanel.provider import \
                                    deregister_provider_in_op_panel_using_gui
        deregister_provider_in_op_panel_using_gui(selenium, user, host,
                                                  onepanel, popups, hosts)
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@then(parsers.re('using (?P<client>.*), (?P<user>.+?) sees that '
                 'provider "(?P<provider_name>.+?)" has been deregistered in '
                 '"(?P<host>.+?)" Onezone service'))
def assert_there_is_no_provider_in_oz(client, request, user, provider_name,
                                      host, hosts, users, selenium,
                                      oz_page):

    if client.lower() == 'rest':
        from tests.mixed_swaggers.utils.onezone.provider import \
                                    assert_there_is_no_provider_in_oz_rest
        assert_there_is_no_provider_in_oz_rest(user, users, host, hosts,
                                               provider_name)
    elif client.lower() == 'web gui':
        from tests.gui.meta_steps.onezone.provider import \
                                    assert_there_is_no_provider_in_oz_gui
        assert_there_is_no_provider_in_oz_gui(
            selenium, user, oz_page, provider_name, hosts)
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@then(parsers.re('using (?P<client>.*), (?P<user>.+?) sees that '
                 'provider "(?P<provider_name>.+?)" does not support '
                 'space named "(?P<space_name>.+?)" in "(?P<host>.+?)" '
                 'Onezone service'))
def assert_provider_does_not_support_space_in_oz(client, request, user,
                                                 provider_name, space_name,
                                                 host, hosts, selenium,
                                                 oz_page, users):

    if client.lower() == 'rest':
        from tests.mixed_swaggers.utils.onezone.space_management import \
                            assert_provider_does_not_support_space_in_oz_rest
        assert_provider_does_not_support_space_in_oz_rest(
            user, users, host, hosts, space_name, provider_name)
    elif client.lower() == 'web gui':
        from tests.gui.meta_steps.onezone.spaces import \
                            assert_provider_does_not_support_space_in_oz_gui
        assert_provider_does_not_support_space_in_oz_gui(
            selenium, user, oz_page, space_name, provider_name, hosts)
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>.+?) registers '
                 'provider in "(?P<host>.+?)" Onezone service with following '
                 'configuration:\n(?P<config>(.|\s)*)'))
@then(parsers.re('using (?P<client>.*), (?P<user>.+?) registers '
                 'provider in "(?P<host>.+?)" Onezone service with following '
                 'configuration:\n(?P<config>(.|\s)*)'))
def register_provider_in_op(client, request, user, hosts, users, selenium,
                            onepanel, config, modals):
    """ Register provider according to given config.

    config should be in yaml format exactly as seen in panel, e.g.

        provider name: oneprovider-1
        OR
        provider name:
            of provider: oneprovider-1

        domain: node1.oneprovider-1.local
        OR
        domain:
            of provider: provider_name      --> in first case it
                                            will use given domain name
                                            in second case it will use
                                            domain name of given
                                            provider
        zone domain: node1.onezone
        OR
        zone domain:
            of zone: zone_name              --> in first case it
                                            will use given domain
                                            in second case it will use
                                            ip of given zone
        storage:
            name: NFS
            type: posix
            mount point: /volumes/storage

    """

    if client.lower() == 'rest':
        from tests.mixed_swaggers.utils.onepanel.provider import \
                                            register_provider_in_op_using_rest
        register_provider_in_op_using_rest(user, users, hosts, config)
    elif client.lower() == 'web gui':
        from tests.gui.meta_steps.onepanel.provider import \
                                            register_provider_in_op_using_gui
        register_provider_in_op_using_gui(selenium, user, onepanel, hosts,
                                          config, modals)
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>.+?) generates space support '
                 'token for space named "(?P<space_name>.+?)" in '
                 '"(?P<host>.+?)" Onezone service and sends it to '
                 '(?P<supporting_user>.+)'))
@then(parsers.re('using (?P<client>.*), (?P<user>.+?) generates space support '
                 'token for space named "(?P<space_name>.+?)" in '
                 '"(?P<host>.+?)" Onezone service and sends it to '
                 '(?P<supporting_user>.+)'))
def request_space_support(client, request, user, space_name,
                          host, hosts, users, selenium,
                          tmp_memory, oz_page, modals, displays, clipboard,
                          supporting_user):

    if client.lower() == 'rest':
        from tests.mixed_swaggers.utils.onezone.space_management import \
                                            request_space_support_using_rest
        request_space_support_using_rest(user, users, space_name, host, hosts,
                                         tmp_memory, supporting_user)
    elif client.lower() == 'web gui':
        from tests.gui.meta_steps.onezone.spaces import \
                                            request_space_support_using_gui
        request_space_support_using_gui(selenium, user, oz_page,
                                        space_name, tmp_memory, modals,
                                        displays, clipboard, supporting_user)
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>.+?) supports '
                 '"(?P<space_name>.*)" space in "(?P<host>.+?)" Oneprovider '
                 'panel service with following configuration:\n'
                 '(?P<config>(.|\s)*)'))
@then(parsers.re('using (?P<client>.*), (?P<user>.+?) supports '
                 '"(?P<space_name>.*)" space in "(?P<host>.+?)" Oneprovider '
                 'panel service with following configuration:\n'
                 '(?P<config>(.|\s)*)'))
def support_space_in_op_panel(client, request, user, selenium, tmp_memory,
                              onepanel, users, hosts, host, config, space_name):
    """ Support space according to given config.

    Config format given in yaml is as follow:

        space_name:
            provider: provider_name             --> required
            storage: storage_name               --> required
            size: 1000                          --> required
            mount in root: True/False           --> optional
            storage import:                     --> optional
                strategy: Simple Scan           --> required if storage import
                                                option is used
                max depth: 2                    --> optional

    """

    if client.lower() == 'web gui':
        from tests.gui.meta_steps.onepanel.spaces import \
                                        support_space_in_op_panel_using_gui
        support_space_in_op_panel_using_gui(selenium, user, config, onepanel,
                                            tmp_memory, space_name, host, hosts)
    elif client.lower() == 'rest':
        from tests.mixed_swaggers.utils.onepanel.spaces import \
                                        support_space_in_op_panel_using_rest
        support_space_in_op_panel_using_rest(user, host, hosts, users,
                                             tmp_memory, config)
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>.+?) sees that list '
                 'of supporting providers for space named '
                 '"(?P<space_name>.+?)" contains "(?P<provider_name>.+?)" in '
                 '"(?P<host>.+?)" Onezone service'))
@then(parsers.re('using (?P<client>.*), (?P<user>.+?) sees that list '
                 'of supporting providers for space named '
                 '"(?P<space_name>.+?)" contains "(?P<provider_name>.+?)" in '
                 '"(?P<host>.+?)" Onezone service'))
def w_assert_space_is_supported_by_provider_in_oz(client, request, user,
                                                  space_name, provider_name,
                                                  host, selenium,
                                                  oz_page, hosts, users):

    if client.lower() == 'web gui':
        from tests.gui.meta_steps.onezone.spaces import \
                                assert_space_is_supported_by_provider_in_oz_gui
        assert_space_is_supported_by_provider_in_oz_gui(selenium, user, oz_page,
                                                        space_name,
                                                        provider_name, hosts,
                                                        with_refresh=True)
    elif client.lower() == 'rest':
        from tests.mixed_swaggers.utils.onezone.space_management import \
                                assert_space_is_supported_by_provider_in_oz_rest
        assert_space_is_supported_by_provider_in_oz_rest(user, users, host,
                                                         hosts, space_name,
                                                         provider_name)
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>.+?) revokes '
                 '"(?P<provider_name>.+?)" provider space support for space '
                 'named "(?P<space_name>.+?)" in "(?P<host>.+?)" Oneprovider '
                 'panel service'))
@then(parsers.re('using (?P<client>.*), (?P<user>.+?) revokes '
                 '"(?P<provider_name>.+?)" provider space support for space '
                 'named "(?P<space_name>.+?)" in "(?P<host>.+?)" Oneprovider '
                 'panel service'))
def revoke_space_support_in_op_panel(client, request, user, space_name,
                                     provider_name, host, selenium, onepanel,
                                     popups, modals, users, hosts):

    if client.lower() == 'web gui':
        from tests.gui.meta_steps.onepanel.spaces import \
                                    revoke_space_support_in_op_panel_using_gui
        revoke_space_support_in_op_panel_using_gui(selenium, user,
                                                   provider_name, onepanel,
                                                   space_name, popups, modals,
                                                   hosts)
    elif client.lower() == 'rest':
        from tests.mixed_swaggers.utils.onepanel.spaces import \
                                    revoke_space_support_in_op_panel_using_rest
        revoke_space_support_in_op_panel_using_rest(user, users, host, hosts,
                                                    space_name)
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@when(parsers.re('using docker, (?P<user>.+?) copies (?P<src_path>.+?) '
                 'to provider\'s storage mount point'))
def cp_files_to_storage_mount_point(user, src_path, tmpdir, hosts):
    from tests.gui.steps.common.docker import wt_cp_files_to_storage_mount_point
    wt_cp_files_to_storage_mount_point(user, src_path, tmpdir, hosts)


@when(parsers.re('using docker, (?P<user>.+?) copies (?P<src_path>.+?) '
                 'to the root directory of "(?P<space_name>.+?)" space'))
def cp_files_to_space_root_dir(user, src_path, space_name, tmpdir, tmp_memory,
                               hosts):
    from tests.gui.steps.common.docker import wt_cp_files_to_space_root_dir
    wt_cp_files_to_space_root_dir(user, src_path, space_name, tmpdir,
                                  tmp_memory, hosts)


@when(parsers.re('using docker, (?P<user>.+?) copies (?P<src_path>.+?) '
                 'to (?P<dst_path>.+?) regular directory of '
                 '"(?P<space_name>.+?)" space'))
def cp_files_to_space_root_dir(user, src_path, dst_path, space_name, tmpdir,
                               tmp_memory, hosts):
    from tests.gui.steps.common.docker import wt_cp_files_to_dst_path_in_space
    wt_cp_files_to_dst_path_in_space(user, src_path, dst_path, space_name,
                                     tmpdir, tmp_memory, hosts)


@when(parsers.re('using (?P<client>.*), (?P<user>.+?) sees that '
                 '(?P<sync_type>IMPORT|UPDATE) strategy configuration for '
                 '"(?P<space>.+?)" in "(?P<host>.+?)" is as follow:\n'
                 '(?P<config>(.|\s)*)'))
def assert_proper_space_configuration_in_op_panel(client, request, user,
                                                  sync_type, space, config,
                                                  selenium, onepanel,
                                                  users, host, hosts):
    """Assert configuration displayed in space record in panel.

    config should be in yaml format exactly as seen in panel, e.g.

    For update strategy:

        Update strategy: Simple scan
        Max depth: 20
        Scan interval [s]: 10
        Write once: true
        Delete enabled: false

    For import strategy:

        Import strategy: Simple scan
        Max depth: 2

    """

    if client.lower() == 'web gui':
        from tests.gui.meta_steps.onepanel.spaces import \
                            assert_proper_space_configuration_in_op_panel_gui
        assert_proper_space_configuration_in_op_panel_gui(selenium, user, space,
                                                          onepanel, sync_type,
                                                          config, host, hosts)
    elif client.lower() == 'rest':
        from tests.mixed_swaggers.utils.onepanel.spaces import \
                            assert_proper_space_configuration_in_op_panel_rest
        assert_proper_space_configuration_in_op_panel_rest(space, user, users,
                                                           host, hosts,
                                                           config, sync_type)
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>.+?) configures '
                 '(?P<sync_type>IMPORT|UPDATE) parameters for '
                 '"(?P<space_name>.+?)" in "(?P<host>.+?)" Oneprovider panel '
                 'service as follow:\n(?P<config>(.|\s)*)'))
def configure_sync_parameters_for_space_in_op_panel(client, request, user,
                                                    sync_type, space_name, host,
                                                    config, selenium, onepanel,
                                                    popups, users, hosts):
    """Configure synchronization parameters for space.

    config should be in yaml format exactly as seen in panel, e.g.

    For update strategy:

        Update strategy: Simple scan
        Max depth: 20
        Scan interval [s]: 10
        Write once: true
        Delete enabled: false

    For import strategy:

        Import strategy: Simple scan
        Max depth: 2

    """

    if client.lower() == 'web gui':
        from tests.gui.meta_steps.onepanel.spaces import \
                            configure_sync_parameters_for_space_in_op_panel_gui
        configure_sync_parameters_for_space_in_op_panel_gui(selenium, user,
                                                            space_name,
                                                            onepanel, popups,
                                                            config, sync_type)
    elif client.lower() == 'rest':
        from tests.mixed_swaggers.utils.onepanel.spaces import \
                            configure_sync_parameters_for_space_in_op_panel_rest
        configure_sync_parameters_for_space_in_op_panel_rest(user, users, host,
                                                             hosts, config,
                                                             space_name,
                                                             sync_type)
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>.+?) sees that '
                 'content for "(?P<space_name>.+?)" in "(?P<host>.+?)" '
                 'Oneprovider service is as follow:\n(?P<config>(.|\s)*)'))
@repeat_failed(timeout=WAIT_BACKEND, interval=1.5)
def assert_space_content_in_op(client, request, config, selenium, user,
                               op_page, tmp_memory, tmpdir, users, hosts,
                               space_name, spaces, host, oz_page):
    """ Assert space has given content in provider.

     space content format given in yaml is as follow:

        - dir1: 5                       --> if item name startswith 'dir' it is
                                        considered directory otherwise a file;
                                        with given num, [num] items should be
                                        in directory
        - dir2:
            - dir22
            - file1.txt: 2222           --> when specifying file,
                                        one can specify it's
                                        content as well

    """

    if client.lower() == 'web gui':
        from tests.gui.meta_steps.oneprovider.data import \
                                                assert_space_content_in_op_gui
        assert_space_content_in_op_gui(config, selenium, user, op_page,
                                       tmp_memory, tmpdir, space_name, oz_page,
                                       host, hosts)
    elif client.lower() == 'rest':
        from tests.mixed_swaggers.utils.oneprovider.data import \
                                                assert_space_content_in_op_rest
        assert_space_content_in_op_rest(user, users, hosts, config, space_name,
                                        spaces, host)
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@when(parsers.re('using docker, (?P<user>.+?) removes (?P<src_path>.+?) '
                 'from the root directory of "(?P<space_name>.+?)" space'))
def rm_files_from_space_root_dir(user, src_path, space_name, tmp_memory, hosts):
    from tests.gui.steps.common.docker import wt_rm_files_to_space_root_dir
    wt_rm_files_to_space_root_dir(src_path, space_name, tmp_memory, hosts)


@when(parsers.re('using (?P<client>.*), (?P<user>.+?) copies Id of '
                 '"(?P<space_name>.+?)" space in Spaces page in Onepanel'))
def copy_id_of_space(client, request, user, space_name, selenium, onepanel,
                     tmp_memory, users, hosts):

    if client.lower() == 'web gui':
        from tests.gui.meta_steps.onepanel.spaces import \
                                                        copy_id_of_space_gui
        copy_id_of_space_gui(selenium, user, space_name, onepanel, tmp_memory)
    elif client.lower() == 'rest':
        from tests.mixed_swaggers.utils.onezone.space_management import \
                                                        copy_id_of_space_rest
        copy_id_of_space_rest(user, users, hosts, space_name, tmp_memory)
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>.+?) is idle for '
                 '(?P<seconds>\d*\.?\d+([eE][-+]?\d+)?) seconds'))
def remove_spaces_in_oz(client, request, user, seconds):
    from tests.gui.steps.common.miscellaneous import wait_given_time
    wait_given_time(seconds)


@given(parsers.re('using web GUI, (?P<user>.+?) sees "(?P<provider>.+?)" '
                  'provider in CLUSTERS sidebar in Onepanel'))
def see_provider_in_cluster_sidebar_in_onepanel(user, provider, selenium, hosts,
                                                onepanel, panel_login_page,
                                                users, modals):
    from tests.gui.meta_steps.onepanel.provider import \
        change_provider_name_if_name_is_different_than_given
    change_provider_name_if_name_is_different_than_given(selenium, user,
                                                         provider, hosts,
                                                         onepanel,
                                                         panel_login_page,
                                                         users, modals)


@given(parsers.re('using web GUI, (?P<user>.+?) refreshes site'))
def refresh_site(selenium, user):
    selenium[user].refresh()
