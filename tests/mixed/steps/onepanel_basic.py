"""This module contains gherkin steps to run acceptance tests featuring
basic operations in Onepanel using REST API mixed with web GUI.
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import Protocol, cast

from _pytest._py.path import LocalPath

from tests.gui.conftest import WAIT_BACKEND
from tests.gui.meta_steps.onepanel.account_management import (
    change_user_password_in_oz_panel_using_gui,
    log_out_from_oz_panel_gui,
    login_to_oz_panel_using_new_password_gui,
)
from tests.gui.meta_steps.onepanel.provider import (
    deregister_provider_in_op_panel_using_gui,
    modify_provider_with_given_name_in_op_panel_using_gui,
    register_provider_in_op_using_gui,
)
from tests.gui.meta_steps.onepanel.spaces import (
    assert_proper_space_configuration_in_op_panel_gui,
    configure_sync_parameters_for_space_in_op_panel_gui,
    copy_id_of_space_gui,
    revoke_space_support_in_op_panel_using_gui,
    run_scan_and_wait_till_finished,
    support_space_in_op_panel_using_gui,
)
from tests.gui.meta_steps.oneprovider.data import assert_space_content_in_op_gui
from tests.gui.meta_steps.onezone.provider import (
    assert_provider_has_name_and_hostname_in_oz_gui,
    assert_there_is_no_provider_in_oz_gui,
    send_copied_invite_token_in_oz_gui,
)
from tests.gui.meta_steps.onezone.spaces import (
    assert_provider_does_not_support_space_in_oz_gui,
    assert_space_is_supported_by_provider_in_oz_gui,
    request_space_support_using_gui,
)
from tests.gui.steps.common.docker import (
    wt_cp_files_to_dir_in_storage_mount_point,
    wt_cp_files_to_dst_path_in_space,
    wt_cp_files_to_space_root_dir,
    wt_cp_files_to_storage_mount_point,
    wt_rm_files_to_space_root_dir,
    wt_rm_files_to_storage_mount_point,
)
from tests.gui.type_definitions import Clipboard, TmpMemory
from tests.mixed.steps.rest.onepanel.account_management import (
    change_user_password_in_oz_panel_using_rest,
    login_to_oz_panel_using_new_password_rest,
)
from tests.mixed.steps.rest.onepanel.provider import (
    deregister_provider_in_op_panel_using_rest,
    modify_provider_in_op_panel_using_rest,
    register_provider_in_op_using_rest,
)
from tests.mixed.steps.rest.onepanel.spaces import (
    assert_proper_space_configuration_in_op_panel_rest,
    configure_sync_parameters_for_space_in_op_panel_rest,
    revoke_space_support_in_op_panel_using_rest,
    support_space_in_op_panel_using_rest,
)
from tests.mixed.steps.rest.oneprovider.data import assert_space_content_in_op_rest
from tests.mixed.steps.rest.onezone.provider import (
    assert_provider_has_name_and_hostname_in_oz_rest,
    assert_there_is_no_provider_in_oz_rest,
)
from tests.mixed.steps.rest.onezone.space_management import (
    assert_provider_does_not_support_space_in_oz_rest,
    assert_space_is_supported_by_provider_in_oz_rest,
    copy_id_of_space_rest,
    request_space_support_using_rest,
)
from tests.mixed.type_definitions import HostsConfig, Spaces
from tests.mixed.utils.common import NoSuchClientException
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt
from tests.utils.entities_setup.spaces import (
    force_start_storage_scan,
    wait_for_space_support,
    wait_for_storage_scan_to_finish,
)
from tests.utils.user_utils import User, Users
from tests.utils.utils import repeat_failed


class CredentialsLike(Protocol):
    username: str
    password: str


def _as_rest_hosts(hosts: Hosts) -> HostsConfig:
    return cast(HostsConfig, hosts)


def _as_credentials(credentials: User) -> CredentialsLike:
    return cast(CredentialsLike, credentials)


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) changes his "
        'password to "(?P<new_password>.+?)" in "(?P<host>.+?)" '
        "Onezone panel service"
    )
)
def change_user_password_in_oz_panel(
    client: str,
    user: str,
    new_password: str,
    host: str,
    selenium: SeleniumDrivers,
    users: Users,
    hosts: Hosts,
) -> None:

    if client.lower() == "web gui":

        change_user_password_in_oz_panel_using_gui(selenium, user, users, new_password)
    elif client.lower() == "rest":

        change_user_password_in_oz_panel_using_rest(
            user, new_password, host, users, hosts
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) logs out from "
        '"(?P<host>.+?)" Onezone panel service'
    )
)
def log_out_from_oz_panel(client: str, user: str, selenium: SeleniumDrivers) -> None:

    if client.lower() == "web gui":

        log_out_from_oz_panel_gui(user, selenium)
    elif client.lower() == "rest":
        pass
        # pytest.skip('This step is not required using {} client'.format(client))
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) successfully "
        'logs in to "(?P<host>.+?)" Onezone panel service using '
        'password "(?P<password>.+?)"'
    )
)
def login_to_oz_panel_using_new_password(
    client: str,
    user: str,
    host: str,
    selenium: SeleniumDrivers,
    hosts: Hosts,
    password: str,
) -> None:

    if client.lower() == "web gui":

        login_to_oz_panel_using_new_password_gui(selenium, user, password)
    elif client.lower() == "rest":

        login_to_oz_panel_using_new_password_rest(user, password, hosts, host)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) modifies "
        'provider "(?P<provider_name>.+?)" changing his name to '
        '"(?P<new_provider_name>.+?)" and domain to test domain in '
        '"(?P<host>.+?)" Oneprovider panel service'
    )
)
def modify_provider_using_test_hostname_in_op_panel(
    client: str,
    user: str,
    provider_name: str,
    new_provider_name: str,
    host: str,
    users: Users,
    hosts: Hosts,
    selenium: SeleniumDrivers,
) -> None:

    test_domain = f"{hosts[provider_name]['hostname']}.test"

    if client.lower() == "rest":

        modify_provider_in_op_panel_using_rest(
            user,
            users,
            host,
            _as_rest_hosts(hosts),
            new_provider_name,
            test_domain,
        )
    elif client.lower() == "web gui":

        modify_provider_with_given_name_in_op_panel_using_gui(
            selenium,
            user,
            hosts[provider_name]["name"],
            new_provider_name,
            test_domain,
            user,
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) modifies provider named "
        '"(?P<provider_name>.+?)" changing his name and '
        'domain to match that of "(?P<target_provider>.+?)" provider '
        'in "(?P<host>.+?)" Oneprovider panel service'
    )
)
def modify_provider_using_known_hostname_in_op_panel(
    client: str,
    user: str,
    provider_name: str,
    target_provider: str,
    host: str,
    users: Users,
    hosts: Hosts,
    selenium: SeleniumDrivers,
) -> None:

    if client.lower() == "rest":

        modify_provider_in_op_panel_using_rest(
            user,
            users,
            host,
            _as_rest_hosts(hosts),
            hosts[target_provider]["name"],
            hosts[target_provider]["hostname"],
        )
    elif client.lower() == "web gui":

        modify_provider_with_given_name_in_op_panel_using_gui(
            selenium,
            user,
            provider_name,
            hosts[target_provider]["name"],
            hosts[target_provider]["hostname"],
            user,
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) sees provider named "
        '"(?P<provider_name>.+?)" with test hostname of provider '
        '"(?P<provider>.+?)" in "(?P<host>.+?)" Onezone service'
    )
)
def assert_provider_has_given_name_and_test_hostname_in_oz(
    client: str,
    user: str,
    provider_name: str,
    provider: str,
    host: str,
    users: Users,
    hosts: Hosts,
    selenium: SeleniumDrivers,
) -> None:

    test_domain = f"{hosts[provider]['hostname']}.test"

    if client.lower() == "rest":

        assert_provider_has_name_and_hostname_in_oz_rest(
            user,
            users,
            host,
            _as_rest_hosts(hosts),
            provider_name,
            test_domain,
        )
    elif client.lower() == "web gui":

        assert_provider_has_name_and_hostname_in_oz_gui(
            selenium,
            user,
            provider_name,
            provider,
            hosts,
            with_refresh=True,
            test_domain=True,
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) deregisters "
        'provider in "(?P<host>.+?)" Oneprovider panel service'
    )
)
def deregister_provider_in_op_panel(
    client: str,
    user: str,
    host: str,
    hosts: Hosts,
    selenium: SeleniumDrivers,
    users: Users,
) -> None:

    if client.lower() == "rest":

        deregister_provider_in_op_panel_using_rest(
            user, users, host, _as_rest_hosts(hosts)
        )
    elif client.lower() == "web gui":

        deregister_provider_in_op_panel_using_gui(selenium, user, host, hosts)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) sees that "
        'provider "(?P<provider_name>.+?)" has been deregistered in '
        '"(?P<host>.+?)" Onezone service'
    )
)
def assert_there_is_no_provider_in_oz(
    client: str,
    user: str,
    provider_name: str,
    host: str,
    hosts: Hosts,
    users: Users,
    selenium: SeleniumDrivers,
) -> None:

    if client.lower() == "rest":

        assert_there_is_no_provider_in_oz_rest(
            user,
            users,
            host,
            _as_rest_hosts(hosts),
            provider_name,
        )
    elif client.lower() == "web gui":

        assert_there_is_no_provider_in_oz_gui(selenium, user, provider_name, hosts)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) sees that "
        'provider "(?P<provider_name>.+?)" does not support '
        'space named "(?P<space_name>.+?)" in "(?P<host>.+?)" '
        "Onezone service"
    )
)
def assert_provider_does_not_support_space_in_oz(
    client: str,
    user: str,
    provider_name: str,
    space_name: str,
    host: str,
    hosts: Hosts,
    selenium: SeleniumDrivers,
    users: Users,
) -> None:

    if client.lower() == "rest":

        assert_provider_does_not_support_space_in_oz_rest(
            user, users, host, hosts, space_name, provider_name
        )
    elif client.lower() == "web gui":

        assert_provider_does_not_support_space_in_oz_gui(
            selenium, user, space_name, provider_name, hosts
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) registers "
        'provider in "(?P<host>.+?)" Onezone service with following '
        r"configuration:\n(?P<config>(.|\s)*)"
    )
)
def register_provider_in_op(
    client: str,
    user: str,
    hosts: Hosts,
    users: Users,
    selenium: SeleniumDrivers,
    config: str,
    tmp_memory: TmpMemory,
) -> None:
    """Register provider according to given config.

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
            mount point: /volumes/posix

    """

    if client.lower() == "rest":

        register_provider_in_op_using_rest(user, users, _as_rest_hosts(hosts), config)
    elif client.lower() == "web gui":

        register_provider_in_op_using_gui(selenium, user, hosts, config, tmp_memory)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) generates space support "
        'token for space named "(?P<space_name>.+?)" in '
        '"(?P<host>.+?)" Onezone service and sends it to '
        "(?P<supporting_user>.+)"
    )
)
def request_space_support(
    client: str,
    user: str,
    space_name: str,
    host: str,
    hosts: Hosts,
    users: Users,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
    displays: dict[str, str],
    clipboard: Clipboard,
    supporting_user: str,
) -> None:

    if client.lower() == "rest":

        request_space_support_using_rest(
            user,
            users,
            space_name,
            host,
            hosts,
            tmp_memory,
            supporting_user,
        )
    elif client.lower() == "web gui":

        request_space_support_using_gui(
            selenium,
            user,
            space_name,
            tmp_memory,
            displays,
            clipboard,
            supporting_user,
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) supports "
        '"(?P<space_name>.*)" space in "(?P<host>.+?)" Oneprovider '
        "panel service with following configuration:\n"
        r"(?P<config>(.|\s)*)"
    )
)
@wt(
    parsers.re(
        "using (?P<client>REST), (?P<user>.+?) supports space with test alias "
        '"(?P<space_name>.*)" in "(?P<host>.+?)" Oneprovider '
        "panel service with following configuration:\n"
        r"(?P<config>(.|\s)*)"
    )
)
def support_space_in_op_panel(
    client: str,
    user: str,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
    users: Users,
    hosts: Hosts,
    host: str,
    config: str,
    space_name: str,
) -> None:
    """Support space according to given config.

    Config format given in yaml is as follows:

        space_name:
            provider: provider_name             --> required
            storage: storage_name               --> required
            size: 1000                          --> required
            mount in root: True/False           --> optional
            storage import:                     --> optional
                continuous scan: True/False     --> required if storage
                                                    import is used
                max depth: 2                    --> optional
                detect modifications: True/False
                detect deletions: True/False
                scan interval [s]: int

    """

    if client.lower() == "web gui":

        support_space_in_op_panel_using_gui(
            selenium,
            user,
            config,
            tmp_memory,
            space_name,
            host,
            hosts,
        )
    elif client.lower() == "rest":

        support_space_in_op_panel_using_rest(
            user, host, hosts, users, tmp_memory, config
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) sees that list "
        "of supporting providers for space named "
        '"(?P<space_name>.+?)" contains "(?P<provider_name>.+?)" in '
        '"(?P<host>.+?)" Onezone service'
    )
)
def w_assert_space_is_supported_by_provider_in_oz(
    client: str,
    user: str,
    space_name: str,
    provider_name: str,
    host: str,
    selenium: SeleniumDrivers,
    hosts: Hosts,
    users: Users,
) -> None:

    if client.lower() == "web gui":

        assert_space_is_supported_by_provider_in_oz_gui(
            selenium, user, space_name, provider_name, hosts
        )
    elif client.lower() == "rest":

        assert_space_is_supported_by_provider_in_oz_rest(
            user, users, host, hosts, space_name, provider_name
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) revokes "
        '"(?P<provider_name>.+?)" provider space support for space '
        'named "(?P<space_name>.+?)" in "(?P<host>.+?)" Oneprovider '
        "panel service"
    )
)
def revoke_space_support_in_op_panel(
    client: str,
    user: str,
    space_name: str,
    provider_name: str,
    host: str,
    selenium: SeleniumDrivers,
    users: Users,
    hosts: Hosts,
    admin_credentials: User,
    onepanel_credentials: User,
) -> None:

    if client.lower() == "web gui":

        revoke_space_support_in_op_panel_using_gui(
            selenium,
            user,
            provider_name,
            space_name,
            hosts,
        )
    elif client.lower() == "rest":

        revoke_space_support_in_op_panel_using_rest(
            user,
            users,
            host,
            hosts,
            space_name,
            _as_credentials(admin_credentials),
            _as_credentials(onepanel_credentials),
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using docker, (?P<user>.+?) copies (?P<src_path>.+?) "
        "to provider's storage mount point"
    )
)
def cp_files_to_storage_mount_point(
    user: str, src_path: str, tmpdir: LocalPath, hosts: Hosts
) -> None:

    wt_cp_files_to_storage_mount_point(user, src_path, tmpdir, hosts)


@wt(
    parsers.re(
        "using docker, (?P<user>.+?) copies (?P<src_path>.+?) "
        "to (?P<dst_path>.+?) provider's storage mount point"
    )
)
def cp_files_to_path_in_storage_mount_point(
    user: str, src_path: str, tmpdir: LocalPath, hosts: Hosts, dst_path: str
) -> None:

    wt_cp_files_to_dir_in_storage_mount_point(user, src_path, tmpdir, hosts, dst_path)


@wt(
    parsers.re(
        "using docker, (?P<user>.+?) copies (?P<src_path>.+?) "
        'to the root directory of "(?P<space_name>.+?)" space'
    )
)
def cp_files_to_space_root_dir(
    user: str,
    src_path: str,
    space_name: str,
    tmpdir: LocalPath,
    tmp_memory: TmpMemory,
    hosts: Hosts,
) -> None:

    wt_cp_files_to_space_root_dir(user, src_path, space_name, tmpdir, tmp_memory, hosts)


@wt(
    parsers.re(
        "using docker, (?P<user>.+?) copies (?P<src_path>.+?) "
        "to (?P<dst_path>.+?) regular directory of "
        '"(?P<space_name>.+?)" space'
    )
)
def cp_files_to_path_in_space_root_dir(
    user: str,
    src_path: str,
    dst_path: str,
    space_name: str,
    tmpdir: LocalPath,
    tmp_memory: TmpMemory,
    hosts: Hosts,
) -> None:

    wt_cp_files_to_dst_path_in_space(
        user, src_path, dst_path, space_name, tmpdir, tmp_memory, hosts
    )


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) sees that "
        "(?P<sync_type>import) strategy configuration for "
        '"(?P<space>.+?)" in "(?P<host>.+?)" is as follow:\n'
        r"(?P<config>(.|\s)*)"
    )
)
def assert_proper_space_configuration_in_op_panel(
    client: str,
    user: str,
    sync_type: str,
    space: str,
    config: str,
    selenium: SeleniumDrivers,
    users: Users,
    host: str,
    hosts: Hosts,
    onepanel_credentials: User,
    admin_credentials: User,
) -> None:
    """Assert configuration displayed in space record in panel.

    config should be in yaml format exactly as seen in panel, e.g.

    For import strategy:

        Continuous scan: true
        Max depth: 20
        Scan interval [s]: 10
        Detect modifications: true
        Detect deletions: false

    """

    if client.lower() == "web gui":

        assert_proper_space_configuration_in_op_panel_gui(
            selenium, user, space, sync_type, config, host, hosts
        )
    elif client.lower() == "rest":

        assert_proper_space_configuration_in_op_panel_rest(
            space,
            user,
            users,
            host,
            hosts,
            config,
            _as_credentials(onepanel_credentials),
            _as_credentials(admin_credentials),
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) configures "
        "import parameters for "
        '"(?P<space_name>.+?)" in "(?P<host>.+?)" Oneprovider panel '
        r"service as follow:\n(?P<config>(.|\s)*)"
    )
)
def configure_sync_parameters_for_space_in_op_panel(
    client: str,
    user: str,
    space_name: str,
    host: str,
    config: str,
    selenium: SeleniumDrivers,
    users: Users,
    hosts: Hosts,
    onepanel_credentials: User,
    admin_credentials: User,
) -> None:
    """Configure synchronization parameters for space.

    config should be in yaml format exactly as seen in panel, e.g.

     For import strategy:
        Max depth: 2
        Scan interval [s]: 10
        Detect modifications: true
        Detect deletions: true
        Synchronize ACL: false
        Continuous scan: true

    """

    if client.lower() == "web gui":

        configure_sync_parameters_for_space_in_op_panel_gui(selenium, user, config)
    elif client.lower() == "rest":

        configure_sync_parameters_for_space_in_op_panel_rest(
            user,
            users,
            host,
            hosts,
            config,
            space_name,
            _as_credentials(onepanel_credentials),
            _as_credentials(admin_credentials),
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) sees that "
        'content for "(?P<space_name>.+?)" in "(?P<host>.+?)" '
        r"Oneprovider service is as follow:\n(?P<config>(.|\s)*)"
    )
)
@repeat_failed(timeout=4 * WAIT_BACKEND, interval=1.5)
def assert_space_content_in_op(
    client: str,
    config: str,
    selenium: SeleniumDrivers,
    user: str,
    tmp_memory: TmpMemory,
    tmpdir: LocalPath,
    users: Users,
    hosts: Hosts,
    space_name: str,
    spaces: Spaces,
    host: str,
) -> None:
    """Assert space has given content in provider.

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

    if client.lower() == "web gui":

        assert_space_content_in_op_gui(
            config,
            selenium,
            user,
            tmp_memory,
            tmpdir,
            space_name,
        )
    elif client.lower() == "rest":

        assert_space_content_in_op_rest(
            user, users, hosts, config, space_name, spaces, host
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using docker, user removes (?P<src_path>.+?) "
        'from the root directory of "(?P<space_name>.+?)" space'
    )
)
def rm_files_from_space_root_dir(
    src_path: str, space_name: str, tmp_memory: TmpMemory, hosts: Hosts
) -> None:

    wt_rm_files_to_space_root_dir(src_path, space_name, tmp_memory, hosts)


