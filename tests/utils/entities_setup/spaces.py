"""Steps for spaces creation using REST API."""

__author__ = "Bartek Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import json
import time
from collections.abc import Mapping, MutableMapping, Sequence
from functools import cache
from typing import Optional, Protocol, TypedDict, cast

import requests
import yaml

from tests import OP_REST_PORT, OZ_REST_PORT, PANEL_REST_PORT
from tests.conftest import HostDescription, JsonValue
from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.utils.generic import parse_seq
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.http_exceptions import (
    HTTPBadRequest,
    HTTPError,
    HTTPForbidden,
    HTTPNotFound,
)
from tests.utils.rest_utils import (
    get_panel_rest_path,
    get_provider_rest_path,
    get_zone_rest_path,
    http_delete,
    http_get,
    http_post,
    http_put,
)
from tests.utils.utils import repeat_failed

type Hosts = Mapping[str, HostDescription]
type Users = Mapping[str, "UserLike"]
type Groups = Mapping[str, str]
type Storages = MutableMapping[str, MutableMapping[str, str]]
type Spaces = MutableMapping[str, str]
type MemberEntry = str | dict[str, "MemberOptions"]
type ProviderEntry = dict[str, "ProviderOptions"]
type Metadata = dict[str, JsonValue]
type TreeValue = JsonValue | "DirectoryTree" | "FileDetails"
type TreeEntry = str | dict[str, TreeValue]
type DirectoryTree = list[TreeEntry]


class CredentialsLike(Protocol):
    @property
    def username(self) -> str: ...

    @property
    def password(self) -> Optional[str]: ...


class UserLike(CredentialsLike, Protocol):
    @property
    def user_id(self) -> str: ...

    @property
    def token(self) -> str: ...


class MemberOptions(TypedDict):
    privileges: list[str]


class ProviderOptions(TypedDict):
    storage: str
    size: int | str


class FileDetails(TypedDict, total=False):
    provider: str
    content: JsonValue
    metadata: Metadata


class CdmiCreator(Protocol):
    def __call__(
        self,
        path: str,
        data: Optional[str] = None,
        repeats: int = 10,
        auth: Optional[tuple[str, Optional[str]]] = None,
        headers: Optional[Mapping[str, str]] = None,
        **extra: str,
    ) -> Optional[requests.Response]: ...


StorageConfig = TypedDict(
    "StorageConfig",
    {"defaults": dict[str, str], "directory tree": DirectoryTree},
)


SpaceDescription = TypedDict(
    "SpaceDescription",
    {
        "owner": str,
        "users": list[MemberEntry],
        "groups": list[MemberEntry],
        "providers": list[ProviderEntry],
        "storage": StorageConfig,
    },
    total=False,
)
type SpacesConfig = Mapping[str, SpaceDescription]


@given(
    parsers.parse(
        'initial spaces configuration in "{zone_host}" Onezone service:\n{config}'
    )
)
def create_and_configure_spaces_step(
    config: str,
    zone_host: str,
    admin_credentials: CredentialsLike,
    onepanel_credentials: CredentialsLike,
    hosts: Hosts,
    users: Users,
    groups: Groups,
    storages: Storages,
    spaces: Spaces,
) -> None:
    create_and_configure_spaces(
        cast(SpacesConfig, yaml.load(config, yaml.Loader)),
        zone_host,
        admin_credentials,
        onepanel_credentials,
        hosts,
        users,
        groups,
        storages,
        spaces,
    )


