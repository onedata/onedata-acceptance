"""This module contains gherkin steps to run acceptance tests featuring
private shares interface in oneprovider web GUI.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from selenium.common.exceptions import ElementClickInterceptedException

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.utils import Popups
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.parse(
        'user of {browser_id} chooses "{option}" in dropdown menu '
        "for handle service on share's private interface"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_option_for_publish_handle_service_as_open_data(
    browser_id, option, popups, selenium
):
    driver = selenium[browser_id]
    popups(driver).handle_service.options[option].click()


@wt(
    parsers.parse(
        'user of {browser_id} chooses "{option}" in dropdown menu '
        "for metadata type on share's private interface"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_option_for_publish_metadata_as_open_data(
    browser_id, option, popups, selenium
):
    driver = selenium[browser_id]
    popups(driver).metadata_type.options[option].click()


@wt(
    parsers.parse(
        'user of {browser_id} writes "{text}" into last {which_input}'
        ' input text field in "Dublin Core Metadata" form on '
        "share's private interface"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def write_input_in_form_in_shares_interface(
    browser_id, text, which_input, selenium, private_share
):
    driver = selenium[browser_id]
    private_share(driver).dublin_core_metadata_form.write_to_last_input(
        text, which_input
    )


@wt(
    parsers.re(
        'user of (?P<browser_id>.*?) clicks "(?P<button>.*?)" button '
        'in "Dublin Core Metadata" form on share\'s private interface'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def clicks_button_in_form_in_shares_interface(
    browser_id, button, selenium, private_share
):
    driver = selenium[browser_id]
    private_share(driver).dublin_core_metadata_form.click_add_button(button)


@wt(
    parsers.re(
        'user of (?P<browser_id>.*?) clicks "(?P<button>.*?)" button in'
        ' "Description" form on share\'s private interface'
    )
)
def click_button_in_description_form(browser_id, selenium, button, private_share):
    driver = selenium[browser_id]
    getattr(private_share(driver).description_form, transform(button))()


@wt(
    parsers.parse(
        'user of {browser_id} sees that link on share\'s private interface is "{link}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_link_on_shares_interface(browser_id, link, selenium, private_share):
    driver = selenium[browser_id]
    err_msg = f'Link on share\'s private interface is not "{link}"'
    assert private_share(driver).link_name == link, err_msg


@wt(
    parsers.parse(
        'user of {browser_id} types "{text}" into {where} in '
        '"Description" form on share\'s private interface'
    )
)
def write_description_in_description_form(
    browser_id, text, where, selenium, private_share
):
    driver = selenium[browser_id]
    setattr(private_share(driver).description_form, transform(where), text)


@wt(
    parsers.parse(
        'user of {browser_id} sees that share in private view is named "{share_name}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND, interval=0.5)
def assert_private_share_named(selenium, browser_id, share_name, private_share):
    driver = selenium[browser_id]
    # because label with share name lies beyond iframe we need to change
    # to default content
    driver.switch_to.default_content()
    displayed_name = private_share(driver).share_name
    assert displayed_name == share_name, (
        "displayed private share name "
        f'is "{displayed_name}" instead of '
        f'expected "{share_name}"'
    )


@wt(
    parsers.parse(
        'user of {browser_id} writes "{text}" to "{which_input}"'
        ' section text field in "EDM" form on '
        "share's private interface"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def write_input_in_edm_form_in_shares_interface(
    browser_id, text, which_input, selenium, private_share
):
    driver = selenium[browser_id]
    form = private_share(driver).edm_metadata_form

    for item in form.items:
        if item.name == "":
            driver.execute_script("arguments[0].scrollIntoView();", item.web_elem)
        if item.name == which_input:
            item_input = item.input
            if not item_input.is_displayed():
                driver.execute_script("arguments[0].scrollIntoView();", item_input)
            item_input.clear()
            item_input.send_keys(text)
            return
    raise AssertionError(f"item {which_input} not found")


@wt(
    parsers.parse(
        'user of {browser_id} chooses "{option}" in "{section_name}"'
        ' section in "EDM" form on '
        "share's private interface"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_option_in_edm_form_in_shares_interface(
    browser_id, option, section_name, selenium, private_share
):
    driver = selenium[browser_id]
    form = private_share(driver).edm_metadata_form

    for item in form.items:
        if item.name == "":
            driver.execute_script("arguments[0].scrollIntoView();", item.web_elem)
        if item.name == section_name:
            item_dropdown = item.dropdown
            try:
                item_dropdown.click()
            except ElementClickInterceptedException:
                driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", item_dropdown
                )
                item_dropdown.click()
            Popups(driver).power_select.choose_item_including_name(option)
            return
    raise AssertionError(f"item {section_name} not found")


# def get_val_edm_form_in_shares_interface(
#     browser_id, text, which_input, selenium, private_share
# ):
#     driver = selenium[browser_id]
#     form = private_share(driver).edm_metadata_form
#     item = form.items[which_input]
#     val = item.get_attribute("value")