@wt(
    parsers.re(
        "using docker, user removes (?P<src_path>.+?) "
        "from provider's storage mount point"
    )
)
def rm_files_from_storage_mount_point(src_path: str, hosts: Hosts) -> None:

    wt_rm_files_to_storage_mount_point(src_path, hosts)


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) copies Id of "
        '"(?P<space_name>.+?)" space in Spaces page in Onepanel'
    )
)
def copy_id_of_space(
    client: str,
    user: str,
    space_name: str,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
    users: Users,
    hosts: Hosts,
    admin_credentials: User,
    onepanel_credentials: User,
) -> None:

    if client.lower() == "web gui":

        copy_id_of_space_gui(selenium, user, space_name, tmp_memory)
    elif client.lower() == "rest":

        copy_id_of_space_rest(
            user,
            users,
            hosts,
            space_name,
            tmp_memory,
            _as_credentials(onepanel_credentials),
            _as_credentials(admin_credentials),
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        "using (?P<client>.*), (?P<user>.+?) sends copied invite token "
        "to (?P<send_to>.+?) user "
        'in "(?P<host>.+?)" Onezone service'
    )
)
def send_copied_invite_token(
    client: str,
    user: str,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
    displays: dict[str, str],
    clipboard: Clipboard,
    send_to: str,
) -> None:
    if client.lower() == "web gui":

        send_copied_invite_token_in_oz_gui(
            selenium, user, send_to, tmp_memory, displays, clipboard
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.parse(
        "using REST, {user} forces start of storage import scan for "
        '"{space}" at "{provider}"'
    )
)
def force_start_storage_import_scan(
    provider: str,
    space: str,
    spaces: Spaces,
    hosts: Hosts,
    onepanel_credentials: User,
) -> None:
    space_id = spaces[space]
    force_start_storage_scan(space_id, provider, hosts, onepanel_credentials)


@wt(
    parsers.parse(
        "using {client}, {user} forces start of storage import scan for "
        '"{space}" at "{provider}" and waits till finished'
    )
)
def force_start_and_wait_to_finish_storage_import_scan(
    client: str,
    user: str,
    provider: str,
    space: str,
    spaces: Spaces,
    hosts: Hosts,
    onepanel_credentials: User,
    selenium: SeleniumDrivers,
) -> None:
    if client.lower() == "rest":
        space_id = spaces[space]
        force_start_storage_scan(space_id, provider, hosts, onepanel_credentials)
        wait_for_storage_scan_to_finish(space_id, provider, hosts, onepanel_credentials)
    elif client.lower() == "web gui":
        run_scan_and_wait_till_finished(selenium, user)
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.parse(
        'using REST, {user} waits for space "{space}" support in {provider_name}'
    )
)
def wt_wait_for_space_support_rest(
    space: str,
    spaces: Spaces,
    user: str,
    users: Users,
    provider_name: str,
    hosts: Hosts,
) -> None:
    wait_for_space_support(
        spaces[space], hosts[provider_name]["hostname"], [user], users
    )
