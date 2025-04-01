"""This module contains tests of view operations after environment upgrade"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import os
from functools import partial

import yaml

from tests.upgrade.utils.rest_utils import (
    configure_file_popularity_mechanism_in_the_space,
    create_view,
    get_provider_configuration,
    get_space_id,
    lookup_file_id,
    query_view,
    set_file_extended_attribute,
    set_file_json_metadata,
    set_file_rdf_metadata,
    subscribe_to_file_changes,
    update_view_reduce_function,
)
from tests.upgrade.utils.upgrade_utils import UpgradeTest
from tests.utils.http_exceptions import HTTPError
from tests.utils.utils import repeat_failed


def get_tests(tests_controller):
    return [
        UpgradeTest(
            "rest views test",
            partial(setup_views, tests_controller),
            partial(verify_views, tests_controller),
        ),
        UpgradeTest(
            "rest views multiprovider test",
            partial(setup_views_multiprovider, tests_controller),
            partial(verify_views_multiprovider, tests_controller),
        ),
        UpgradeTest(
            "rest subscribe changes test",
            partial(setup_subscribe_changes, tests_controller),
            partial(verify_subscribe_changes, tests_controller),
        ),
    ]


MAP_FUNC_ALL_FILES = """
    function(id, type, meta, ctx) {
    if(type == 'file_meta')
        return [id, ctx];
}
"""
MAP_FUNC_FILES_WITH_META = """
    function(id, type, meta, ctx) {
    if(type == 'custom_metadata')
        return [id, meta];
}
"""
MAP_FUNC_SPATIAL = """
function(id, type, meta, ctx) {
    if(type === "custom_metadata"){
        if (meta['latitude'] != null && meta['longitude'] != null){
            return [
                [{
                    "type": "Point",
                    "coordinates": [meta['latitude'], meta['longitude']]
                }],                                                         
                id                                                          
            ];
        }
    }
}
"""
REDUCE_FUNC = """
function(key, values, rereduce) {
   if (rereduce) {
       var result = 0;
       for (var i = 0; i < values.length; i++) {
           result += values[i];
       }
       return result;
   } else {
       return values.length;
   }
}
"""

VIEW1 = "view_all_files"
VIEW2 = "view_files_with_meta"
VIEW3 = "view_spatial"
VIEW4 = "view_with_reduce"
VIEW5 = "view_double_providers"
VIEW6 = "view_double_providers_error"

RESULTS = {}


# pylint: disable=too-many-statements
def setup_views(tests_controller):
    client = tests_controller.get_client("user1", "oneclient-1", "client11")
    provider_host = tests_controller.hosts["oneprovider-1"]["hostname"]
    token = tests_controller.users["user1"].token
    admin_token = tests_controller.users["admin"].token
    space_id = get_space_id("space_views", provider_host, token)

    # enable file popularity mechanism in space
    data = {"enabled": True}
    configure_file_popularity_mechanism_in_the_space(
        provider_host, admin_token, space_id, data
    )

    # create views
    _ = create_view(provider_host, token, space_id, VIEW1, MAP_FUNC_ALL_FILES)
    _ = create_view(provider_host, token, space_id, VIEW2, MAP_FUNC_FILES_WITH_META)
    _ = create_view(
        provider_host, token, space_id, VIEW3, MAP_FUNC_SPATIAL, spatial=True
    )
    _ = create_view(provider_host, token, space_id, VIEW4, MAP_FUNC_FILES_WITH_META)

    # create files
    create_example_content_in_space(client, "space_views")

    # create metadata
    add_example_metadata_to_files_in_space(provider_host, token, "space_views")

    # add reduce function to view
    update_view_reduce_function(provider_host, token, space_id, VIEW4, REDUCE_FUNC)

    RESULTS["view1"] = wait_for_expected_files_in_query_view(
        partial(query_view, provider_host, token, space_id, VIEW1),
        provider_host,
        token,
        "view1",
        "space_views",
    )
    RESULTS["view2"] = wait_for_expected_files_in_query_view(
        partial(query_view, provider_host, token, space_id, VIEW2),
        provider_host,
        token,
        "view2",
        "space_views",
    )
    RESULTS["view3"] = wait_for_expected_files_in_query_view(
        partial(
            query_view,
            provider_host,
            token,
            space_id,
            VIEW3,
            spatial=True,
            start_range="[0,0]",
            end_range="[5,10]",
        ),
        provider_host,
        token,
        "view3",
        "space_views",
    )
    RESULTS["view4"] = wait_for_expected_result_in_reduce_query_view(
        partial(query_view, provider_host, token, space_id, VIEW4)
    )
    RESULTS["file-popularity"] = wait_for_expected_files_in_query_view(
        partial(query_view, provider_host, token, space_id, "file-popularity"),
        provider_host,
        token,
        "file-popularity",
        "space_views",
    )


def verify_views(tests_controller):
    provider_host = tests_controller.hosts["oneprovider-1"]["hostname"]
    token = tests_controller.users["user1"].token
    space_id = get_space_id("space_views", provider_host, token)

    assert RESULTS["view1"] == query_view(provider_host, token, space_id, VIEW1)
    assert RESULTS["view2"] == query_view(provider_host, token, space_id, VIEW2)
    assert RESULTS["view3"] == query_view(
        provider_host,
        token,
        space_id,
        VIEW3,
        spatial=True,
        start_range="[0,0]",
        end_range="[5,10]",
    )
    assert RESULTS["view4"] == query_view(provider_host, token, space_id, VIEW4)
    assert RESULTS["file-popularity"] == query_view(
        provider_host, token, space_id, "file-popularity"
    )


def setup_views_multiprovider(tests_controller):
    multi_provider_suite = "oneprovider-2" in tests_controller.hosts
    if not multi_provider_suite:
        return

    provider_host = tests_controller.hosts["oneprovider-1"]["hostname"]
    provider_host2 = tests_controller.hosts["oneprovider-2"]["hostname"]
    prov1_id = get_provider_configuration(provider_host)["providerId"]
    prov2_id = get_provider_configuration(provider_host2)["providerId"]

    token = tests_controller.users["user1"].token
    space_id = get_space_id("space_views", provider_host, token)

    _ = create_view(
        provider_host,
        token,
        space_id,
        VIEW5,
        MAP_FUNC_ALL_FILES,
        providers=[prov1_id, prov2_id],
    )
    _ = create_view(
        provider_host,
        token,
        space_id,
        VIEW6,
        MAP_FUNC_ALL_FILES,
    )

    # expected files are the same as in view1
    RESULTS["view5"] = wait_for_expected_files_in_query_view(
        partial(query_view, provider_host2, token, space_id, VIEW5),
        provider_host,
        token,
        "view1",
        "space_views",
    )

    try:
        query_view(provider_host2, token, space_id, VIEW6)
    except HTTPError as e:
        # description message differs in different provider versions
        RESULTS["view6"] = e.response.json()["error"]["id"]


def verify_views_multiprovider(tests_controller):
    multi_provider_suite = "oneprovider-2" in tests_controller.hosts
    if not multi_provider_suite:
        return
    provider_host = tests_controller.hosts["oneprovider-1"]["hostname"]
    provider_host2 = tests_controller.hosts["oneprovider-2"]["hostname"]
    token = tests_controller.users["user1"].token
    space_id = get_space_id("space_views", provider_host, token)

    _assert(RESULTS["view5"], query_view(provider_host2, token, space_id, VIEW5))
    try:
        query_view(provider_host2, token, space_id, VIEW6)
        raise AssertionError("Operation should have failed")
    except HTTPError as e:
        _assert(RESULTS["view6"], e.response.json()["error"]["id"])


def setup_subscribe_changes(tests_controller):
    provider_host = tests_controller.hosts["oneprovider-1"]["hostname"]
    token = tests_controller.users["user1"].token
    space_id = get_space_id("space_views", provider_host, token)

    data = {
        "triggers": ["customMetadata"],
        "customMetadata": {"always": True, "fields": ["string"], "exists": ["string"]},
    }

    res = wait_for_expected_files_in_file_changes(
        provider_host, token, space_id, data, "space_views"
    )

    RESULTS["file_changes"] = res.text


def verify_subscribe_changes(tests_controller):
    provider_host = tests_controller.hosts["oneprovider-1"]["hostname"]
    token = tests_controller.users["user1"].token
    space_id = get_space_id("space_views", provider_host, token)
    data = {
        "triggers": ["customMetadata"],
        "customMetadata": {"always": True, "fields": ["string"], "exists": ["string"]},
    }

    file_id = lookup_file_id("space_views/file_json", provider_host, token)
    assert_file_id_in_file_changes(provider_host, token, space_id, data, file_id)

    res = subscribe_to_file_changes(provider_host, token, space_id, data)
    assert RESULTS["file_changes"] == res.text


def _assert(actual, expected):
    err_msg = f"Expected value: {expected}, but got: {actual}"
    assert actual == expected, err_msg


@repeat_failed(timeout=60)
def wait_for_expected_files_in_query_view(
    query, provider_host, token, view_name, space_name: str
):
    res = query()
    if view_name in ["view1", "view2"]:
        items = [item["key"] for item in res]
    else:
        items = [item["value"] for item in res]
    view_to_expected_files = {
        "view1": [
            "file_json",
            "file_rdf",
            "file_xattrs",
            "file_sp1",
            "file_sp2",
            "file_sp3",
            "file_popularity_example",
        ],
        "view2": [
            "file_json",
            "file_rdf",
            "file_xattrs",
            "file_sp1",
            "file_sp2",
            "file_sp3",
        ],
        "view3": ["file_sp1", "file_sp3"],
        "file-popularity": ["file_popularity_example"],
    }
    for file in view_to_expected_files[view_name]:
        file_id = lookup_file_id(f"{space_name}/{file}", provider_host, token)
        assert file_id in items, f"file {file} not in query view"
    return res


@repeat_failed(timeout=60)
def wait_for_expected_result_in_reduce_query_view(query):
    res = query()
    assert res[0]["value"] == 6, f"expected reduce value 6 but got {res}"
    return res


@repeat_failed(timeout=60)
def assert_file_id_in_file_changes(provider_host, token, space_id, data, file_id):
    res = subscribe_to_file_changes(provider_host, token, space_id, data)
    items = res.text.split("\r\n")
    items = [yaml.load(item, yaml.Loader) for item in items][0:-1]
    assert any(
        item for item in items if item["fileId"] == file_id
    ), f"fileId {file_id} not in file changes"


@repeat_failed(timeout=60)
def wait_for_expected_files_in_file_changes(
    provider_host, token, space_id, data, space_name
):
    res = subscribe_to_file_changes(provider_host, token, space_id, data)
    items = res.text.split("\r\n")
    items = [yaml.load(item, yaml.Loader) for item in items][0:-1]
    items = [item["fileId"] for item in items]
    expected_files = [
        "file_json",
        "file_rdf",
        "file_xattrs",
        "file_sp1",
        "file_sp2",
        "file_sp3",
    ]
    for file in expected_files:
        file_id = lookup_file_id(f"{space_name}/{file}", provider_host, token)
        assert file_id in items, f"file {file} not in file changes"
    return res


def create_example_content_in_space(client, space_name: str):
    space_path = client.absolute_path(space_name)
    file_path = os.path.join(space_path, "file_json")
    client.create_file(file_path)
    file_path = os.path.join(space_path, "file_rdf")
    client.create_file(file_path)
    file_path = os.path.join(space_path, "file_xattrs")
    client.create_file(file_path)
    file_path = os.path.join(space_path, "file_sp1")
    client.create_file(file_path)
    file_path = os.path.join(space_path, "file_sp2")
    client.create_file(file_path)
    file_path = os.path.join(space_path, "file_sp3")
    client.create_file(file_path)
    file_path = os.path.join(space_path, "file_popularity_example")
    client.create_file(file_path)
    client.write("abc123", file_path)


def add_example_metadata_to_files_in_space(provider_host, token, space_name: str):
    file_id = lookup_file_id(f"{space_name}/file_json", provider_host, token)
    json_meta = {"coordinates": [5, 10]}
    set_file_json_metadata(provider_host, token, file_id, json_meta)
    file_id = lookup_file_id(f"{space_name}/file_rdf", provider_host, token)
    rdf_meta = (
        '<?xml version="1.0"?>\n\n'
        '<rdf:RDF\nxmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n'
        'xmlns:si="https://www.w3schools.com/rdf/">\n\n<rdf:Description'
        ' rdf:about="https://www.w3schools.com">\n  <si:title>W3Schools</si:title>\n '
        " <si:author>Jan Egil Refsnes</si:author>\n</rdf:Description>\n\n</rdf:RDF>"
    )
    set_file_rdf_metadata(provider_host, token, file_id, rdf_meta)
    file_id = lookup_file_id(f"{space_name}/file_xattrs", provider_host, token)
    xattrs_meta = {"licence": "MIT"}
    set_file_extended_attribute(provider_host, token, file_id, xattrs_meta)
    file_id = lookup_file_id(f"{space_name}/file_sp1", provider_host, token)
    xattrs_meta = {"latitude": 5, "longitude": 10}
    set_file_extended_attribute(provider_host, token, file_id, xattrs_meta)
    file_id = lookup_file_id(f"{space_name}/file_sp2", provider_host, token)
    xattrs_meta = {"latitude": 10, "longitude": 5}
    set_file_extended_attribute(provider_host, token, file_id, xattrs_meta)
    file_id = lookup_file_id(f"{space_name}/file_sp3", provider_host, token)
    xattrs_meta = {"latitude": 0, "longitude": 0}
    set_file_extended_attribute(provider_host, token, file_id, xattrs_meta)