def create_and_configure_spaces(
    config: SpacesConfig,
    zone_host: str,
    admin_credentials: CredentialsLike,
    onepanel_credentials: CredentialsLike,
    hosts: Hosts,
    users: Users,
    groups: Groups,
    storages: Storages,
    spaces: Spaces,
) -> None:
    """Create and configure spaces according to given config.

    Config format given in yaml is as follows:

        space_name_1:
            owner: user_name                ---> currently we identify user account with concrete
                                                 browser so user_name == browser_id
            [users]:                        ---> optional
                - user_name_2
                - user_name_3:
                    [privileges]:           ---> optional
                        - privilege_1
                        - privilege_2
            [groups]:                       ---> optional
                - group_name_1:
                    [privileges]:           ---> optional
                        - privilege_1
                        - privilege_2
                - group_name_2
            [providers]:                    ---> optional
                - provider_name_1:
                    storage: name
                    size: size in bits
            [storage]:                      ---> optional
                defaults:
                    provider: provider_name         --> default provider on whose storage
                                                        files will be created
                directory tree:
                    - dir0                  ---> name starting with 'dir' prefix
                                                 is treated as directory
                    - dir2:
                        - file0: text
                        - file1:
                            provider: p2    ---> mandatory if dict form is used
                            content: text
                            metadata:
                                type: json/basic(xattrs)
                                key: value
                        - file2

        space_name_2:
            ...

    Example configuration:

        space1:
            owner: user1
            users:
                - user2
                - user3
            groups:
                - group1
            providers:
                - p1:
                    storage: onestorage
                    size: 1000000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1
                    - dir2:
                        - file0
                        - file1: 11111
                        - file2:
                            provider: 2
                            content: 22222
                            metadata:
                              type: basic
                              author: John Doe
                              year: 2020
    """
    _create_and_configure_spaces(
        cast(SpacesConfig, config),
        zone_host,
        admin_credentials,
        onepanel_credentials,
        hosts,
        users,
        groups,
        storages,
        spaces,
    )


@given(
    parsers.parse(
        'additional spaces configuration in "{zone_host}" Onezone service:\n{config}'
    )
)
def add_spaces_configuration(
    config: str,
    zone_host: str,
    admin_credentials: CredentialsLike,
    onepanel_credentials: CredentialsLike,
    hosts: Hosts,
    users: Users,
    groups: Groups,
    storages: Storages,
    spaces: Spaces,
) -> None:
    _create_and_configure_spaces(
        cast(SpacesConfig, yaml.load(config, yaml.Loader)),
        zone_host,
        admin_credentials,
        onepanel_credentials,
        hosts,
        users,
        groups,
        storages,
        spaces,
    )


def _create_and_configure_spaces(
    config: SpacesConfig,
    zone_name: str,
    admin_credentials: CredentialsLike,
    onepanel_credentials: CredentialsLike,
    hosts: Hosts,
    users_db: Users,
    groups_db: Groups,
    storages_db: Storages,
    spaces_db: Spaces,
) -> None:
    zone = cast(Mapping[str, str], hosts[zone_name])
    zone_hostname = zone["hostname"]

    for space_name, description in config.items():
        owner = users_db[description["owner"]]
        users_to_add = description.get("users", [])
        spaces_db[space_name] = space_id = _create_space(
            zone_hostname, owner.username, owner.password, space_name
        )
        _add_users_to_space(
            zone_hostname, admin_credentials, space_id, users_db, users_to_add
        )
        _add_groups_to_space(
            zone_hostname,
            admin_credentials,
            space_id,
            groups_db,
            description.get("groups", []),
        )
        _get_support(
            zone_hostname,
            onepanel_credentials,
            owner,
            space_id,
            storages_db,
            hosts,
            description.get("providers", []),
            users_to_add,
            users_db,
        )
        _init_storage_from_config(
            owner, space_name, hosts, users_db, description.get("storage")
        )


def _create_space(
    zone_hostname: str,
    owner_username: str,
    owner_password: Optional[str],
    space_name: str,
) -> str:
    space_properties = {"name": space_name}
    response = http_post(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("user", "spaces"),
        auth=(owner_username, owner_password),
        data=json.dumps(space_properties),
    )
    return response.headers["location"].split("/")[-1]


def _add_users_to_space(
    zone_hostname: str,
    admin_credentials: CredentialsLike,
    space_id: str,
    users_db: Users,
    users_to_add: list[MemberEntry],
) -> None:
    for user in users_to_add:
        if isinstance(user, dict):
            [(user, options)] = user.items()
            privileges = options["privileges"]
        else:
            privileges = None

        _add_user_to_space(
            zone_hostname,
            admin_credentials.username,
            admin_credentials.password,
            space_id,
            users_db[user].user_id,
            privileges,
        )


def _add_user_to_space(
    zone_hostname: str,
    admin_username: str,
    admin_password: Optional[str],
    space_id: str,
    user_id: str,
    privileges: Optional[list[str]],
) -> None:
    if privileges:
        data = json.dumps({"operation": "set", "privileges": privileges})
    else:
        data = None

    http_put(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("spaces", space_id, "users", user_id),
        auth=(admin_username, admin_password),
        data=data,
    )


