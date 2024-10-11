"""This module contains gherkin steps to run acceptance tests featuring
spaces configuration in onezone web GUI.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)


from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.parse(
        'user of {browser_id} sees that "Advertise in Marketplace" '
        "toggle is {checked} on space configuration page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_advertise_in_marketplace_toggle(
    selenium, browser_id, oz_page, checked
):
    driver = selenium[browser_id]
    page = oz_page(driver)["data"].configuration_page

    if "not" in checked:
        assert (
            page.advertise_toggle.is_unchecked()
        ), "Space is advertised in marketplace"
    else:
        assert (
            page.advertise_toggle.is_checked()
        ), "Space is not advertised in marketplace"


@wt(
    parsers.re(
        "user of (?P<browser_id>.*) (?P<option>check|uncheck)s "
        '"Advertise in Marketplace" toggle on space configuration page'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def advertise_space_on_space_configuration_page(
    browser_id, selenium, oz_page, option
):
    driver = selenium[browser_id]
    page = oz_page(driver)["data"].configuration_page
    getattr(page.advertise_toggle, option)()


@wt(
    parsers.parse(
        'user of {browser_id} clicks "View in Marketplace" link on '
        "space configuration page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_on_space_configuration_page(browser_id, selenium, oz_page):
    driver = selenium[browser_id]
    page = oz_page(driver)["data"].configuration_page
    page.marketplace_link.click()


@wt(
    parsers.parse(
        'user of {browser_id} sees "{email_address}" in marketplace '
        "contact e-mail address text field"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_contact_email_address(browser_id, selenium, oz_page, email_address):
    driver = selenium[browser_id]
    contact_email = oz_page(driver)["data"].configuration_page.contact_email
    err_msg = (
        f"Email address {contact_email.name} displayed on space "
        f"configuration page, does not match expected {email_address}"
    )

    assert email_address in contact_email.name, err_msg


@repeat_failed(timeout=WAIT_FRONTEND)
def set_space_data_in_configuration_tab(
    selenium, browser_id, oz_page, data_type, data_name, with_save=True
):
    driver = selenium[browser_id]
    data_type = transform(data_type)
    page = getattr(oz_page(driver)["data"].configuration_page, data_type)
    page.click()
    page.value = data_name
    if with_save:
        page.confirm()


@wt(
    parsers.parse(
        "user of {browser_id} sets organization description "
        '"{description}" in space configuration subpage'
    )
)
def set_description_of_a_space_(selenium, browser_id, oz_page, description):
    set_description_of_a_space(selenium, browser_id, oz_page, description)


@repeat_failed(timeout=WAIT_FRONTEND)
def set_description_of_a_space(
    selenium, browser_id, oz_page, description, with_save=True
):
    driver = selenium[browser_id]
    page = oz_page(driver)["data"].configuration_page
    page.editor_description_mode.click()
    page.description_text_area = description
    if with_save:
        page.save_button.click()
        page.preview_description_mode.click()


@repeat_failed(timeout=WAIT_FRONTEND)
def add_tags_in_space_configuration_tab(
    selenium, browser_id, oz_page, popups, tag_type, tags, with_save=True
):
    driver = selenium[browser_id]
    page = oz_page(driver)["data"].configuration_page
    page.space_tags_editor.click()
    page.space_tags_editor.add_tag.click()
    getattr(popups(driver).spaces_tags, tag_type).click()

    for tag in tags:
        popups(driver).spaces_tags.search_bar = tag
        popups(driver).spaces_tags.tags_list[tag].click()

    if with_save:
        page.space_tags_editor.save_button.click()


@wt(
    parsers.parse(
        'user of {browser_id} sees "{label_info}" header label'
        " in configuration space"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def check_header_info_in_space_configuration(
    selenium, browser_id, label_info, oz_page
):
    driver = selenium[browser_id]
    header_label_message = oz_page(driver)[
        "data"
    ].configuration_page.header_label_warning
    err_msg = (
        f"expected {label_info} header label instead of {header_label_message}"
    )
    assert header_label_message == str(label_info), err_msg


@wt(
    parsers.parse(
        'user of {browser_id} sees "{message_type}" message after '
        'hovering over "{toggle_name}" toggle in '
        "configuration space"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def check_message_after_hovering_over_toggle(
    selenium, browser_id, message_type, toggle_name, oz_page, popups
):
    messages_dict = {
        "Insufficient privileges": (
            "Insufficient privileges "
            '(requires "modify space" and '
            '"manage in Marketplace" '
            "privileges in this space)."
        )
    }
    driver = selenium[browser_id]
    page = oz_page(driver)["data"].configuration_page
    page.move_to_toggle(driver)
    toggle_info = popups(driver).toggle_label
    expected_message = messages_dict[message_type]
    err_msg = (
        f"expected {expected_message} info to be visible instead of "
        f"{toggle_info} after hovering over toggle {toggle_name}"
    )
    assert toggle_info == messages_dict[message_type], err_msg


@wt(
    parsers.parse(
        "user of {browser_id} changes organization name for "
        '"{org_name}" in space configuration subpage'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def change_org_name_in_space_conf(selenium, browser_id, oz_page, org_name):
    driver = selenium[browser_id]
    page = oz_page(driver)["data"].configuration_page
    page.organization_name.click()
    page.organization_name.value = str(org_name)
    page.organization_name.confirm.click()
