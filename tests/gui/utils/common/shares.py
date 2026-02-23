"""Utils mainly for testing public and private shares,
concerning mainly XML editor and metadata fields."""

__author__ = "Jakub Karczewski"
__copyright__ = "Copyright (C) 2025 Onedata (onedata.org)"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import xml.etree.ElementTree as ET

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.common.miscellaneous import switch_to_iframe
from tests.gui.utils import PublicShareView as public_share
from tests.utils.utils import repeat_failed

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
    "datacite": "http://datacite.org/schema/kernel-4",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
}


def _register_xml_namespaces_openaire():
    for prefix, uri in NAMESPACES_OPENAIRE.items():
        ET.register_namespace(prefix, uri)


def _map_namespace_prefix_to_uri_openaire(prefix):
    return NAMESPACES_OPENAIRE.get(prefix)


def _map_namespace_prefix_to_uri_datacite(prefix):
    return NAMESPACES_DATACITE.get(prefix)


def _register_xml_namespaces_datacite():
    for prefix, uri in NAMESPACES_DATACITE.items():
        ET.register_namespace(prefix, uri)


def _get_xml_editor_data(selenium, browser_id):
    return selenium[browser_id].execute_script(
        "return ace.edit(document.querySelector('.ace_editor')).getValue()"
    )


def _replace_xml_editor_data(selenium, browser_id, new_data):
    selenium[browser_id].execute_script(
        """
        var editor = ace.edit(document.querySelector('.ace_editor'));
        editor.setValue(arguments[0], -1);
        """,
        new_data,
    )


def _check_editor_appeared(selenium, browser_id):
    driver = selenium[browser_id]
    try:
        _ = _get_xml_data_openaire(driver)
    except RuntimeError:
        switch_to_iframe(selenium, browser_id)
        _ = _get_xml_data_openaire(driver)


@repeat_failed(timeout=WAIT_FRONTEND)
def _get_xml_data_openaire(driver):
    return public_share(driver).xml_data_ace_editor


def _is_metadata_field_option_choosable(field_name):
    return field_name.lower() in [
        "category",
        "name of organisation uploading the data",
        "copyright licence url of the digital object",
        "material",
    ]


def _is_metadata_field_default_in_dublin_core_form(field_name):
    return field_name.lower() in ["title", "creator", "description", "date"]


def _is_metadata_field_default_in_edm_form(field_name):
    return field_name.lower() in [
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
    ]