def _add_groups_to_space(
    zone_hostname: str,
    admin_credentials: CredentialsLike,
    space_id: str,
    groups_db: Groups,
    groups_to_add: list[MemberEntry],
) -> None:
    for group in groups_to_add:
        if isinstance(group, dict):
            [(group, options)] = group.items()
            privileges = options["privileges"]
        else:
            privileges = None

        _add_group_to_space(
            zone_hostname,
            admin_credentials.username,
            admin_credentials.password,
            space_id,
            groups_db[group],
            privileges,
        )


def _add_group_to_space(
    zone_hostname: str,
    admin_username: str,
    admin_password: Optional[str],
    space_id: str,
    group_id: str,
    privileges: Optional[list[str]],
) -> None:
    if privileges:
        data = json.dumps({"operation": "set", "privileges": privileges})
    else:
        data = None

    http_put(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("spaces", space_id, "groups", group_id),
        auth=(admin_username, admin_password),
        data=data,
    )


def _get_support(
    zone_hostname: str,
    onepanel_credentials: CredentialsLike,
    owner_credentials: UserLike,
    space_id: str,
    storages_db: Storages,
    hosts: Hosts,
    providers: Sequence[ProviderEntry],
    members: Sequence[MemberEntry],
    users: Users,
) -> None:
    onepanel_username = onepanel_credentials.username
    onepanel_password = onepanel_credentials.password

    for provider_entry in providers:
        [(provider, options)] = provider_entry.items()

        host = cast(Mapping[str, str], hosts[provider])
        provider_name = host["name"]
        provider_hostname = host["hostname"]
        storage_name = cast(str, options["storage"])

        provider_storages = storages_db.setdefault(provider_name, {})
        try:
            storage_id = provider_storages[storage_name]
        except KeyError:
            storage_id = _get_storage_id(
                provider_hostname, onepanel_username, onepanel_password, storage_name
            )
            provider_storages[storage_name] = storage_id

        token = http_post(
            ip=zone_hostname,
            port=OZ_REST_PORT,
            path=get_zone_rest_path("spaces", space_id, "providers", "token"),
            auth=(owner_credentials.username, owner_credentials.password),
        ).json()["token"]

        space_support_details = {
            "token": token,
            "size": int(cast(int | str, options["size"])),
            "storageId": storage_id,
        }
        http_post(
            ip=provider_hostname,
            port=PANEL_REST_PORT,
            path=get_panel_rest_path("provider", "spaces"),
            auth=(onepanel_username, onepanel_password),
            data=json.dumps(space_support_details),
        )

        all_members = [owner_credentials.username] + [
            member if isinstance(member, str) else next(iter(member))
            for member in members
        ]
        wait_for_space_support(space_id, provider_hostname, all_members, users)


@repeat_failed(attempts=30, interval=0.5, exceptions=(AssertionError, HTTPError))
def wait_for_space_support(
    space_id: str, provider_hostname: str, members: list[str], users: Users
) -> None:
    for user in members:
        response = http_get(
            ip=provider_hostname,
            port=OP_REST_PORT,
            path=get_provider_rest_path("spaces"),
            headers={"X-Auth-Token": users[user].token},
        ).content
        space_id_list = [space["spaceId"] for space in json.loads(response)]

        assert (
            space_id in space_id_list
        ), f"space {space_id} not found in user {user} spaces"


@repeat_failed(attempts=10, interval=5)
def wait_for_storage_details(
    provider_hostname: str,
    storage_id: str,
    onepanel_username: str,
    onepanel_password: Optional[str],
) -> requests.Response:
    storage_details = http_get(
        ip=provider_hostname,
        port=PANEL_REST_PORT,
        path=get_panel_rest_path("provider", "storages", storage_id),
        auth=(onepanel_username, onepanel_password),
    )
    return storage_details


@repeat_failed(attempts=10, interval=5)
def wait_for_storages_id(
    provider_hostname: str,
    onepanel_username: str,
    onepanel_password: Optional[str],
) -> requests.Response:
    storages_id = http_get(
        ip=provider_hostname,
        port=PANEL_REST_PORT,
        path=get_panel_rest_path("provider", "storages"),
        auth=(onepanel_username, onepanel_password),
    )
    return storages_id


