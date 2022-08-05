"""This module contains gherkin steps to run acceptance tests featuring
private shares interface in oneprovider web GUI.
"""
__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import wt, parsers

from tests.gui.conftest import WAIT_FRONTEND
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} chooses "{option}" in dropdown menu '
                  'for handle service on share\'s private interface'))
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_option_for_publish_as_open_data(browser_id, option, popups,
                                           selenium):
    driver = selenium[browser_id]
    popups(driver).handle_service.options[option].click()


@wt(parsers.parse('user of {browser_id} writes "{text}" into last {which_input}'
                  ' input text field in "Dublin Core Metadata" form on '
                  'share\'s private interface'))
@repeat_failed(timeout=WAIT_FRONTEND)
def write_input_in_form_in_shares_interface(browser_id, text, which_input,
                                            selenium, private_share):
    driver = selenium[browser_id]
    private_share(driver).dublin_core_metadata_form.write_to_last_input(
        text, which_input)


@wt(parsers.re('user of (?P<browser_id>.*?) clicks "(?P<button>.*?)" button '
               'in "Dublin Core Metadata" form on share\'s private interface'))
@repeat_failed(timeout=WAIT_FRONTEND)
def clicks_button_in_form_in_shares_interface(browser_id, button, selenium,
                                              private_share):
    driver = selenium[browser_id]
    private_share(driver).dublin_core_metadata_form.click_add_button(button)


@wt(parsers.re('user of (?P<browser_id>.*?) clicks "(?P<button>.*?)" button in'
               ' "Description" form on share\'s private interface'))
def click_button_in_description_form(browser_id, selenium, button,
                                     private_share):
    driver = selenium[browser_id]
    getattr(private_share(driver).description_form, transform(button))()


@wt(parsers.parse('user of {browser_id} sees that link on share\'s private '
                  'interface is "{link}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_link_on_shares_interface(browser_id, link, selenium, private_share):
    driver = selenium[browser_id]
    err_msg = f'Link on share\'s private interface is not "{link}"'
    assert private_share(driver).link_name == link, err_msg


@wt(parsers.parse('user of {browser_id} types "{text}" into {where} in '
                  '"Description" form on share\'s private interface'))
def write_description_in_description_form(browser_id, text, where, selenium,
                                          private_share):
    driver = selenium[browser_id]
    setattr(private_share(driver).description_form, transform(where), text)

