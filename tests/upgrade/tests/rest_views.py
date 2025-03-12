"""This module contains tests of view operations after environment upgrade"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import os
import time
from functools import partial

from tests.upgrade.utils.rest import (
    configure_file_popularity_mechanism_in_the_space,
    create_view,
    get_provider_configuration,
    get_space_id,
    lookup_file_id,
    query_view,
    set_file_extended_attribute,
    set_file_json_metadata,
    set_file_rdf_metadata,
    subscribe_to_file_events,
    update_view_reduce_function,
)
from tests.upgrade.utils.upgrade_utils import UpgradeTest
from tests.utils.http_exceptions import HTTPError


def get_tests(tests_controller):
    return [
        UpgradeTest(
            "rest views test",
            partial(setup, tests_controller),
            partial(verify, tests_controller),
        ),
        UpgradeTest(
            "rest views multi providers",
            partial(setup_2_providers, tests_controller),
            partial(verify_2_providers, tests_controller),
        ),
        UpgradeTest(
            "rest subscribe events",
            partial(setup_subscribe_events, tests_controller),
            partial(verify_subscribe_events, tests_controller),
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
def setup(tests_controller):
    client = tests_controller.mount_client("user1", "oneclient-1", "client11")
    provider_host = tests_controller.hosts["oneprovider-1"]["hostname"]
    token = tests_controller.users["user1"].token
    admin_token = tests_controller.users["admin"].token
    space_id = get_space_id("space_posix", provider_host, token)

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
    space_path = client.absolute_path("space_posix")
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

    # create metadata
    file_id = lookup_file_id("space_posix/file_json", provider_host, token)
    json_meta = {"coordinates": [5, 10]}
    set_file_json_metadata(provider_host, token, file_id, json_meta)
    file_id = lookup_file_id("space_posix/file_rdf", provider_host, token)
    rdf_meta = (
        '<?xml version="1.0"?>\n\n'
        '<rdf:RDF\nxmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n'
        'xmlns:si="https://www.w3schools.com/rdf/">\n\n<rdf:Description'
        ' rdf:about="https://www.w3schools.com">\n  <si:title>W3Schools</si:title>\n '
        " <si:author>Jan Egil Refsnes</si:author>\n</rdf:Description>\n\n</rdf:RDF>"
    )
    set_file_rdf_metadata(provider_host, token, file_id, rdf_meta)
    file_id = lookup_file_id("space_posix/file_xattrs", provider_host, token)
    xattrs_meta = {"licence": "MIT"}
    set_file_extended_attribute(provider_host, token, file_id, xattrs_meta)
    file_id = lookup_file_id("space_posix/file_sp1", provider_host, token)
    xattrs_meta = {"latitude": 5, "longitude": 10}
    set_file_extended_attribute(provider_host, token, file_id, xattrs_meta)
    file_id = lookup_file_id("space_posix/file_sp2", provider_host, token)
    xattrs_meta = {"latitude": 10, "longitude": 5}
    set_file_extended_attribute(provider_host, token, file_id, xattrs_meta)
    file_id = lookup_file_id("space_posix/file_sp3", provider_host, token)
    xattrs_meta = {"latitude": 0, "longitude": 0}
    set_file_extended_attribute(provider_host, token, file_id, xattrs_meta)

    # add reduce function to view
    update_view_reduce_function(provider_host, token, space_id, VIEW4, REDUCE_FUNC)

    # first call always does not work
    # query views, and save results
    time.sleep(60)
    RESULTS["view1"] = query_view(provider_host, token, space_id, VIEW1)
    RESULTS["view2"] = query_view(provider_host, token, space_id, VIEW2)
    RESULTS["view3"] = query_view(
        provider_host,
        token,
        space_id,
        VIEW3,
        spatial=True,
        start_range="[0,0]",
        end_range="[5,10]",
    )
    RESULTS["view4"] = query_view(provider_host, token, space_id, VIEW4)
    RESULTS["file-popularity"] = query_view(
        provider_host, token, space_id, "file-popularity"
    )

    RESULTS["view1"] = query_view(provider_host, token, space_id, VIEW1)
    RESULTS["view2"] = query_view(provider_host, token, space_id, VIEW2)
    RESULTS["view3"] = query_view(
        provider_host,
        token,
        space_id,
        VIEW3,
        spatial=True,
        start_range="[0,0]",
        end_range="[5,10]",
    )
    RESULTS["view4"] = query_view(provider_host, token, space_id, VIEW4)
    RESULTS["file-popularity"] = query_view(
        provider_host, token, space_id, "file-popularity"
    )

    # sleep is necessary as events are processed asynchronously and there is possible race
    # between client unmounting (which is done after the setup) and processing all its events
    # by provider.
    time.sleep(10)


def setup_2_providers(tests_controller):
    multi_provider_suite = "oneprovider-2" in tests_controller.hosts
    if not multi_provider_suite:
        return

    provider_host = tests_controller.hosts["oneprovider-1"]["hostname"]
    provider_host2 = tests_controller.hosts["oneprovider-2"]["hostname"]
    prov1_id = get_provider_configuration(provider_host)["providerId"]
    prov2_id = get_provider_configuration(provider_host2)["providerId"]

    token = tests_controller.users["user1"].token
    space_id = get_space_id("space_posix", provider_host, token)

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

    time.sleep(60)
    RESULTS["view5"] = query_view(provider_host2, token, space_id, VIEW5)
    RESULTS["view5"] = query_view(provider_host2, token, space_id, VIEW5)

    try:
        query_view(provider_host2, token, space_id, VIEW6)
    except HTTPError as e:
        RESULTS["view6"] = e.response.text


def setup_subscribe_events(tests_controller):
    provider_host = tests_controller.hosts["oneprovider-1"]["hostname"]
    token = tests_controller.users["user1"].token
    space_id = get_space_id("space_posix", provider_host, token)

    data = {
        "triggers": ["customMetadata"],
        "customMetadata": {"always": True, "fields": ["string"], "exists": ["string"]},
    }

    res = subscribe_to_file_events(provider_host, token, space_id, data)
    time.sleep(10)
    RESULTS["file_events"] = res.text


def verify(tests_controller):
    provider_host = tests_controller.hosts["oneprovider-1"]["hostname"]
    token = tests_controller.users["user1"].token
    space_id = get_space_id("space_posix", provider_host, token)

    # is order guaranteed ?
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
    # _assert(len(RESULTS["view1"]), 7)
    _assert(len(RESULTS["view2"]), 6)
    _assert(len(RESULTS["view3"]), 2)
    _assert(RESULTS["view4"][0]["value"], 6)
    assert RESULTS["file-popularity"] == query_view(
        provider_host, token, space_id, "file-popularity"
    )


def verify_2_providers(tests_controller):
    multi_provider_suite = "oneprovider-2" in tests_controller.hosts
    if not multi_provider_suite:
        return
    provider_host = tests_controller.hosts["oneprovider-1"]["hostname"]
    provider_host2 = tests_controller.hosts["oneprovider-2"]["hostname"]
    token = tests_controller.users["user1"].token
    space_id = get_space_id("space_posix", provider_host, token)

    query_view(provider_host2, token, space_id, VIEW5)
    _assert(RESULTS["view5"], query_view(provider_host2, token, space_id, VIEW5))
    try:
        query_view(provider_host2, token, space_id, VIEW6)
    except HTTPError as e:
        _assert(RESULTS["view6"], e.response.text)


def verify_subscribe_events(tests_controller):
    provider_host = tests_controller.hosts["oneprovider-1"]["hostname"]
    token = tests_controller.users["user1"].token
    space_id = get_space_id("space_posix", provider_host, token)
    data = {
        "triggers": ["customMetadata"],
        "customMetadata": {"always": True, "fields": ["string"], "exists": ["string"]},
    }

    res = subscribe_to_file_events(provider_host, token, space_id, data)
    assert RESULTS["file_events"] == res.text
    assert RESULTS["file_events"] != ""


def _assert(actual, expected):
    err_msg = f"Expected value: {expected}, but got: {actual}"
    assert actual == expected, err_msg
