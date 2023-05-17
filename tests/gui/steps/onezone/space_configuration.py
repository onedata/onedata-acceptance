"""This module contains gherkin steps to run acceptance tests featuring
spaces configuration  in onezone web GUI.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import json

from tests.gui.conftest import WAIT_FRONTEND

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
               '"Advertise in Marketplace" toggle1 on space configuration page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def advertise_space_on_space_configuration_page(browser_id, selenium, oz_page,
                                                option):
    driver = selenium[browser_id]
    page = oz_page(driver)['data'].configuration_page
    getattr(page.advertise_toggle, option)()


@wt(parsers.parse('user of {browser_id} sees "{email_address}" in marketplace '
                  'contact e-mail address text field'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_contact_email_address(browser_id, selenium, oz_page, email_address):
    driver = selenium[browser_id]
    contact_email = oz_page(driver)['data'].configuration_page.contact_email
    contact_email.click()
    assert 'oneicon-checkbox-empty' in contact_email

#    'oneicon-checkbox-empty'


@wt(parsers.parse('user of browser clicks "View in Marketplace" button on '
                  'space configuration page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_on_space_configuration_page(browser_id, selenium, oz_page):
    driver = selenium[browser_id]
    page = oz_page(driver)['data'].configuration_page
    page.marketplace_link.click()


@repeat_failed(timeout=WAIT_FRONTEND)
def set_space_name_in_configuration_tab(selenium, browser_id, oz_page,
                                        space_name):
    driver = selenium[browser_id]
    page = oz_page(driver)['data'].configuration_page
    page.space_name.click()
    page.space_name.value = space_name
    page.space_name.confirm()


@repeat_failed(timeout=WAIT_FRONTEND)
def set_organization_name_in_configuration_tab(selenium, browser_id, oz_page,
                                               organization_name):
    driver = selenium[browser_id]
    page = oz_page(driver)['data'].configuration_page
    page.organization_name.click()
    page.organization_name.value = organization_name
    page.organization_name.confirm()


@repeat_failed(timeout=WAIT_FRONTEND)
def set_description_of_a_space(selenium, browser_id, oz_page, description):
    driver = selenium[browser_id]
    page = oz_page(driver)['data'].configuration_page
    page.editor_description_mode.click()
    page.description_text_area = json.dumps(description)
    page.save_button.click()
    page.preview_description_mode.click()


@repeat_failed(timeout=WAIT_FRONTEND)
def add_tag_in_space_configuration_tab(browser_id, config, selenium, oz_page, popups, tag_type, tag):
    driver = selenium[browser_id]
    page = oz_page(driver)['data'].configuration_page
    page.space_tags_editor.click()
    page.space_tags_editor.add_tag.click()

    popups(driver).general_button.click()
    popups(driver).general_button.search_bar.value == tag
    popups(driver).tags_list[tag].click()
    popups(driver).general_button.search_bar.clear()

    page.space_tags_editor.add_tag.save_button



