"""This module contains gherkin steps to run acceptance tests featuring
private shares interface in oneprovider web GUI.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from typing import Any

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
)

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.utils import Popups
from tests.gui.utils import PrivateShareView as private_share
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import parsers, wt
from tests.utils.utils import repeat_failed
from tests.conftest import SeleniumDrivers


@wt(
    parsers.parse(
        'user of {browser_id} chooses "{option}" in dropdown menu '
        "for handle service on share's private interface"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_option_for_publish_handle_service_as_open_data(
    browser_id: Any, option: Any, selenium: SeleniumDrivers
) -> Any:
    driver = selenium[browser_id]
    Popups(driver).handle_service.options[option].click()


@wt(
    parsers.parse(
        'user of {browser_id} chooses "{option}" in dropdown menu '
        "for metadata type on share's private interface"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_option_for_publish_metadata_as_open_data(
    browser_id: Any, option: Any, selenium: SeleniumDrivers
) -> Any:
    driver = selenium[browser_id]
    Popups(driver).metadata_type.options[option].click()


@wt(
    parsers.parse(
        'user of {browser_id} writes "{text}" into last {which_input}'
        ' input text field in "Dublin Core Metadata" form on '
        "share's private interface"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def write_input_in_form_in_shares_interface(
    browser_id: Any, text: Any, which_input: Any, selenium: SeleniumDrivers
) -> Any:
    driver = selenium[browser_id]
    private_share(driver).dublin_core_metadata_form.write_to_last_input(
        driver, text, which_input
    )


@wt(
    parsers.re(
        'user of (?P<browser_id>.*?) clicks "(?P<button>.*?)" button '
        'in "Dublin Core Metadata" form on share\'s private interface'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_in_form_in_shares_interface(
    browser_id: Any, button: Any, selenium: SeleniumDrivers
) -> Any:
    driver = selenium[browser_id]
    private_share(driver).dublin_core_metadata_form.click_add_button(driver, button)


@wt(
    parsers.re(
        'user of (?P<browser_id>.*?) clicks "(?P<button>.*?)" button in'
        ' "Description" form on share\'s private interface'
    )
)
def click_button_in_description_form(
    browser_id: Any, selenium: SeleniumDrivers, button: Any
) -> Any:
    driver = selenium[browser_id]
    getattr(private_share(driver).description_form, transform(button))()


@wt(
    parsers.parse(
        'user of {browser_id} sees that link on share\'s private interface is "{link}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_link_on_shares_interface(browser_id: Any, link: Any, selenium: SeleniumDrivers) -> Any:
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
    browser_id: Any, text: Any, where: Any, selenium: SeleniumDrivers
) -> Any:
    driver = selenium[browser_id]
    setattr(private_share(driver).description_form, transform(where), text)


@wt(
    parsers.parse(
        'user of {browser_id} sees that share in private view is named "{share_name}"'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND, interval=0.5)
def assert_private_share_named(selenium: SeleniumDrivers, browser_id: Any, share_name: Any) -> Any:
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
        " section text field in EDM form on "
        "share's private interface"
    )
)
def write_input_in_edm_form_in_shares_interface(
    browser_id: Any, text: Any, which_input: Any, selenium: SeleniumDrivers, numerals: Any
) -> Any:
    numeral = "first"
    write_to_nth_input_in_edm_form_in_shares_interface(
        browser_id, text, which_input, selenium, numeral, numerals
    )


@wt(
    parsers.parse(
        'user of {browser_id} writes "{text}" to {numeral} "{which_input}"'
        " section text field in EDM form on "
        "share's private interface"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def write_to_nth_input_in_edm_form_in_shares_interface(
    browser_id: Any,
    text: Any,
    which_input: Any,
    selenium: SeleniumDrivers,
    numeral: Any,
    numerals: Any,
) -> Any:
    driver = selenium[browser_id]
    form = private_share(driver).edm_metadata_form
    idx = numerals[numeral]
    for item in form.items:
        if item.name == "":
            driver.execute_script("arguments[0].scrollIntoView();", item.web_elem)
        if item.name.lower() == which_input.lower():
            if idx == 0:
                item_input = item.input
                if not item_input.is_displayed():
                    driver.execute_script("arguments[0].scrollIntoView();", item_input)
                item_input.clear()
                item_input.send_keys(text)
                return
            idx -= 1
    raise AssertionError(f"item {which_input} not found")


@wt(
    parsers.parse(
        'user of {browser_id} chooses "{option}" in "{section_name}"'
        " section in EDM form on "
        "share's private interface"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_option_in_edm_form_in_shares_interface(
    browser_id: Any,
    option: Any,
    section_name: Any,
    selenium: SeleniumDrivers,
    is_group: Any = False,
    requires_group_selection: Any = False,
) -> Any:
    driver = selenium[browser_id]
    form = private_share(driver).edm_metadata_form

    if (
        requires_group_selection and not is_group
    ):  # When group selection is enabled but we are selecting a concrete item
        # (not the group itself), it can be chosen directly without expanding
        # the dropdown again.
        Popups(driver).power_select.choose_item(option, require_full_match=False)
        return

    for item in form.items:
        if item.name == "":
            driver.execute_script("arguments[0].scrollIntoView();", item.web_elem)
        if item.name.lower() == section_name.lower():
            _open_section_dropdown_and_choose(driver, item, option, is_group)
            # intentionally return after handling the matching item
            return

    raise AssertionError(f"item {section_name} not found")


def _open_section_dropdown_and_choose(
    driver: Any, item: Any, option: Any, is_group: Any
) -> Any:
    item_dropdown = item.dropdown
    try:
        item_dropdown.click()
    except (ElementClickInterceptedException, ElementNotInteractableException):
        # fallback: scroll to center and try again
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", item_dropdown
        )
        item_dropdown.click()

    if is_group:
        Popups(driver).power_select.choose_group(option, require_full_match=False)
    else:
        Popups(driver).power_select.choose_item(option, require_full_match=False)


@wt(
    'user of {browser_id} chooses "{option}" item group in "{section_name}"'
    " section in EDM form on "
    "share's private interface"
)
def choose_option_group_in_edm_form_in_shares_interface(
    browser_id: Any, option: Any, section_name: Any, selenium: SeleniumDrivers
) -> Any:
    choose_option_in_edm_form_in_shares_interface(
        browser_id,
        option,
        section_name,
        selenium,
        is_group=True,
        requires_group_selection=True,
    )


@wt(
    parsers.parse(
        'user of {browser_id} sees that "{section_name}" section has value'
        ' "{expected_value}" in EDM form on share\'s private interface'
    )
)
def assert_val_edm_form_in_shares_interface(
    browser_id: Any,
    expected_value: Any,
    section_name: Any,
    selenium: SeleniumDrivers,
    numerals: Any,
) -> Any:
    numeral = "first"
    assert_nth_val_edm_form_in_shares_interface(
        browser_id, expected_value, section_name, selenium, numeral, numerals
    )


@wt(
    parsers.parse(
        'user of {browser_id} sees that {numeral} "{section_name}" section has value'
        ' "{expected_value}" in EDM form on share\'s private interface'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_nth_val_edm_form_in_shares_interface(
    browser_id: Any,
    expected_value: Any,
    section_name: Any,
    selenium: SeleniumDrivers,
    numeral: Any,
    numerals: Any,
) -> Any:
    driver = selenium[browser_id]
    items = private_share(driver).edm_public_view.items
    idx = numerals[numeral]
    for item in items:
        if item.name == "":
            driver.execute_script("arguments[0].scrollIntoView();", item.web_elem)
        if item.name.lower() == section_name.lower():
            if idx == 0:
                item_value = item.value.text
                err_msg = (
                    f"Expected value: {expected_value} but got {item_value} for item"
                    f" {section_name}"
                )
                assert item_value == expected_value, err_msg
                return
            idx -= 1
    raise AssertionError(f"item {section_name} not found")


@wt(
    parsers.parse(
        'user of {browser_id} adds property "{item_name}" in'
        " section in EDM form on "
        "share's private interface"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def add_property_to_edm_form_in_shares_interface(
    browser_id: Any, selenium: SeleniumDrivers, item_name: Any
) -> Any:
    driver = selenium[browser_id]
    form = private_share(driver).edm_metadata_form
    driver.execute_script(
        "arguments[0].scrollIntoView({block: 'center'});", form.add_property.web_elem
    )
    form.add_property.click()
    Popups(driver).options_selector.choose_option(item_name.lower())


@wt(
    parsers.parse(
        'user of {browser_id} sees warning alert message "{mess_text}" in '
        "share's private interface"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_warning_message_in_shares_page(
    browser_id: Any, selenium: SeleniumDrivers, mess_text: Any
) -> Any:
    driver = selenium[browser_id]
    warning = private_share(driver).alert_warning
    err_msg = f"Expected alert message: {mess_text} but got: {warning.text}"
    assert mess_text in warning.text, err_msg


@wt(
    parsers.parse(
        "user of {browser_id} sees there is no warning alert in "
        "share's private interface"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_no_warning_message_in_shares_page(browser_id: Any, selenium: SeleniumDrivers) -> Any:
    driver = selenium[browser_id]
    try:
        warning = private_share(driver).alert_warning
        raise AssertionError(f"There is visible warning alert: {warning.text}")
    except RuntimeError:
        pass


def add_metadata_field_in_dublin_core_form(driver: Any, field_name: Any) -> Any:
    share = private_share(driver)
    share.dublin_core_metadata_form.add_more_elements.click()
    share.dropdown.options[field_name.capitalize()].click()

    share.dublin_core_metadata_form.click_on_background()