def _get_storage_id(
    provider_hostname: str,
    onepanel_username: str,
    onepanel_password: Optional[str],
    storage_name: str,
) -> str:
    storages_id = wait_for_storages_id(
        provider_hostname, onepanel_username, onepanel_password
    )
    for storage_id in storages_id.json()["ids"]:
        storage_details = wait_for_storage_details(
            provider_hostname, storage_id, onepanel_username, onepanel_password
        )
        if storage_details is None:
            raise AssertionError("Did not manage to get storage details")
        if storage_details.json()["name"] == storage_name:
            return storage_id

    raise RuntimeError(
        f"Storage with name '{storage_name}' was not found in Oneprovider "
        f"at {provider_hostname}. Make sure you have provided the right environment "
        "(env file) for the test."
    )


def _init_storage_from_config(
    owner_credentials: UserLike,
    space_name: str,
    hosts: Hosts,
    users: Users,
    storage_conf: Optional[StorageConfig],
) -> None:
    if not storage_conf:
        return

    defaults = storage_conf["defaults"]
    provider = cast(Mapping[str, str], hosts[defaults["provider"]])
    provider_hostname = provider["hostname"]
    directory_tree = storage_conf["directory tree"]

    init_storage(
        owner_credentials, space_name, hosts, provider_hostname, users, directory_tree
    )


def init_storage(
    owner_credentials: UserLike,
    space_name: str,
    hosts: Hosts,
    provider_hostname: str,
    users: Users,
    directory_tree: DirectoryTree,
) -> None:
    # if we make call too fast after deleting users from previous test
    # provider cache may not be refreshed and call will create dir for
    # currently nonexistent user, to avoid this wait some time

    time.sleep(2)

    def create_cdmi_object(
        path: str,
        data: Optional[str] = None,
        repeats: int = 10,
        auth: Optional[tuple[str, Optional[str]]] = None,
        headers: Optional[Mapping[str, str]] = None,
        **_extra: str,
    ) -> Optional[requests.Response]:
        if headers is None:
            headers = {"X-Auth-Token": owner_credentials.token}
        response = None
        for _attempt in range(repeats):
            try:
                response = http_put(
                    ip=provider_hostname,
                    port=OP_REST_PORT,
                    path="/cdmi/" + path,
                    headers=headers,
                    auth=auth,
                    data=data,
                )
            except (HTTPNotFound, HTTPBadRequest, HTTPError):
                # because user may not yet exist in provider first call
                # will fail, as such wait some time and try again
                time.sleep(1)
            else:
                break
        return response

    _mkdirs(
        create_cdmi_object,
        space_name,
        hosts,
        owner_credentials,
        provider_hostname,
        users,
        directory_tree,
    )


def _mkdirs(
    create_cdmi_obj: CdmiCreator,
    cwd: str,
    hosts: Hosts,
    owner_credentials: UserLike,
    provider_hostname: str,
    users: Users,
    dir_content: Optional[DirectoryTree] = None,
) -> None:
    if not dir_content:
        return

    for item in dir_content:
        if isinstance(item, dict):
            [(name, content)] = item.items()
            nested_content = cast(Optional[DirectoryTree], content)
        else:
            name, nested_content = item, None

        path = cwd + "/" + name
        if name.startswith("dir"):
            create_cdmi_obj(path + "/")
            _mkdirs(
                create_cdmi_obj,
                path,
                hosts,
                owner_credentials,
                provider_hostname,
                users,
                nested_content,
            )
        else:
            _mkfile(
                create_cdmi_obj,
                path,
                hosts,
                owner_credentials,
                provider_hostname,
                users,
                nested_content,
            )


def set_file_metadata(
    file_path: str,
    owner_credentials: UserLike,
    provider_hostname: str,
    users: Users,
    metadata: Optional[Metadata] = None,
) -> None:
    if metadata is None:
        return
    metadata_type = cast(str, metadata.pop("type", "json"))
    metadata_type = "xattrs" if metadata_type == "basic" else metadata_type
    user = owner_credentials.username
    file_id = get_file_id_by_rest(file_path, provider_hostname, users[user].token)
    http_put(
        ip=provider_hostname,
        port=OP_REST_PORT,
        path=get_provider_rest_path("data", file_id, "metadata", metadata_type),
        headers={"X-Auth-Token": owner_credentials.token},
        data=json.dumps(metadata),
    )


