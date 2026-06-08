"""This module contains rest functions used in upgrade tests"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


import json
from typing import Any

from tests import OP_REST_PORT, OZ_REST_PORT, PANEL_REST_PORT
from tests.utils.rest_utils import (
    get_panel_rest_path,
    get_provider_rest_path,
    get_zone_rest_path,
    http_delete,
    http_get,
    http_patch,
    http_post,
    http_put,
)
from tests.utils.utils import repeat_failed

DEFAULT_REST_QUERY_TIMEOUT = 60

EXAMPLE_HANDLE_METADATA = {
    "handleServiceId": "$handle_service_id",
    "resourceType": "Share",
    "resourceId": "$share_id",
    "metadataPrefix": "oai_dc",
    "metadata": """<?xml version="1.0" encoding="utf-8"?>
<metadata xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
          xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>Test dataset</dc:title>
    <dc:creator>Jane Doe</dc:creator>
    <dc:subject>Test</dc:subject>
</metadata>""",
}

# Spaces


def list_all_user_spaces(provider_host: Any, token: Any) -> Any:
    res = http_get(
        ip=provider_host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("spaces"),
        headers={
            "X-Auth-Token": token,
        },
    )
    return res.json()


def get_space_id(space_name: Any, provider_host: Any, token: Any) -> Any:
    spaces = list_all_user_spaces(provider_host, token)
    for space in spaces:
        if space["name"] == space_name:
            return space["spaceId"]
    raise ValueError(f"space {space_name} not found")


# File access and management


def lookup_file_id(file_path: Any, provider_hostname: Any, token: Any) -> Any:
    res = http_post(
        ip=provider_hostname,
        port=OP_REST_PORT,
        path=get_provider_rest_path("lookup-file-id", file_path),
        headers={
            "X-Auth-Token": token,
        },
    )
    return res.json()["fileId"]


def download_file_content(provider_host: Any, token: Any, file_id: Any) -> Any:
    res = http_get(
        ip=provider_host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("data", file_id, "content"),
        headers={
            "X-Auth-Token": token,
        },
    )
    return res.content


def get_file_attributes(
    provider_host: Any, token: Any, file_id: Any, attributes: Any
) -> Any:
    # if provider version is lower than 21.02.5, provided attributes are ignored
    # and all available attributes are returned
    res = http_get(
        ip=provider_host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("data", file_id),
        headers={
            "X-Auth-Token": token,
            "Content-Type": "application/json",
        },
        data=json.dumps({"attributes": attributes}),
    )
    return res.json()


@repeat_failed(timeout=30)
def get_directory_size_statistics(
    provider_host: Any, token: Any, file_id: Any, mode: Any
) -> Any:
    res = http_get(
        ip=provider_host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("data", file_id, "dir_size_stats"),
        headers={
            "X-Auth-Token": token,
            "Content-Type": "application/json",
        },
        data=json.dumps({"mode": mode}),
    )
    return res.json()


# Metadata


def set_file_json_metadata(
    provider_host: Any, token: Any, file_id: Any, data: Any
) -> Any:
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


def get_file_json_metadata(provider_host: Any, token: Any, file_id: Any) -> Any:
    res = http_get(
        ip=provider_host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("data", file_id, "metadata", "json"),
        headers={
            "X-Auth-Token": token,
        },
    )
    return res


def delete_file_json_metadata(provider_host: Any, token: Any, file_id: Any) -> Any:
    res = http_delete(
        ip=provider_host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("data", file_id, "metadata", "json"),
        headers={
            "X-Auth-Token": token,
        },
    )
    return res


def set_file_rdf_metadata(
    provider_host: Any, token: Any, file_id: Any, data: Any
) -> Any:
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


def get_file_rdf_metadata(provider_host: Any, token: Any, file_id: Any) -> Any:
    res = http_get(
        ip=provider_host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("data", file_id, "metadata", "rdf"),
        headers={
            "X-Auth-Token": token,
        },
    )
    return res


def delete_file_rdf_metadata(provider_host: Any, token: Any, file_id: Any) -> Any:
    res = http_delete(
        ip=provider_host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("data", file_id, "metadata", "rdf"),
        headers={
            "X-Auth-Token": token,
        },
    )
    return res


def set_file_extended_attribute(
    provider_host: Any, token: Any, file_id: Any, data: Any
) -> Any:
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


def get_file_extended_attributes(
    provider_host: Any, token: Any, file_id: Any, attribute: Any = None
) -> Any:
    res = http_get(
        ip=provider_host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("data", file_id, "metadata", "xattrs"),
        params={"attribute": attribute} if attribute else None,
        headers={
            "X-Auth-Token": token,
        },
    )
    return res


def delete_file_extended_attributes(
    provider_host: Any, token: Any, file_id: Any, keys: Any = None
) -> Any:
    data = {"keys": list(keys)}
    res = http_delete(
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


def establish_dataset(provider_host: Any, token: Any, file_id: Any) -> Any:
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


@repeat_failed(timeout=10)
def create_archive(
    provider_host: Any,
    token: Any,
    dataset_id: Any,
    description: Any,
    config: Any = None,
) -> Any:
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


def get_archive_information(provider_host: Any, token: Any, archive_id: Any) -> Any:
    res = http_get(
        ip=provider_host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("archives", archive_id),
        headers={
            "X-Auth-Token": token,
        },
    )
    return res.json()


# Shares and Handles


def create_share(provider_host: Any, token: Any, file_id: Any, name: Any) -> Any:
    prov_version = int(
        get_provider_configuration(provider_host)["version"].split(".")[0]
    )
    res = http_post(
        ip=provider_host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("shares"),
        headers={
            "X-Auth-Token": token,
            "Content-Type": "application/json",
        },
        data=json.dumps(
            {
                "name": name,
                "rootFileId" if prov_version >= 21 else "fileId": file_id,
            }
        ),
    )
    return res.json()["shareId"]


def get_share_info(provider_host: Any, token: Any, share_id: Any) -> Any:
    res = http_get(
        ip=provider_host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("shares", share_id),
        headers={
            "X-Auth-Token": token,
        },
    )
    return res.json()


def list_handles(zone_host: Any, token: Any) -> Any:
    res = http_get(
        ip=zone_host,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("handles"),
        headers={
            "X-Auth-Token": token,
        },
    )
    return res.json()


def list_handle_services(zone_host: Any, token: Any) -> Any:
    res = http_get(
        ip=zone_host,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("handle_services"),
        headers={
            "X-Auth-Token": token,
        },
    )
    return res.json()


def register_handle(zone_host: Any, token: Any, share_id: Any) -> Any:
    handle_service_id = list_handle_services(zone_host, token)["handle_services"][0]
    EXAMPLE_HANDLE_METADATA.update(
        {"handleServiceId": handle_service_id, "resourceId": share_id}
    )
    res = http_post(
        ip=zone_host,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("handles"),
        headers={
            "X-Auth-Token": token,
            "Content-Type": "application/json",
        },
        data=json.dumps(EXAMPLE_HANDLE_METADATA),
    )
    return res


def get_handle(zone_host: Any, token: Any, handle_id: Any) -> Any:
    res = http_get(
        ip=zone_host,
        port=OZ_REST_PORT,
        path=get_zone_rest_path("handles", handle_id),
        headers={
            "X-Auth-Token": token,
        },
    )
    return res.json()


# Views


def create_view(
    provider_host: Any,
    token: Any,
    space_id: Any,
    view_name: Any,
    data: Any,
    spatial: Any = False,
    providers: Any = None,
) -> Any:
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
    provider_host: Any,
    token: Any,
    space_id: Any,
    view_name: Any,
    spatial: Any = False,
    start_range: Any = None,
    end_range: Any = None,
) -> Any:
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
        headers={
            "X-Auth-Token": token,
        },
        params=query_params,
    )
    return res.json()


def get_view(provider_host: Any, token: Any, space_id: Any, view_name: Any) -> Any:
    res = http_get(
        ip=provider_host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("spaces", space_id, "views", view_name),
        headers={
            "X-Auth-Token": token,
        },
    )
    return res.json()


def update_view_reduce_function(
    provider_host: Any, token: Any, space_id: Any, view_name: Any, data: Any
) -> Any:
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


def get_provider_configuration(provider_host: Any) -> Any:
    res = http_get(
        ip=provider_host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("configuration"),
    )
    return res.json()


def subscribe_to_file_changes(
    provider_host: Any, token: Any, space_id: Any, data: Any, stream: Any = True
) -> Any:
    query_params = {"last_seq": 0, "timeout": 1000}

    res = http_post(
        ip=provider_host,
        port=OP_REST_PORT,
        path=get_provider_rest_path("changes", "metadata", space_id),
        headers={
            "X-Auth-Token": token,
            "Content-Type": "application/json",
        },
        data=json.dumps(data),
        stream=stream,
        params=query_params,
    )
    return res


# Onepanel


def configure_file_popularity_mechanism_in_the_space(
    provider_host: Any, token: Any, space_id: Any, data: Any
) -> Any:
    res = http_patch(
        ip=provider_host,
        port=PANEL_REST_PORT,
        path=get_panel_rest_path(
            "provider", "spaces", space_id, "file-popularity", "configuration"
        ),
        headers={
            "X-Auth-Token": token,
            "Content-Type": "application/json",
        },
        data=json.dumps(data),
    )
    return res
