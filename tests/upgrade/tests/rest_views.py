"""This module contains tests of view operations after environment upgrade"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import os
import time
from functools import partial

from tests.upgrade.utils.rest import (
    create_view,
    get_provider_configuration,
    get_space_id,
    lookup_file_id,
    query_view,
    set_file_extended_attribute,
    set_file_json_metadata,
    set_file_rdf_metadata,
    update_view_reduce_function,
)
from tests.upgrade.utils.upgrade_utils import UpgradeTest


def get_tests(tests_controller):
    return [
        UpgradeTest(
            "rest views test",
            partial(setup, tests_controller),
            partial(verify, tests_controller),
        )
    ]


map_func_all_files = """
    function(id, type, meta, ctx) {
    if(type == 'file_meta')
        return [id, ctx];
}
"""
map_func_files_with_meta = """
    function(id, type, meta, ctx) {
    if(type == 'custom_metadata')
        return [id, meta];
}
"""
map_func_spatial = """
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
reduce_func = """
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
VIEW4 = "view_double_providers"
VIEW5 = "view_with_reduce"

RESULTS = {}


def setup(tests_controller):
    client = tests_controller.mount_client("user1", "oneclient-1", "client11")
    provider_host = tests_controller.hosts["oneprovider-1"]["hostname"]

    multi_provider_suite = "oneprovider-2" in tests_controller.hosts
    if multi_provider_suite:
        provider_host2 = tests_controller.hosts["oneprovider-2"]["hostname"]

    prov1_id = get_provider_configuration(provider_host)["providerId"]
    if multi_provider_suite:
        prov2_id = get_provider_configuration(provider_host2)["providerId"]

    token = tests_controller.users["user1"].token
    prov_version = tests_controller.test_config["initialVersions"]["oneprovider"]
    prov_version = int(prov_version.split(".")[0])

    space_id = get_space_id("space_posix", provider_host, token)
    _ = create_view(provider_host, token, space_id, VIEW1, map_func_all_files)
    _ = create_view(provider_host, token, space_id, VIEW2, map_func_files_with_meta)
    _ = create_view(
        provider_host, token, space_id, VIEW3, map_func_spatial, spatial=True
    )
    if multi_provider_suite:
        _ = create_view(
        provider_host,
        token,
        space_id,
        VIEW4,
        map_func_all_files,
        providers=[prov1_id, prov2_id],
        )
    _ = create_view(provider_host, token, space_id, VIEW5, map_func_files_with_meta)

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

    file_id = lookup_file_id("space_posix/file_json", provider_host, token)
    json_meta = {"coordinates": [5, 10]}
    set_file_json_metadata(provider_host, token, file_id, json_meta)

    file_id = lookup_file_id("space_posix/file_rdf", provider_host, token)
    rdf_meta = (
        "<?xml"
        ' version="1.0"?>\n\n<rdf:RDF\nxmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\nxmlns:si="https://www.w3schools.com/rdf/">\n\n<rdf:Description'
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

    update_view_reduce_function(provider_host, token, space_id, VIEW5, reduce_func)

    # first call always does not work
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
    if multi_provider_suite:
        RESULTS["view4"] = query_view(provider_host2, token, space_id, VIEW4)
    RESULTS["view5"] = query_view(provider_host, token, space_id, VIEW5)

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
    if multi_provider_suite:
        RESULTS["view4"] = query_view(provider_host2, token, space_id, VIEW4)
    RESULTS["view5"] = query_view(provider_host, token, space_id, VIEW5)

    # sleep is necessary as events are processed asynchronously and there is possible race
    # between client unmounting (which is done after the setup) and processing all its events
    # by provider.
    time.sleep(10)


def verify(tests_controller):
    provider_host = tests_controller.hosts["oneprovider-1"]["hostname"]
    multi_provider_suite = "oneprovider-2" in tests_controller.hosts
    if multi_provider_suite:
        provider_host2 = tests_controller.hosts["oneprovider-2"]["hostname"]
    token = tests_controller.users["user1"].token
    prov_version = tests_controller.test_config["initialVersions"]["oneprovider"]
    prov_version = int(prov_version.split(".")[0])

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
    if multi_provider_suite:
        assert RESULTS["view4"] == query_view(provider_host2, token, space_id, VIEW4)
    assert RESULTS["view5"] == query_view(provider_host, token, space_id, VIEW5)
    _assert(len(RESULTS["view1"]), 9)
    _assert(len(RESULTS["view2"]), 6)
    _assert(len(RESULTS["view3"]), 2)
    if multi_provider_suite:
        _assert(len(RESULTS["view4"]), 9)
    _assert(RESULTS["view5"][0]["value"], 6)


def _assert(actual, expected):
    err_msg = f"Expected value: {expected}, but got: {actual}"
    assert actual == expected, err_msg
