"""Utils and fixtures to facilitate operations on storages in Onepanel
using REST API.
"""

# pylint: disable=wrong-import-position, unused-argument
from __future__ import absolute_import

__author__ = "Bartek Kryza"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"
import os
import sys

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../mixed")),
)

from tests.mixed.onepanel_client import StoragesApi
from tests.mixed.onepanel_client.models.cephrados_modify import CephradosModify
from tests.mixed.onepanel_client.models.nulldevice_modify import NulldeviceModify
from tests.mixed.onepanel_client.models.posix_modify import PosixModify
from tests.mixed.onepanel_client.models.s3_modify import S3Modify
from tests.mixed.utils.common import login_to_panel


def modify_storage_parameters(
    user,
    provider,
    storage_id,
    storage_name,
    params,
    onepanel_host,
    onepanel_credentials,
):
    user_client = login_to_panel(
        onepanel_credentials.username,
        onepanel_credentials.password,
        onepanel_host,
    )

    storages_api = StoragesApi(user_client)

    if params["type"] == "cephrados":
        modify_request = CephradosModify(**params)
    elif params["type"] == "s3":
        modify_request = S3Modify(**params)
    elif params["type"] == "posix":
        modify_request = PosixModify(**params)
    elif params["type"] == "nulldevice":
        modify_request = NulldeviceModify(**params)
    else:
        raise ValueError(f"Unsupported storage type {params['type']}")

    storages_api.modify_storage(storage_id, {storage_name: modify_request})
