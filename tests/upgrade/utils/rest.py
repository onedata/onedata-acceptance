"""This module contains rest functions used in upgrade tests"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"



import json

from tests import OP_REST_PORT, OZ_REST_PORT
from tests.utils.rest_utils import (
    get_provider_rest_path,
    get_zone_rest_path,
    http_get,
    http_post,
    http_put,
)

# Spaces


def list_all_user_spaces(provider_host, token):
    res = http_get(
        ip=provider_host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("spaces"),
        headers={"X-Auth-Token": token},
    )
    return res.json()


def get_space_id(space_name, provider_host, token):
    spaces = list_all_user_spaces(provider_host, token)
    for space in spaces:
        if space["name"] == space_name:
            return space["spaceId"]
    raise ValueError(f"space {space_name} not found")


# File access and management


def lookup_file_id(file_path, provider_hostname, token):
    res = http_post(
        ip=provider_hostname,
        port=OP_REST_PORT,
        path=get_provider_rest_path("lookup-file-id", file_path),
        headers={"X-Auth-Token": token},
    )
    return res.json()["fileId"]


def download_file_content(provider_host, token, file_id):
    res = http_get(
        ip=provider_host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("data", file_id, "content"),
        headers={"X-Auth-Token": token},
    )
    return res.content


# Metadata


def set_file_json_metadata(provider_host, token, file_id, data):
    res = http_put(
        ip=provider_host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("data", file_id, "metadata", "json"),
        headers={
            "X-Auth-Token": token,
            "Content-Type": "application/json",
        },
        data=json.dumps(data),
    )
    return res


def set_file_rdf_metadata(provider_host, token, file_id, data):
    res = http_put(
        ip=provider_host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("data", file_id, "metadata", "rdf"),
        headers={
            "X-Auth-Token": token,
            "Content-Type": "application/rdf+xml",
        },
        data=data,
    )
    return res


def set_file_extended_attribute(provider_host, token, file_id, data):
    res = http_put(
        ip=provider_host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("data", file_id, "metadata", "xattrs"),
        headers={
            "X-Auth-Token": token,
            "Content-Type": "application/json",
        },
        data=json.dumps(data),
    )
    return res


# Datasets amd Archives


def establish_dataset(provider_host, token, file_id):
    res = http_post(
        ip=provider_host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("datasets"),
        headers={
            "X-Auth-Token": token,
            "Content-Type": "application/json",
        },
        data=json.dumps({"rootFileId": file_id}),
    )
    return res.json()


def create_archive(provider_host, token, dataset_id, description, config=None):
    data = {"datasetId": dataset_id, "description": description}
    if config:
        data.update(config)
    res = http_post(
        ip=provider_host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("archives"),
        headers={
            "X-Auth-Token": token,
            "Content-Type": "application/json",
        },
        data=json.dumps(data),
    )
    return res.json()


def get_archive_information(provider_host, token, archive_id):
    res = http_get(
        ip=provider_host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("archives", archive_id),
        headers={"X-Auth-Token": token},
    )
    return res.json()


# Shares and Handles


def create_share(provider_host, token, file_id, prov_version):
    res = http_post(
        ip=provider_host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("shares"),
        headers={"X-Auth-Token": token, "Content-Type": "application/json"},
        data=json.dumps(
            {
                "name": "testShare",
                "rootFileId" if prov_version >= 21 else "fileId": file_id,
            }
        ),
    )
    return res.json()["shareId"]


def get_share_info(provider_host, token, share_id):
    res = http_get(
        ip=provider_host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("shares", share_id),
        headers={"X-Auth-Token": token},
    )
    return res.json()


def list_handles(zone_host, token):
    res = http_get(
        ip=zone_host,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("handles"),
        headers={"X-Auth-Token": token},
    )
    return res.json()


def list_handle_services(zone_host, token):
    res = http_get(
        ip=zone_host,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("handle_services"),
        headers={"X-Auth-Token": token},
    )
    return res.json()


def register_handle(zone_host, token, config):
    res = http_post(
        ip=zone_host,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("handles"),
        headers={
            "X-Auth-Token": token,
            "Content-Type": "application/json",
        },
        data=json.dumps(config),
    )
    return res


def get_handle(zone_host, token, handle_id):
    res = http_get(
        ip=zone_host,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("handles", handle_id),
        headers={"X-Auth-Token": token},
    )
    return res.json()


# Views


def create_view(
    provider_host, token, space_id, view_name, data, spatial=False, providers=None
):
    query_params = {}
    if providers:
        query_params.update({"providers[]": providers})
    if spatial:
        query_params.update({"spatial": "true"})
    res = http_put(
        ip=provider_host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("spaces", space_id, "views", view_name),
        headers={
            "X-Auth-Token": token,
            "Content-Type": "application/javascript",
        },
        data=data,
        params=query_params,
    )
    return res


def query_view(
    provider_host,
    token,
    space_id,
    view_name,
    spatial=None,
    start_range=None,
    end_range=None,
):
    if spatial:
        query_params = {
            "spatial": "true",
            "start_range": start_range,
            "end_range": end_range,
        }
    else:
        query_params = {}
    res = http_get(
        ip=provider_host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("spaces", space_id, "views", view_name, "query"),
        headers={"X-Auth-Token": token},
        params=query_params,
    )
    return res.json()


def get_view(provider_host, token, space_id, view_name):
    res = http_get(
        ip=provider_host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("spaces", space_id, "views", view_name),
        headers={"X-Auth-Token": token},
    )
    return res.json()


def update_view_reduce_function(provider_host, token, space_id, view_name, data):
    res = http_put(
        ip=provider_host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("spaces", space_id, "views", view_name, "reduce"),
        headers={
            "X-Auth-Token": token,
            "Content-Type": "application/javascript",
        },
        data=data,
    )
    return res


# Provider


def get_provider_configuration(provider_host):
    res = http_get(
        ip=provider_host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("configuration"),
    )
    return res.json()
