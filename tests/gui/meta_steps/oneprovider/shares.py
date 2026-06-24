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
from tests.gui.types import Clipboard, TmpMemory
from tests.gui.utils import Modals, Popups
from tests.gui.utils import PublicShareView as public_share
from tests.gui.utils.common.xml_addons import (
    check_ace_editor_appeared,
    get_xml_editor_data,
    is_metadata_field_option_selectable_edm,
    is_name_in_initial_form_fields,
    register_namespace_by_metadata_type,
    replace_xml_editor_data,
    resolve_xml_tag_for_et_search,
)
from tests.gui.utils.generic import WhichBrowser, parse_seq, transform
from tests.types import SeleniumDrivers
from tests.utils.acceptance_utils import num_to_ordinal
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
def create_share(
    selenium: SeleniumDrivers,
    browser_id: str,
    share_name: str,
    item_name: str,
    tmp_memory: TmpMemory,
) -> None:
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
    selenium: SeleniumDrivers,
    browser_id: str,
    share_name: str,
    tmp_memory: TmpMemory,
    item_name: str,
) -> None:

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
def create_another_share(
    selenium: SeleniumDrivers, browser_id: str, share_name: str
) -> None:
    button = "Create another share"
    modal_name = "Shares"
    create_button = "Create"

    click_panel_button(selenium, browser_id, button, modal_name)
    write_name_into_text_field_in_panel(selenium, browser_id, share_name, modal_name)
    click_panel_button(selenium, browser_id, create_button, modal_name)


@wt(parsers.parse("user of {browser_id} removes current share"))
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_current_share(
    selenium: SeleniumDrivers, browser_id: str, tmp_memory: TmpMemory
) -> None:
    option = "Remove"
    modal_name = "Remove share"
    button = "Remove"

    click_menu_button_on_shares_page(selenium, browser_id)
    click_option_in_share_row_menu(selenium, browser_id, option)
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    click_modal_button(selenium, browser_id, button, modal_name)


