"""This module contains gherkin steps to run mixed acceptance tests featuring
basic operation on symlinks and hardlinks using web GUI and swagger.
"""

__author__ = "Jakub Karczewski"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.meta_steps.oneprovider.data import (
    create_hardlink_of_file_located_outside_current_location_and_place_it_in_path,
    create_symlinks_of_file_with_path,
)
from tests.mixed.steps.oneclient.data_basic import change_client_name_to_hostname
from tests.mixed.steps.rest.oneprovider.data import (
    _lookup_file_id,
    check_for_hardlink_between_files_rest,
    create_hardlink_rest,
    create_symlink_rest,
    get_file_hardlinks_rest,
    get_file_symlink_value_rest,
)
from tests.mixed.utils.common import NoSuchClientException, login_to_provider
from tests.oneclient.steps.multi_file_steps import (
    assert_hardlink_between_files,
    assert_symlink_of_file,
    create_hardlink,
    create_symlink,
)
from tests.utils.acceptance_utils import list_parser
from tests.utils.bdd_utils import parsers, wt


@wt(
    parsers.re(
        r"using (?P<client>.*), user (?P<user>.+?) sees that "
        r'"(?P<path1>.*)" symlink points to "(?P<path2>.*)" in "(?P<space>.*)"'
        r" in (?P<host>.*)"
    )
)
def assert_file_symlink_value(client, users, user, hosts, host, space, path1, path2):
    client_lower = client.lower()
    if client_lower == "rest":
        user_client_op = login_to_provider(user, users, hosts[host]["hostname"])
        symlink_id = _lookup_file_id(f"{space}/{path1}", user_client_op)
        target_path = get_file_symlink_value_rest(users, user, hosts, host, symlink_id)

        path_splitted = target_path.split("/")
        cut_path = "/".join(path_splitted[1:])

        assert (
            cut_path == path2
        ), f"given path: {path2} not equal to target path from endpoint: {cut_path}"
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), user (?P<user>.+) sees that"
        r' "(?P<file_path>.*)" hardlinks point to "(?P<paths_list>.*)"'
        r' in space "(?P<space>.*)" in (?P<host>.*)'
    )
)
def assert_file_hardlinks(
    client, users, user, hosts, host, file_path, space, paths_list
):
    client_lower = client.lower()
    if client_lower == "rest":
        user_client_op = login_to_provider(user, users, hosts[host]["hostname"])
        file_id = _lookup_file_id(f"{space}/{file_path}", user_client_op)
        actual_hardlinks = get_file_hardlinks_rest(users, user, hosts, host, file_id)
        expected_ids = [
            _lookup_file_id(f"{space}/{path}", user_client_op)
            for path in list_parser(paths_list)
        ]
        assert set(actual_hardlinks) == set(expected_ids), (
            "The IDs of hardlinks from endpoint are not the same as IDs of provided"
            " files"
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), user( of)? (?P<user>.+) creates"
        r' symlink located in "(?P<path>.*)" pointing to "(?P<file_name>.*)" in'
        r' "(?P<space>.*)" in file browser'
        r" in (?P<host>.*)"
    )
)
def create_file_symlink(
    client,
    users,
    user,
    hosts,
    host,
    selenium,
    file_name,
    path,
    space,
    spaces,
    tmp_memory,
    op_container,
    popups,
):
    client_lower = client.lower()
    if client_lower == "web gui":
        create_symlinks_of_file_with_path(
            selenium,
            user,
            file_name,
            space,
            tmp_memory,
            op_container,
            popups,
            path,
        )
    elif client_lower == "rest":
        user_client_op = login_to_provider(user, users, hosts[host]["hostname"])

        path_splitted = path.split("/")
        parent_path = "/".join(path_splitted[:-1])

        space_prefix = f"<__onedata_space_id:{spaces[space]}>"
        target_path = f"{space_prefix}/{file_name}"

        destination_dir_id = _lookup_file_id(f"{space}/{parent_path}", user_client_op)
        create_symlink_rest(
            users, user, hosts, host, destination_dir_id, target_path, file_name
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), user (?P<user>.+) creates"
        r' symlink located in "(?P<symlink_path>.*)" pointing to "(?P<file_path>.*)" in'
        r' "(?P<space>.*)"'
    )
)
def create_symlink_oneclient(client, user, users, symlink_path, file_path, space):
    client_lower = client.lower()
    if "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        file_name = file_path.split("/")[-1]
        create_symlink(
            user,
            f"{space}/{file_path}",
            f"{space}/{symlink_path}/{file_name}",
            oneclient_host,
            users,
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), user( of)? (?P<user>.*) creates hardlink of "
        r'"(?P<file_path>.*)" placed in "(?P<hardlink_path>.*)" directory in'
        r' "(?P<space>.*)"'
        r" in (?P<host>.*)"
    )
)
def create_file_hardlink(
    client,
    users,
    user,
    hosts,
    host,
    selenium,
    file_path,
    hardlink_path,
    space,
    tmp_memory,
    op_container,
    popups,
):
    client_lower = client.lower()
    if client_lower == "web gui":
        create_hardlink_of_file_located_outside_current_location_and_place_it_in_path(
            selenium,
            user,
            space,
            tmp_memory,
            op_container,
            popups,
            file_path,
            hardlink_path,
        )
    elif client_lower == "rest":
        user_client_op = login_to_provider(user, users, hosts[host]["hostname"])
        file_name = file_path.split("/")[-1]
        create_hardlink_rest(
            users,
            user,
            hosts,
            host,
            _lookup_file_id(f"{space}/{hardlink_path}", user_client_op),
            _lookup_file_id(f"{space}/{file_path}", user_client_op),
            file_name,
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>.*), user (?P<user>.*) creates hardlink of "
        r'"(?P<file_path>.*)" placed in "(?P<hardlink_path>.*)" directory in'
        r' "(?P<space>.*)"'
    )
)
def create_hardlink_oneclient(client, user, users, file_path, hardlink_path, space):
    client_lower = client.lower()
    if "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        file_name = file_path.split("/")[-1]
        create_hardlink(
            user,
            f"{space}/{file_path}",
            f"{space}/{hardlink_path}/{file_name}",
            oneclient_host,
            users,
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using REST, user (?P<user>.*) sees that"
        r' the path of "(?P<hardlink_path>.*)" hardlink is "(?P<file_path>.*)" in space'
        r' "(?P<space>.*)" in (?P<host>.*)'
    )
)
def assert_hardlink_between_files_rest(
    users, user, hosts, host, file_path, hardlink_path, space
):
    user_client_op = login_to_provider(user, users, hosts[host]["hostname"])
    file_id1 = _lookup_file_id(f"{space}/{file_path}", user_client_op)
    file_id2 = _lookup_file_id(f"{space}/{hardlink_path}", user_client_op)
    assert check_for_hardlink_between_files_rest(
        users, user, hosts, host, file_id1, file_id2
    ), f"file: {hardlink_path} is not a hardlink to file: {file_path}"


@wt(
    parsers.re(
        r'using (?P<client>\w+), user (?P<user>\w+) can see that "(?P<file_path1>.*)"'
        r' and "(?P<file_path2>.*)" are'
        r" hardlinked"
    )
)
def assert_hardlink_between_files_oneclient(
    client, user, users, file_path1, file_path2, request
):
    client_lower = client.lower()
    if "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        assert_hardlink_between_files(
            user, oneclient_host, users, file_path1, file_path2, request
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")


@wt(
    parsers.re(
        r"using (?P<client>\w+), user (?P<user>\w+) can see that file"
        r' "(?P<symlink_path>.*)" is a symlink and points to "(?P<file_path>.*)"'
    )
)
def assert_file_is_symlink_and_where_it_points_oneclient(
    client, user, users, file_path, symlink_path, request
):
    client_lower = client.lower()
    if "oneclient" in client_lower:
        oneclient_host = change_client_name_to_hostname(client_lower)
        assert_symlink_of_file(
            user, oneclient_host, users, symlink_path, file_path, request
        )
    else:
        raise NoSuchClientException(f"Client: {client} not found.")
