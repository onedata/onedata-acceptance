"""Meta steps implementation for shares GUI tests."""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import xml.etree.ElementTree as ET

import yaml

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.common.copy_paste import send_copied_item_to_other_users
from tests.gui.steps.modals.modal import (
    click_icon_in_share_directory_modal,
    click_modal_button,
    click_panel_button,
    click_share_details_link_in_shares_panel,
    write_name_into_text_field_in_modal,
    write_name_into_text_field_in_panel,
    wt_wait_for_modal_to_appear,
)
from tests.gui.steps.oneprovider.browser import (
    click_menu_for_elem_in_browser,
    click_option_in_data_row_menu_in_browser,
)
from tests.gui.steps.oneprovider.data_tab import assert_browser_in_tab_in_op
from tests.gui.steps.oneprovider.file_browser import (
    click_on_status_tag_for_file_in_file_browser,
)
from tests.gui.steps.oneprovider.private_shares import (
    add_metadata_field_in_dublin_core_form,
    add_property_to_edm_form_in_shares_interface,
    assert_link_on_shares_interface,
    assert_nth_val_edm_form_in_shares_interface,
    assert_val_edm_form_in_shares_interface,
    choose_option_for_publish_handle_service_as_open_data,
    choose_option_for_publish_metadata_as_open_data,
    choose_option_group_in_edm_form_in_shares_interface,
    choose_option_in_edm_form_in_shares_interface,
    click_button_in_description_form,
    click_button_in_form_in_shares_interface,
    write_description_in_description_form,
    write_input_in_form_in_shares_interface,
    write_to_nth_input_in_edm_form_in_shares_interface,
)
from tests.gui.steps.oneprovider.public_shares import (
    assert_data_in_dublin_core_metadata,
    assert_file_browser_in_public_share,
    click_button_in_share,
    copy_link_in_shares_interface,
    open_tab_in_public_share,
)
from tests.gui.steps.oneprovider.shares import (
    change_shares_browser_to_file_browser,
    click_menu_button_on_shares_page,
    click_option_in_share_row_menu,
    click_share_in_shares_browser,
    is_selected_share_named,
)
from tests.gui.steps.onezone.spaces import click_on_option_of_space_on_left_sidebar_menu
from tests.gui.utils import Modals, Popups
from tests.gui.utils import PublicShareView as public_share
from tests.gui.utils.common.xml_addons import (
    check_editor_appeared_openaire,
    get_xml_editor_data,
    is_metadata_field_default_in_dublin_core_form,
    is_metadata_field_default_in_edm_form,
    is_metadata_field_option_choosable,
    replace_xml_editor_data,
    resolve_xml_tag_for_et_search,
    register_namespace_by_metadata_type
)
from tests.gui.utils.generic import WhichBrowser, parse_seq, transform
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.parse(
        'user of {browser_id} creates "{share_name}" share of "{item_name}" file'
    )
)
@wt(
    parsers.parse(
        'user of {browser_id} creates "{share_name}" share of "{item_name}" directory'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def create_share(selenium, browser_id, share_name, item_name, tmp_memory):
    option = "Share / Publish"
    modal_name = "Share / Publish directory"
    button = "Create"

    click_menu_for_elem_in_browser(browser_id, item_name, tmp_memory)
    click_option_in_data_row_menu_in_browser(selenium, browser_id, option)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    write_name_into_text_field_in_modal(selenium, browser_id, share_name, modal_name)
    click_modal_button(selenium, browser_id, button, modal_name)


@wt(
    parsers.parse(
        'user of {browser_id} opens "{share_name}" single share '
        'view of "{item_name}" using "Shared" tag'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def open_single_share_view_by_modal(
    selenium,
    browser_id,
    share_name,
    tmp_memory,
    item_name,
):

    items_browser = transform(WhichBrowser.SHARES_FILE_BROWSER.value)
    status_type = "shared"

    click_on_status_tag_for_file_in_file_browser(
        browser_id, status_type, item_name, tmp_memory
    )
    click_share_details_link_in_shares_panel(selenium, browser_id, share_name)
    assert_browser_in_tab_in_op(selenium, browser_id, tmp_memory, items_browser)
    is_selected_share_named(selenium, browser_id, share_name)


@wt(parsers.parse('user of {browser_id} creates another share named "{share_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_another_share(selenium, browser_id, share_name):
    button = "Create another share"
    modal_name = "Shares"
    create_button = "Create"

    click_panel_button(selenium, browser_id, button, modal_name)
    write_name_into_text_field_in_panel(selenium, browser_id, share_name, modal_name)
    click_panel_button(selenium, browser_id, create_button, modal_name)


@wt(parsers.parse("user of {browser_id} removes current share"))
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_current_share(selenium, browser_id, tmp_memory):
    option = "Remove"
    modal_name = "Remove share"
    button = "Remove"

    click_menu_button_on_shares_page(selenium, browser_id)
    click_option_in_share_row_menu(selenium, browser_id, option)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    click_modal_button(selenium, browser_id, button, modal_name)


@wt(parsers.parse('user of {browser_id} opens shares view of "{space_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def open_shares_view_of_given_space(selenium, browser_id, space_name, tmp_memory):
    option = "Shares, Public Data"
    items_browser = "shares_browser"

    click_on_option_of_space_on_left_sidebar_menu(
        selenium, browser_id, space_name, option
    )
    assert_browser_in_tab_in_op(selenium, browser_id, tmp_memory, items_browser)


@wt(
    parsers.parse(
        'user of {browser_id} opens "{share_name}" single '
        'share view of space "{space_name}" using sidebar'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def open_single_share_view_by_sidebar(
    selenium,
    browser_id,
    share_name,
    tmp_memory,
    space_name,
):
    open_shares_view_of_given_space(selenium, browser_id, space_name, tmp_memory)
    click_share_in_shares_browser(selenium, browser_id, share_name)
    change_shares_browser_to_file_browser(selenium, browser_id, tmp_memory)


@wt(
    parsers.parse(
        'user of {browser_id} hands "{share_name}" share\'s URL of '
        '"{item_name}" to user of {browser2_id}'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def hand_share_url_to_another_user(
    selenium,
    browser_id,
    browser2_id,
    share_name,
    item_name,
    tmp_memory,
    displays,
    clipboard,
):
    modal_name = "Details modal"
    item_type = "URL"
    button = "X"

    copy_url_of_share(selenium, browser_id, share_name, item_name, tmp_memory)
    send_copied_item_to_other_users(
        browser_id, item_type, browser2_id, tmp_memory, displays, clipboard
    )
    click_modal_button(selenium, browser_id, button, modal_name)


@wt(
    parsers.parse(
        'user of {browser_id} copies share URL of "{share_name}" share of "{item_name}"'
    )
)
def copy_url_of_share(selenium, browser_id, share_name, item_name, tmp_memory):
    icon_name = "copy"
    status_type = "shared"

    click_on_status_tag_for_file_in_file_browser(
        browser_id, status_type, item_name, tmp_memory
    )
    click_icon_in_share_directory_modal(selenium, browser_id, share_name, icon_name)


@wt(
    parsers.parse(
        'user of {browser_id} renames current share to "{new_name}"'
        " in single share view"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def rename_share_from_single_view(selenium, browser_id, new_name, tmp_memory):
    option = "Rename"
    modal_name = "Rename share"
    button = "Rename"

    click_menu_button_on_shares_page(selenium, browser_id)
    click_option_in_share_row_menu(selenium, browser_id, option)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    write_name_into_text_field_in_modal(selenium, browser_id, new_name, modal_name)
    click_modal_button(selenium, browser_id, button, modal_name)
    is_selected_share_named(selenium, browser_id, new_name)


@wt(
    parsers.re(
        'user of (?P<browser_id>.*?) copies command for "(?P<command>.*?)" operation in'
        " API section from (file|directory) details modal"
    )
)
def copy_command_from_api_in_file_details_modal(selenium, browser_id, command):
    driver = selenium[browser_id]
    modal = Modals(driver).details_modal
    command = f"{command}\nREST"

    modal.navigation["API"].click()
    modal.api.operations.click()
    Popups(driver).power_select.choose_item(command)
    modal.api.copy_button.click()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) opens "
        r'"(?P<metadata_type>Dublin Core|DataCite|OpenAIRE|Europeana Data Model)"'
        r" Public Data editor in share's private interface"
    )
)
def open_public_data_metadata_editor(selenium, browser_id, metadata_type):
    option = "private"

    open_tab_in_public_share(selenium, browser_id, "Expose as Public Data")
    click_button_in_share(selenium, browser_id, "Choose a handle service", option)
    choose_option_for_publish_handle_service_as_open_data(
        browser_id, "Mock Handle Service", selenium
    )
    click_button_in_share(selenium, browser_id, "Choose a metadata type", option)
    choose_option_for_publish_metadata_as_open_data(browser_id, metadata_type, selenium)

    click_button_in_share(selenium, browser_id, "Proceed", option)


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*?) adds "(?P<description>.*?)" description for'
        r' "(?P<share_name>.*?)" share on '
        r"share's private interface"
    )
)
def add_description_to_share_on_private_interface(selenium, browser_id, description):
    open_tab_in_public_share(selenium, browser_id, "Description")
    click_button_in_description_form(browser_id, selenium, "Create description")
    write_description_in_description_form(
        browser_id, description, "description field", selenium
    )
    click_button_in_description_form(browser_id, selenium, "Save")


@wt(
    parsers.parse(
        "user of {browser_id} fills the input fields of Dublin Core form"
        " with:\n{config}"
    )
)
def fill_inputs_in_dublin_core_metadata_form(selenium, browser_id, config):
    """
    Fill Dublin Core metadata form according to given config.
    Config format given in yaml is as follows:

            metadata field: value               ---> single value
            metadata field:
                - first value
                - second value                  ---> multiple values
            ...
    """
    option = "private"
    tab_name = "Expose as Public Data"

    open_tab_in_public_share(selenium, browser_id, tab_name)
    config = yaml.load(config, yaml.Loader)

    for option, value in config.items():
        option = option.lower()

        if not is_metadata_field_default_in_dublin_core_form(option):
            add_metadata_field_in_dublin_core_form(selenium[browser_id], option)

        if not isinstance(value, list):  # single string value
            write_input_in_form_in_shares_interface(browser_id, value, option, selenium)
        else:
            write_input_in_form_in_shares_interface(
                browser_id, value[0], option, selenium
            )
            for val in value[1:]:
                click_button_in_form_in_shares_interface(
                    browser_id, f"Add another {option}", selenium
                )
                write_input_in_form_in_shares_interface(
                    browser_id, val, option, selenium
                )


@wt(
    parsers.parse(
        "user of {browser_id} sees that properties of Dublin Core"
        " metadata in share's {option} interface are"
        " like the following:\n{config}"
    )
)
def assert_properties_in_dublin_core_metadata_form(
    selenium, browser_id, metadata_type, config
):
    """
    Assert Dublin Core metadata values according to given config.
    Config format given in yaml is in fill_inputs_in_dublin_core_metadata_form function.
    """
    config = yaml.load(config, yaml.Loader)
    for _, data in config.items():
        if metadata_type.lower() == "dublin core":
            if not isinstance(data, list):
                assert_data_in_dublin_core_metadata(browser_id, data, selenium)
            else:
                for item in data:
                    assert_data_in_dublin_core_metadata(browser_id, item, selenium)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) opens"
        r" share's file browser on share's public interface"
    )
)
def open_shares_file_browser(selenium, browser_id, tmp_memory):
    open_tab_in_public_share(selenium, browser_id, "Files")
    assert_file_browser_in_public_share(selenium, browser_id, tmp_memory)


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*?) sends "Public handle link"'
        r" from share's private interface to"
        r" user of (?P<browser2_id>.*?)"
    )
)
def send_public_handle_link_to_user(
    selenium, browser_id, browser2_id, tmp_memory, displays, clipboard
):
    item_type = "URL"
    link_type = "Public handle link"

    assert_link_on_shares_interface(browser_id, link_type, selenium)
    copy_link_in_shares_interface(browser_id, selenium)

    send_copied_item_to_other_users(
        browser_id, item_type, browser2_id, tmp_memory, displays, clipboard
    )


@wt(
    parsers.parse(
        "user of {browser_id} fills text section fields of EDM metadata form"
        " with:\n{config}"
    )
)
def fill_inputs_in_edm_metadata_form(
    selenium, browser_id, config, numerals, num_to_ordinal
):
    """
    Fill EDM metadata form according to given config.
    Config format given in yaml is as follows:

            metadata field: value               ---> single value
            metadata field:
                - first value
                - second value                  ---> multiple values
            Material:
                group: material group
                value: material value
    """
    config = yaml.load(config, yaml.Loader)

    for field_name, value in config.items():
        field_name = field_name.lower()
        if not is_metadata_field_default_in_edm_form(field_name):
            add_property_to_edm_form_in_shares_interface(
                browser_id, selenium, field_name
            )

        if is_metadata_field_option_choosable(
            field_name
        ):  # these fields cannot have literal before them
            if field_name != "material":
                choose_option_in_edm_form_in_shares_interface(
                    browser_id, value, field_name, selenium, expand_dropdown=True
                )

            else:  # choosing material involves also choosing options group first
                choose_option_group_in_edm_form_in_shares_interface(
                    browser_id,
                    value["group"],
                    field_name,
                    selenium,
                    expand_dropdown=True,
                )
                choose_option_in_edm_form_in_shares_interface(
                    browser_id,
                    value["value"],
                    field_name,
                    selenium,
                    expand_dropdown=False,
                )

        else:
            if isinstance(value, list):
                for i, val in enumerate(value):
                    if i > 0:
                        # if it's not the first value for given field,
                        # we need to click "Add another ..." button before writing value
                        add_property_to_edm_form_in_shares_interface(
                            browser_id, selenium, field_name
                        )
                    write_to_nth_input_in_edm_form_in_shares_interface(
                        browser_id,
                        val,
                        field_name,
                        selenium,
                        num_to_ordinal[i],
                        numerals,
                    )
            else:
                write_to_nth_input_in_edm_form_in_shares_interface(
                    browser_id, value, field_name, selenium, "first", numerals
                )


@wt(
    parsers.parse(
        "user of {browser_id} sees that fields of EDM metadata form"
        " are like the following:\n{config}"
    )
)
def assert_properties_in_edm_metadata_form(
    selenium, browser_id, config, numerals, num_to_ordinal
):
    """
    Assert EDM metadata values according to given config.
    Config format given in yaml is in fill_inputs_in_edm_metadata_form function.
    """
    config = yaml.load(config, yaml.Loader)

    for field_name, value in config.items():
        field_name = field_name.lower()
        if is_metadata_field_option_choosable(field_name):
            assert_val_edm_form_in_shares_interface(
                browser_id, value, field_name, selenium, numerals
            )
        else:
            if isinstance(value, list):
                for i, val in enumerate(value):
                    assert_nth_val_edm_form_in_shares_interface(
                        browser_id,
                        val,
                        field_name,
                        selenium,
                        num_to_ordinal[i],
                        numerals,
                    )
            else:
                assert_nth_val_edm_form_in_shares_interface(
                    browser_id, value, field_name, selenium, "first", numerals
                )


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*?) renames "(?P<share_name>.*?)"'
        r' share to "(?P<new_name>.*?)"'
        r" on share's private interface"
    )
)
def rename_share_on_private_interface(selenium, browser_id, new_name, tmp_memory):
    modal_name = "Rename share"
    click_menu_button_on_shares_page(selenium, browser_id)
    click_option_in_share_row_menu(selenium, browser_id, "Rename")
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    write_name_into_text_field_in_modal(selenium, browser_id, new_name, modal_name)
    click_modal_button(selenium, browser_id, "Rename", modal_name)


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*?) sees that "(?P<metadata_type>DataCite|OpenAIRE)"'
        r" XML data contains nodes like:"
        r" (?P<data>.*?) on share's (private|public) interface"
    )
)
def assert_xml_data_in_edm_form_in_shares_interface(
    selenium, browser_id, data, metadata_type
):
    check_editor_appeared_openaire(selenium, browser_id)
    xml_data = get_xml_editor_data(selenium[browser_id])
    root = ET.fromstring(xml_data)

    for elem in parse_seq(data):
        elem_for_search = resolve_xml_tag_for_et_search(elem, metadata_type)
        assert (
            root.find(f".//{elem_for_search}") is not None
        ), f"Node with name: {elem} was not found in XML data"


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) modifies"
        r' "(?P<metadata_type>DataCite|OpenAIRE)" XML'
        r' element with "(?P<tag>.*?)" tag by changing its text to "(?P<new_text>.*?)"'
        r" in share's private interface"
    )
)
def modify_xml_data_in_edm_form_in_shares_interface(
    selenium, browser_id, metadata_type, tag, new_text
):
    driver = selenium[browser_id]
    public_share(driver).modify_button.click()

    check_editor_appeared_openaire(selenium, browser_id)
    xml_data = get_xml_editor_data(driver)

    register_namespace_by_metadata_type(metadata_type)
    root = ET.fromstring(xml_data)
    tag_for_search = resolve_xml_tag_for_et_search(tag, metadata_type)

    elem = root.find(f".//{tag_for_search}")
    assert elem is not None, f"Node with tag: {tag} was not found in XML data"

    elem.text = new_text
    replace_xml_editor_data(
        driver,
        ET.tostring(root, encoding="utf-8", xml_declaration=True).decode("utf-8"),
    )
    public_share(driver).save_button.click()


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) sees that"
        r' "(?P<metadata_type>DataCite|OpenAIRE)" XML node with "(?P<tag>.*?)"'
        r' tag has "(?P<text>.*?)" value'
        r" in share's private interface"
    )
)
def assert_xml_node_value(selenium, browser_id, tag, text, metadata_type):
    check_editor_appeared_openaire(selenium, browser_id)

    xml_data = get_xml_editor_data(selenium[browser_id])
    root = ET.fromstring(xml_data)
    tag_for_search = resolve_xml_tag_for_et_search(tag, metadata_type)
    elem = root.find(f".//{tag_for_search}")
    assert elem is not None, f"Node with tag: {tag} was not found in XML data"

    assert (
        elem.text == text
    ), f"Value of XML node: {elem.text} does not match expected: {text}"
