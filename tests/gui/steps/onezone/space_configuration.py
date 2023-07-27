"""This module contains gherkin steps to run acceptance tests featuring
spaces configuration in onezone web GUI.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import json

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.utils.generic import transform

from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} sees that "Advertise in Marketplace" '
                  'toggle is {checked} on space configuration page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_advertise_in_marketplace_toggle(selenium, browser_id, oz_page,
                                           checked):
    driver = selenium[browser_id]
    page = oz_page(driver)['data'].configuration_page

    if 'not' in checked:
        assert page.advertise_toggle.is_unchecked(), 'Space is advertised in ' \
                                                     'marketplace'
    else:
        assert page.advertise_toggle.is_checked(), 'Space is not advertised ' \
                                                   'in marketplace'


@wt(parsers.re('user of (?P<browser_id>.*) (?P<option>check|uncheck)s '
               '"Advertise in Marketplace" toggle on space configuration page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def advertise_space_on_space_configuration_page(browser_id, selenium, oz_page,
                                                option):
    driver = selenium[browser_id]
    page = oz_page(driver)['data'].configuration_page
    getattr(page.advertise_toggle, option)()


@wt(parsers.parse('user of {browser_id} clicks "View in Marketplace" link on '
                  'space configuration page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_on_space_configuration_page(browser_id, selenium, oz_page):
    driver = selenium[browser_id]
    page = oz_page(driver)['data'].configuration_page
    page.marketplace_link.click()


@wt(parsers.parse('user of {browser_id} sees "{email_address}" in marketplace '
                  'contact e-mail address text field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_contact_email_address(browser_id, selenium, oz_page, email_address):
    driver = selenium[browser_id]
    contact_email = oz_page(driver)['data'].configuration_page.contact_email
    contact_email.click()
    err_msg = f'Email address {contact_email.text} displayed on space ' \
              f'configuration page, does not match expected {email_address}'

    assert email_address in contact_email.text, err_msg


@repeat_failed(timeout=WAIT_FRONTEND)
def set_space_data_in_configuration_tab(selenium, browser_id, oz_page,
                                        data_type, data_name):
    driver = selenium[browser_id]
    data_type = transform(data_type)
    page = getattr(oz_page(driver)['data'].configuration_page, data_type)
    page.click()
    page.value = data_name
    page.confirm()


@wt(parsers.parse('user of {browser_id} sets organization description '
                  '"{description}" in space configuration subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def set_description_of_a_space(selenium, browser_id, oz_page, description):
    driver = selenium[browser_id]
    page = oz_page(driver)['data'].configuration_page
    page.editor_description_mode.click()
    page.description_text_area = json.dumps(description)
    page.save_button.click()
    page.preview_description_mode.click()


@repeat_failed(timeout=WAIT_FRONTEND)
def add_tags_in_space_configuration_tab(selenium, browser_id,  oz_page, popups,
                                        tag_type, tags):
    driver = selenium[browser_id]
    page = oz_page(driver)['data'].configuration_page
    page.space_tags_editor.click()
    page.space_tags_editor.add_tag.click()
    getattr(popups(driver).spaces_tags, tag_type).click()

    for tag in tags:
        popups(driver).spaces_tags.search_bar = tag
        popups(driver).spaces_tags.tags_list[tag].click()

    page.space_tags_editor.save_button.click()