def _mkfile(
    create_cdmi_obj: CdmiCreator,
    file_path: str,
    hosts: Hosts,
    owner_credentials: UserLike,
    provider_hostname: str,
    users: Users,
    file_content: Optional[TreeValue] = None,
) -> None:
    if file_content:
        if not isinstance(file_content, dict):
            create_cdmi_obj(file_path, str(file_content))
        else:
            details = cast(FileDetails, file_content)
            provider = details.get("provider")
            if provider:
                provider_host = hosts[provider]
                create_cdmi_obj(
                    file_path,
                    data=str(details.get("content", None)),
                    url=f"https://{provider_host["hostname"]}:{OP_REST_PORT}/cdmi/",
                )
                set_file_metadata(
                    file_path,
                    owner_credentials,
                    provider_hostname,
                    users,
                    details.get("metadata"),
                )
            else:
                create_cdmi_obj(file_path, str(details.get("content", None)))
                set_file_metadata(
                    file_path,
                    owner_credentials,
                    provider_hostname,
                    users,
                    details.get("metadata"),
                )
    else:
        create_cdmi_obj(file_path)


def create_empty_file(
    path: str, users: Users, user: str, provider: str, hosts: Hosts
) -> None:
    provider_host = cast(Mapping[str, str], hosts[provider])
    http_put(
        ip=provider_host["hostname"],
        port=OP_REST_PORT,
        path="/cdmi/" + path,
        headers={"X-Auth-Token": users[user].token},
        auth=None,
        data=None,
    )


@repeat_failed(timeout=WAIT_BACKEND)
def get_file_id_by_rest(file_path: str, provider_hostname: str, token: str) -> str:
    response = http_post(
        ip=provider_hostname,
        port=OP_REST_PORT,
        path=get_provider_rest_path("lookup-file-id", file_path),
        headers={"X-Auth-Token": token},
    ).content
    return cast(str, json.loads(response)["fileId"])


@cache
def get_file_id_cached(file_path: str, provider_hostname: str, token: str) -> str:
    """
    Caches file ID lookup to avoid repeated REST calls.
    Useful also for retrieving IDs of files that may have been deleted.
    """
    return get_file_id_by_rest(file_path, provider_hostname, token)


@given(
    parsers.parse(
        "using REST, {user} creates a path with {number} "
        'nested directories named "{name}" in "{path}" '
        'supported by "{provider}" provider'
    )
)
def create_nested_directory(
    user: str,
    path: str,
    provider: str,
    number: str,
    name: str,
    users: Users,
    hosts: Hosts,
) -> None:
    names_list = name.split("/")
    min_index = int(names_list[0].split("_")[1])
    name_prefix = names_list[0].split("_")[0]
    nested_path = f"{path}"
    for i in range(min_index, min_index + int(number), 1):
        nested_path += f"/{name_prefix}_{i}"
        create_empty_file(nested_path + "/", users, user, provider, hosts)


@given(
    parsers.parse(
        'using REST, {user} creates "{file_name}" file in the '
        'last of {number} nested directories "{dir_name}" in '
        '"{path}" supported by "{provider}" provider'
    )
)
def create_file_in_nested_directory(
    user: str,
    path: str,
    provider: str,
    number: str,
    dir_name: str,
    file_name: str,
    users: Users,
    hosts: Hosts,
) -> None:
    names_list = dir_name.split("/")
    min_index = int(names_list[0].split("_")[1])
    name_prefix = names_list[0].split("_")[0]
    nested_path = f"{path}"
    for i in range(min_index, min_index + int(number), 1):
        nested_path += f"/{name_prefix}_{i}"
    nested_path += f"/{file_name}"
    create_empty_file(nested_path, users, user, provider, hosts)