@wt(parsers.parse('user of {browser_id} opens shares view of "{space_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def open_shares_view_of_given_space(
    selenium: SeleniumDrivers, browser_id: str, space_name: str, tmp_memory: TmpMemory
) -> None:
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
    selenium: SeleniumDrivers,
    browser_id: str,
    share_name: str,
    tmp_memory: TmpMemory,
    space_name: str,
) -> None:
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
    selenium: SeleniumDrivers,
    browser_id: str,
    browser2_id: str,
    share_name: str,
    item_name: str,
    tmp_memory: TmpMemory,
    displays: dict[str, str],
    clipboard: Clipboard,
) -> None:
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
def copy_url_of_share(
    selenium: SeleniumDrivers,
    browser_id: str,
    share_name: str,
    item_name: str,
    tmp_memory: TmpMemory,
) -> None:
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
def rename_share_from_single_view(
    selenium: SeleniumDrivers, browser_id: str, new_name: str, tmp_memory: TmpMemory
) -> None:
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
def copy_command_from_api_in_file_details_modal(
    selenium: SeleniumDrivers, browser_id: str, command: str
) -> None:
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
def open_public_data_metadata_editor(
    selenium: SeleniumDrivers, browser_id: str, metadata_type: str
) -> None:
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
def add_description_to_share_on_private_interface(
    selenium: SeleniumDrivers, browser_id: str, description: str
) -> None:
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
def fill_inputs_in_dublin_core_metadata_form(
    selenium: SeleniumDrivers, browser_id: str, config: str
) -> None:
    """
    Fill Dublin Core metadata form according to given config.
    Config format given in yaml is as follows:

        metadata field: value               ---> single value
        metadata field:
            - first value
            - second value                  ---> multiple values
    ...

    If multiple values are provided for the same metadata field,
    additional input fields are added below within the same section.

    The behavior is the same as in the function `fill_inputs_in_edm_metadata_form`,
    except that:
    - There are currently no selectable fields.
    - There is no special field like "Material".
    """
    option = "private"
    tab_name = "Expose as Public Data"

    open_tab_in_public_share(selenium, browser_id, tab_name)
    parsed_config = yaml.load(config, yaml.Loader)

    for option, value in parsed_config.items():
        option = option.lower()

        if not is_name_in_initial_form_fields(option, "dublin_core"):
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
    selenium: SeleniumDrivers, browser_id: str, config: str
) -> None:
    """
    Assert Dublin Core metadata values according to given config.
    Config format given in yaml is the same as in the function:
    fill_inputs_in_dublin_core_metadata_form.
    """
    parsed_config = yaml.load(config, yaml.Loader)
    for _, data in parsed_config.items():
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
def open_shares_file_browser(
    selenium: SeleniumDrivers, browser_id: str, tmp_memory: TmpMemory
) -> None:
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
    selenium: SeleniumDrivers,
    browser_id: str,
    browser2_id: str,
    tmp_memory: TmpMemory,
    displays: dict[str, str],
    clipboard: Clipboard,
) -> None:
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
    selenium: SeleniumDrivers, browser_id: str, config: str, numerals: dict[str, int]
) -> None:
    """
    Fill EDM metadata form according to given config.

    Config format in YAML:

            metadata field: value               ---> single value

            metadata field:
                - first value
                - second value                  ---> multiple values

            Material:
                group: material group
                value: material value

    Behaviour:
    - For fields with a single value, the existing input field is filled.

    - For non-selectable text fields with multiple values, additional
    input rows are added under the same metadata section.

    - For fields not initially visible in the form, the field is added
    first and then populated with the given value(s).

    - Some fields are of type "selectable" and require selecting a value
    from a predefined set of options (e.g. a dropdown), rather than
    typing a free-text value. These fields accept a single value.

    - The "Material" field is a special selectable field that requires
    selecting a group first and then choosing the corresponding value
    within that group.
    """
    parsed_config = yaml.load(config, yaml.Loader)

    for field_name, value in parsed_config.items():
        field_name = field_name.lower()
        if not is_name_in_initial_form_fields(field_name, "edm"):
            add_property_to_edm_form_in_shares_interface(
                browser_id, selenium, field_name
            )

        if is_metadata_field_option_selectable_edm(
            field_name
        ):  # these fields cannot have literal before them
            if field_name != "material":
                choose_option_in_edm_form_in_shares_interface(
                    browser_id, value, field_name, selenium
                )

            else:  # choosing material involves also choosing options group first
                choose_option_group_in_edm_form_in_shares_interface(
                    browser_id,
                    value["group"],
                    field_name,
                    selenium,
                )
                choose_option_in_edm_form_in_shares_interface(
                    browser_id,
                    value["value"],
                    field_name,
                    selenium,
                    requires_group_selection=True,
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
                        num_to_ordinal(i),
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
    selenium: SeleniumDrivers, browser_id: str, config: str, numerals: dict[str, int]
) -> None:
    """
    Assert EDM metadata values according to given config.
    Config format given in yaml is the same as in the function:
    fill_inputs_in_edm_metadata_form.
    """
    parsed_config = yaml.load(config, yaml.Loader)

    for field_name, value in parsed_config.items():
        field_name = field_name.lower()
        if is_metadata_field_option_selectable_edm(field_name):
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
                        num_to_ordinal(i),
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
def rename_share_on_private_interface(
    selenium: SeleniumDrivers, browser_id: str, new_name: str, tmp_memory: TmpMemory
) -> None:
    modal_name = "Rename share"
    click_menu_button_on_shares_page(selenium, browser_id)
    click_option_in_share_row_menu(selenium, browser_id, "Rename")
    wt_wait_for_modal_to_appear(selenium, browser_id, modal_name, tmp_memory)
    write_name_into_text_field_in_modal(selenium, browser_id, new_name, modal_name)
    click_modal_button(selenium, browser_id, "Rename", modal_name)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) sees that (?P<metadata_type>DataCite|OpenAIRE)"
        r" XML data contains nodes like:"
        r" (?P<data>.*?) on share's (private|public) interface"
    )
)
def assert_xml_data_in_edm_form_in_shares_interface(
    selenium: SeleniumDrivers, browser_id: str, data: str, metadata_type: str
) -> None:
    check_ace_editor_appeared(selenium, browser_id)
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
        r" (?P<metadata_type>DataCite|OpenAIRE) XML"
        r' element with "(?P<tag>.*?)" tag by changing its text to "(?P<new_text>.*?)"'
        r" in share's private interface"
    )
)
def modify_xml_data_in_edm_form_in_shares_interface(
    selenium: SeleniumDrivers,
    browser_id: str,
    metadata_type: str,
    tag: str,
    new_text: str,
) -> None:
    driver = selenium[browser_id]
    public_share(driver).modify_button.click()

    check_ace_editor_appeared(selenium, browser_id)
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
        r' (?P<metadata_type>DataCite|OpenAIRE) XML node with "(?P<tag>.*?)"'
        r' tag has "(?P<text>.*?)" value'
        r" in share's private interface"
    )
)
def assert_xml_node_value(
    selenium: SeleniumDrivers,
    browser_id: str,
    tag: str,
    text: str,
    metadata_type: str,
) -> None:
    check_ace_editor_appeared(selenium, browser_id)

    xml_data = get_xml_editor_data(selenium[browser_id])
    root = ET.fromstring(xml_data)
    tag_for_search = resolve_xml_tag_for_et_search(tag, metadata_type)
    elem = root.find(f".//{tag_for_search}")
    assert elem is not None, f"Node with tag: {tag} was not found in XML data"

    assert (
        elem.text == text
    ), f"Value of XML node: {elem.text} does not match expected: {text}"
