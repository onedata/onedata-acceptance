"""Utils to facilitate basic operations in Oneprovider using REST API."""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from oneprovider_client import BasicFileOperationsApi, FilePathResolutionApi

from tests.mixed.type_definitions import HostsConfig
from tests.mixed.utils.common import login_to_provider
from tests.utils.user_utils import Users


def see_item_is_dir_op_rest(
    path: str,
    user: str,
    users: Users,
    host: str,
    hosts: HostsConfig,
) -> bool:
    client = login_to_provider(user, users, hosts[host]["hostname"])
    resolve_file_path_api = FilePathResolutionApi(client)
    file_id = resolve_file_path_api.lookup_file_id(path).file_id
    file_api = BasicFileOperationsApi(client)
    attributes = file_api.get_attrs(file_id)
    return attributes.type == "DIR"
