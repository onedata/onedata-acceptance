"""This module contains tests of operations on file with metadata
after environment upgrade"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 onedata.org"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import os
from functools import partial

from tests.upgrade.utils.rest_utils import (
    delete_file_extended_attributes,
    delete_file_json_metadata,
    delete_file_rdf_metadata,
    get_file_extended_attributes,
    get_file_json_metadata,
    get_file_rdf_metadata,
    lookup_file_id,
    set_file_extended_attribute,
    set_file_json_metadata,
    set_file_rdf_metadata,
)
from tests.upgrade.utils.upgrade_utils import UpgradeTest

SPACE_NAME = "space_posix"

JSON_META = {"hello": {"world": ["hello", "world"]}}

RDF_META = (
    '<?xml version="1.0"?>\n\n'
    '<rdf:RDF\nxmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n'
    'xmlns:si="https://www.w3schools.com/rdf/">\n\n<rdf:Description'
    ' rdf:about="https://www.w3schools.com">\n  <si:title>W3Schools</si:title>\n '
    " <si:author>Jan Egil Refsnes</si:author>\n</rdf:Description>\n\n</rdf:RDF>"
)

XATTRS_META = [{"licence1": "MIT1"}, {"licence2": "MIT2"}, {"licence3": "MIT3"}]


def get_tests(tests_controller):
    return [
        UpgradeTest(
            "rest metadata test",
            partial(setup_metadata, tests_controller),
            partial(verify_metadata, tests_controller),
        )
    ]


def setup_metadata(tests_controller):
    provider_host = tests_controller.hosts["oneprovider-1"]["hostname"]
    token = tests_controller.users["user1"].token
    client = tests_controller.get_client("user1", "oneclient-1", "client11")

    # create files
    create_example_content_in_space(client)

    # create metadata
    add_example_metadata_to_files_in_space(provider_host, token)


def verify_metadata(tests_controller):
    provider_host = tests_controller.hosts["oneprovider-1"]["hostname"]
    token = tests_controller.users["user1"].token

    # assert the same metadata in files after upgrade
    err_msg = "Expected metadata:\n {},\n but got:\n {}"
    file_id = lookup_file_id(f"{SPACE_NAME}/file_metadata", provider_host, token)
    res = get_file_json_metadata(provider_host, token, file_id)
    assert res.json() == JSON_META, err_msg.format(JSON_META, res.json())

    res = get_file_rdf_metadata(provider_host, token, file_id)
    assert res.text == RDF_META, err_msg.format(RDF_META, res.text)

    res = get_file_extended_attributes(provider_host, token, file_id)
    formatted_res = [{k: v} for k, v in sorted(res.json().items())]
    assert formatted_res == XATTRS_META, err_msg.format(XATTRS_META, formatted_res)

    for xattr_meta in XATTRS_META:
        (key,) = (xattr_meta.keys(),)
        res = get_file_extended_attributes(provider_host, token, file_id, attribute=key)
        assert res.json() == xattr_meta, err_msg.format(xattr_meta, res.json())

    # successfully modify existing metadata
    delete_file_json_metadata(provider_host, token, file_id)

    new_json_meta = {"new": "meta"}

    set_file_json_metadata(provider_host, token, file_id, new_json_meta)
    res = get_file_json_metadata(provider_host, token, file_id)
    assert res.json() == new_json_meta, err_msg.format(new_json_meta, res.json())

    delete_file_rdf_metadata(provider_host, token, file_id)

    new_rdf_meta = (
        '<?xml version="1.0"?>\n\n'
        '<rdf:RDF\nxmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n'
        'xmlns:si="https://www.w3schools.com/rdf/">\n\n<rdf:Description'
        ' rdf:about="https://www.w3schools.com">\n  <si:title>W3Schools</si:title>\n '
        " <si:author>New Author Refsnes</si:author>\n</rdf:Description>\n\n</rdf:RDF>"
    )

    set_file_rdf_metadata(provider_host, token, file_id, new_rdf_meta)
    res = get_file_rdf_metadata(provider_host, token, file_id)
    assert res.text == new_rdf_meta, err_msg.format(new_rdf_meta, res.text)

    delete_file_extended_attributes(provider_host, token, file_id, keys=["licence1"])

    new_xattr = {"licence4": "MIT4"}

    set_file_extended_attribute(provider_host, token, file_id, new_xattr)
    res = get_file_extended_attributes(provider_host, token, file_id)

    formatted_res = [{k: v} for k, v in sorted(res.json().items())]
    new_expected_result = XATTRS_META.copy()
    new_expected_result.remove({"licence1": "MIT1"})
    new_expected_result.append(new_xattr)
    assert formatted_res == new_expected_result, err_msg.format(
        new_expected_result, formatted_res
    )


def create_example_content_in_space(client):
    space_path = client.absolute_path(SPACE_NAME)
    file_path = os.path.join(space_path, "file_metadata")
    client.create_file(file_path)


def add_example_metadata_to_files_in_space(provider_host, token):
    file_id = lookup_file_id(f"{SPACE_NAME}/file_json", provider_host, token)
    set_file_json_metadata(provider_host, token, file_id, JSON_META)
    set_file_rdf_metadata(provider_host, token, file_id, RDF_META)
    for xattr_meta in XATTRS_META:
        set_file_extended_attribute(provider_host, token, file_id, xattr_meta)
