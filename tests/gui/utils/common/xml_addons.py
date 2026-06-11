"""Helper utilities for validating public and private shares,
with a primary focus on the XML editor and metadata handling."""

__author__ = "Jakub Karczewski"
__copyright__ = "Copyright (C) 2026 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import xml.etree.ElementTree as ET
from typing import Any

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.common.miscellaneous import switch_to_iframe
from tests.gui.utils import PublicShareView as public_share
from tests.utils.utils import repeat_failed
from tests.conftest import SeleniumDrivers

NAMESPACES_OPENAIRE = {
    "oaire": "http://namespace.openaire.eu/schema/oaire/",
    "datacite": "http://datacite.org/schema/kernel-4",
    "dc": "http://purl.org/dc/elements/1.1/",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "dcterms": "http://purl.org/dc/terms/",
    "vc": "http://www.w3.org/2007/XMLSchema-versioning",
}

NAMESPACES_DATACITE = {
    "": "http://datacite.org/schema/kernel-4",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}

INITIAL_FIELDS = {
    "dublin_core": {"title", "creator", "description", "date"},
    "edm": {
        "title",
        "description/caption",
        "category",
        "subject",
        "type of object",
        "parent entity (collection, object, site…)",
        "material",
        "description of digital object",
        "type of digital object",
        "content provider institution",
        "name of organisation uploading the data",
        "copyright licence url of the digital object",
    },
}

SELECTABLE_FIELDS = {
    "edm": {
        "category",
        "name of organisation uploading the data",
        "copyright licence url of the digital object",
        "material",
    }
}


def register_namespace_by_metadata_type(metadata_type: Any) -> Any:
    namespaces = (
        NAMESPACES_OPENAIRE
        if metadata_type.lower() == "openaire"
        else NAMESPACES_DATACITE
    )
    for prefix, uri in namespaces.items():
        ET.register_namespace(prefix, uri)


def map_namespace_prefix_to_uri(prefix: Any, metadata_type: Any) -> Any:
    prefix = prefix.lower()
    if metadata_type.lower() == "openaire":
        return NAMESPACES_OPENAIRE.get(prefix)

    if prefix == "datacite":
        # In the NAMESPACES_DATACITE dictionary the default namespace
        # is stored under an empty string key ("").
        return NAMESPACES_DATACITE.get("")
    return NAMESPACES_DATACITE.get(prefix)


def resolve_xml_tag_for_et_search(tag: Any, metadata_type: Any) -> Any:
    if tag.startswith("{") or ":" not in tag:
        # If the tag is already in the format {uri}local_name or
        # doesn't contain a colon, that is possibly a namespace separator
        return tag

    prefix, local_name = tag.split(":", 1)
    uri = map_namespace_prefix_to_uri(prefix, metadata_type)

    # If the prefix is not recognized, treat the tag as a literal
    # (assume the colon is not indicating a namespace).
    if uri is None:
        return tag
    return f"{{{uri}}}{local_name}"


def get_xml_editor_data(driver: Any) -> Any:
    return driver.execute_script(
        "return ace.edit(document.querySelector('.ace_editor')).getValue()"
    )


def replace_xml_editor_data(driver: Any, new_data: Any) -> Any:
    driver.execute_script(
        """
        var editor = ace.edit(document.querySelector('.ace_editor'));
        editor.setValue(arguments[0], -1);
        """,
        new_data,
    )


def check_ace_editor_appeared(selenium: SeleniumDrivers, browser_id: Any) -> Any:
    driver = selenium[browser_id]
    try:
        _ = get_xml_data_openaire(driver)
    except RuntimeError:
        switch_to_iframe(selenium, browser_id)
        _ = get_xml_data_openaire(driver)


@repeat_failed(timeout=WAIT_FRONTEND)
def get_xml_data_openaire(driver: Any) -> Any:
    return public_share(driver).xml_data_ace_editor


def is_metadata_field_option_selectable_edm(field_name: Any) -> Any:
    return field_name.lower() in SELECTABLE_FIELDS["edm"]


def is_name_in_initial_form_fields(field_name: Any, metadata_type: Any) -> Any:
    return field_name.lower() in INITIAL_FIELDS[metadata_type.lower()]
