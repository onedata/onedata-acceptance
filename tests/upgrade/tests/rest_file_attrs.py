"""This module contains tests of shares, handles, datasets and archives operations
after environment upgrade"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2025 ACK CYFRONET AGH"
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
from tests.upgrade.utils.upgrade_utils import (
    UpgradeTest,
)


SPACE_NAME = "space_posix"

TEXT = "example"


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
    zone_host = tests_controller.hosts["onezone"]["hostname"]
    token = tests_controller.users["user1"].token
    admin_token = tests_controller.users["admin"].token
    client = tests_controller.get_client("user1", "oneclient-1", "client11")

    # create file, hardlink and symlink
    create_example_content_in_space(client)


def verify_metadata(tests_controller):
    provider_host = tests_controller.hosts["oneprovider-1"]["hostname"]
    zone_host = tests_controller.hosts["onezone"]["hostname"]
    token = tests_controller.users["user1"].token
    admin_token = tests_controller.users["admin"].token

    # assert the same metadata in files after upgrade
    file_id = lookup_file_id(f"{SPACE_NAME}/file_json", provider_host, token)
    res = get_file_json_metadata(provider_host, token, file_id)
    assert res.json() == JSON_META

    file_id = lookup_file_id(f"{SPACE_NAME}/file_rdf", provider_host, token)
    res = get_file_rdf_metadata(provider_host, token, file_id)
    assert res.text == RDF_META

    file_id = lookup_file_id(f"{SPACE_NAME}/file_xattrs", provider_host, token)
    res = get_file_extended_attributes(provider_host, token, file_id)
    formatted_res = [{k: v} for k, v in sorted(res.json().items())]
    assert formatted_res == XATTRS_META

    for xattr_meta in XATTRS_META:
        (key,) = (xattr_meta.keys(),)
        res = get_file_extended_attributes(provider_host, token, file_id, attribute=key)
        assert res.json() == xattr_meta

    # successfully modify existing metadata
    file_id = lookup_file_id(f"{SPACE_NAME}/file_json", provider_host, token)
    delete_file_json_metadata(provider_host, token, file_id)

    new_json_meta = {"new": "meta"}

    set_file_json_metadata(provider_host, token, file_id, new_json_meta)
    res = get_file_json_metadata(provider_host, token, file_id)
    assert res.json() == new_json_meta

    file_id = lookup_file_id(f"{SPACE_NAME}/file_rdf", provider_host, token)
    delete_file_rdf_metadata(provider_host, file_id, token)

    new_rdf_meta = (
        '<?xml version="1.0"?>\n\n'
        '<rdf:RDF\nxmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"\n'
        'xmlns:si="https://www.w3schools.com/rdf/">\n\n<rdf:Description'
        ' rdf:about="https://www.w3schools.com">\n  <si:title>W3Schools</si:title>\n '
        " <si:author>New Author Refsnes</si:author>\n</rdf:Description>\n\n</rdf:RDF>"
    )

    set_file_rdf_metadata(provider_host, token, file_id, new_rdf_meta)
    res = get_file_rdf_metadata(provider_host, token, file_id)
    assert res.text == new_rdf_meta

    file_id = lookup_file_id(f"{SPACE_NAME}/file_xattrs", provider_host, token)
    delete_file_extended_attributes(provider_host, token, file_id, keys=["license1"])

    new_xattr = {"license4": "MIT4"}

    set_file_extended_attribute(provider_host, token, file_id, new_xattr)
    res = get_file_extended_attributes(provider_host, token, file_id)
    formatted_res = [{k: v} for k, v in sorted(res.json().items())]
    XATTRS_META.remove({"licence1": "MIT1"})
    new_expected_result = XATTRS_META
    new_expected_result.append(new_xattr)
    assert formatted_res == new_expected_result


def create_example_content_in_space(client):
    space_path = client.absolute_path(SPACE_NAME)
    file_path = os.path.join(space_path, "file_attrs")
    client.create_file(file_path)
    client.write(TEXT, file_path)
    link_path = os.path.join(space_path, "file_attrs_hardlink")
    client.create_hardlink(file_path, link_path)
    link_path = os.path.join(space_path, "file_attrs_symlink")
    client.create_symlink(file_path, link_path)
