import xml.etree.ElementTree as ET

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.common.miscellaneous import switch_to_iframe
from tests.gui.utils import PublicShareView as public_share
from tests.utils.utils import repeat_failed


def _register_xml_namespaces_openaire():
    ET.register_namespace("oaire", "http://namespace.openaire.eu/schema/oaire/")
    ET.register_namespace("datacite", "http://datacite.org/schema/kernel-4")
    ET.register_namespace("dc", "http://purl.org/dc/elements/1.1/")
    ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")
    ET.register_namespace("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    ET.register_namespace("dcterms", "http://purl.org/dc/terms/")
    ET.register_namespace("vc", "http://www.w3.org/2007/XMLSchema-versioning")


def _register_xml_namespaces_datacite():
    ET.register_namespace("", "http://datacite.org/schema/kernel-4")
    ET.register_namespace("xsi", "http://www.w3.org/2001/XMLSchema-instance")


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
    return field_name in [
        "category",
        "name of organisation uploading the data",
        "copyright licence url of the digital object",
        "material",
    ]
