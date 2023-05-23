"""This module contains gherkin steps to run acceptance tests featuring
Space Marketplace management in onezone web GUI.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from datetime import date

from tests.gui.conftest import WAIT_FRONTEND
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed


@wt(parsers.re('user of (?P<browser_id>.*) clicks on "Advertise your space" '
               'button in Space Marketplace subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_in_marketplace_subpage(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['data'].space_marketplace_page.advertise_space_button()


@wt(parsers.re('user of (?P<browser_id>.*) sees that "(?P<space_name>.*)" '
               'space is advertised in the marketplace in space sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_marketplace_icon_in_space_sidebar(selenium, browser_id, oz_page,
                                             space_name):
    driver = selenium[browser_id]
    err_msg = "Space: {space_name} does not have marketplace indicator visible"

    assert oz_page(driver)['data'].elements_list[space_name].advertised_icon, \
        err_msg


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_organization_name_in_space_marketplace(selenium, browser_id, oz_page,
                                                  space_name,
                                                  organization_name):
    driver = selenium[browser_id]
    page = oz_page(driver)['data'].space_marketplace_page
    err_msg = "Advertised space: {space_name} does not have:{organization_name} displayed"

    assert organization_name in page.marketplaces_list[space_name].organization_name, err_msg


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_tags_in_space_marketplace(selenium, browser_id, oz_page, space_name,
                                     tags):
    driver = selenium[browser_id]
    page = oz_page(driver)['data'].space_marketplace_page
    tags_list = page.marketplaces_list[space_name].tags_list

    for tag in tags:
        assert tag in tags_list, f'Advertised space: {space_name} does not have tag: {tag}'


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_creation_time_in_space_marketplace(selenium, browser_id, oz_page,
                                              space_name, given_date):
    driver = selenium[browser_id]
    if given_date == "current":
        today = date.today()

        day = str(today.day)
        month = today.strftime('%B')
        year = str(today.year)
        given_date = day + " " + month + " " + year

    page = oz_page(driver)['data'].space_marketplace_page
    err_msg = "Advertised space: {space_name} does not have right creation time displayed"

    assert given_date in page.marketplaces_list[space_name].creation_time, err_msg


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_support_in_space_marketplace(selenium, browser_id, oz_page, space_name, support):
    driver = selenium[browser_id]
    page = oz_page(driver)['data'].space_marketplace_page
    space_support = page.marketplaces_list[space_name].tags_list

    for provider in support:
        pdb.set_trace()
        assert provider in space_support, f'Advertised space: {space_name} does not have tag: {provider} as support'


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_description_in_space_marketplace(selenium, browser_id, oz_page,
                                            space_name, description, modals):
    driver = selenium[browser_id]
    page = oz_page(driver)['data'].space_marketplace_page
    marketplace = page.marketplaces_list[space_name]
    err_msg = "Advertised space: {space_name} does not have right description displayed"

    assert description in marketplace.description, err_msg