@wt(
    parsers.parse(
        "using REST, {user} creates {number} empty files in "
        '"{path}" named "file_001", "file_002", ..., '
        '"file_N" supported by "{provider}" provider'
    )
)
@given(
    parsers.parse(
        "using REST, {user} creates {number} empty files in "
        '"{path}" named "file_001", "file_002", ..., '
        '"file_N" supported by "{provider}" provider'
    )
)
def create_files_names_alphabetically(
    number: str | int,
    path: str,
    users: Users,
    user: str,
    provider: str,
    hosts: Hosts,
) -> None:
    for i in range(int(number)):
        num = str(i + 1).rjust(3, "0")
        file_path = f"{path}/file_{num}"
        create_empty_file(file_path, users, user, provider, hosts)


@given(
    parsers.parse(
        "using REST, {user} creates {number} empty files in "
        'directories {dir_list} named "file_001", "file_002", ...,'
        ' "file_N" supported by "{provider}" provider'
    )
)
def create_files_names_alphabetically_with_dir_list(
    user: str,
    number: str | int,
    dir_list: str,
    provider: str,
    users: Users,
    hosts: Hosts,
) -> None:
    for dir_path in parse_seq(dir_list):
        create_files_names_alphabetically(
            number, dir_path, users, user, provider, hosts
        )


def _get_users_space_id_list(
    zone_hostname: str, owner_username: str, owner_password: Optional[str]
) -> list[str]:

    resp = http_get(
        ip=zone_hostname,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("user", "spaces"),
        auth=(owner_username, owner_password),
    ).json()
    spaces_id_list = resp["spaces"]
    return cast(list[str], spaces_id_list)


def _rm_all_spaces_for_user(
    zone_hostname: str, owner_username: str, owner_password: Optional[str]
) -> None:
    spaces_id_list = _get_users_space_id_list(
        zone_hostname, owner_username, owner_password
    )

    for space_id in spaces_id_list:
        try:
            http_delete(
                ip=zone_hostname,
                port=OZ_REST_PORT,
                path=get_zone_rest_path("spaces", space_id),
                auth=(owner_username, owner_password),
            )
        except HTTPForbidden:
            pass


def _rm_all_spaces_for_users_list(zone_hostname: str, users_db: Users) -> None:
    for user_credentials in users_db.values():
        _rm_all_spaces_for_user(
            zone_hostname, user_credentials.username, user_credentials.password
        )


@given(parsers.parse('there are no spaces of {user} in "{zone_host}" Onezone service'))
@repeat_failed(timeout=WAIT_FRONTEND)
def g_remove_all_space_supports_using_rest(
    hosts: Hosts, users: Users, user: str, zone_host: str
) -> None:
    host = cast(Mapping[str, str], hosts[zone_host])
    zone_hostname = host["hostname"]
    user_credentials = users[user]
    _rm_all_spaces_for_user(
        zone_hostname, user_credentials.username, user_credentials.password
    )


def force_start_storage_scan(
    space_id: str,
    provider: str,
    hosts: Hosts,
    onepanel_credentials: CredentialsLike,
) -> None:
    provider_host = cast(Mapping[str, str], hosts[provider])
    provider_hostname = provider_host["hostname"]
    onepanel_username = onepanel_credentials.username
    onepanel_password = onepanel_credentials.password
    http_post(
        ip=provider_hostname,
        port=PANEL_REST_PORT,
        path=get_panel_rest_path(
            "provider", "spaces", space_id, "storage-import", "auto", "force-start"
        ),
        auth=(onepanel_username, onepanel_password),
    )


@repeat_failed(timeout=WAIT_BACKEND)
def wait_for_storage_scan_to_finish(
    space_id: str,
    provider: str,
    hosts: Hosts,
    onepanel_credentials: CredentialsLike,
) -> None:
    provider_host = cast(Mapping[str, str], hosts[provider])
    provider_hostname = provider_host["hostname"]
    onepanel_username = onepanel_credentials.username
    onepanel_password = onepanel_credentials.password
    resp = http_get(
        ip=provider_hostname,
        port=PANEL_REST_PORT,
        path=get_panel_rest_path(
            "provider", "spaces", space_id, "storage-import", "auto", "info"
        ),
        auth=(onepanel_username, onepanel_password),
    )
    err_msg = f"status of storage scan is {resp.json()["status"]}"
    assert resp.json()["status"] == "completed", err_msg
