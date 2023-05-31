"""This module contains gherkin steps to run acceptance tests featuring
Space Marketplace management in onezone web GUI.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import pdb
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


def get_space_from_marketplace_list(selenium, browser_id, oz_page, space_name):
    driver = selenium[browser_id]
    page = oz_page(driver)['data'].space_marketplace_page
    return page.spaces_marketplace_list[space_name]


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_organization_name_in_space_marketplace(selenium, browser_id, oz_page,
                                                  space_name,
                                                  organization_name):

    space = get_space_from_marketplace_list(selenium, browser_id, oz_page,
                                            space_name)
    err_msg = f'Advertised space: {space_name} does not have:' \
              f'{organization_name} displayed'

    assert organization_name in space.organization_name, err_msg


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_tags_in_space_marketplace(selenium, browser_id, oz_page, space_name,
                                     tags):
    space = get_space_from_marketplace_list(selenium, browser_id, oz_page,
                                            space_name)
    for tag in tags:
        assert tag in space.tags_list, f'Advertised space: {space_name} ' \
                                        f'does not have tag: {tag}'


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_creation_time_in_space_marketplace(selenium, browser_id, oz_page,
                                              space_name, given_date):
    if given_date == "current":
        today = date.today()

        day = str(today.day)
        month = today.strftime('%B')[0:3]
        year = str(today.year)
        given_date = day + " " + month + " " + year

    space = get_space_from_marketplace_list(selenium, browser_id, oz_page,
                                            space_name)
    err_msg = f'Advertised space: {space_name} does not have ' \
              f'right creation time displayed'

    assert given_date in space.creation_time, err_msg


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_support_in_space_marketplace(selenium, browser_id, oz_page,
                                        space_name, support):
    space = get_space_from_marketplace_list(selenium, browser_id, oz_page,
                                            space_name)
    for provider in support:
        assert provider in space.space_support, \
            f'Advertised space: {space_name} does not have ' \
            f'provider: {provider} as support'


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_description_in_space_marketplace(selenium, browser_id, oz_page,
                                            space_name, description):
    space = get_space_from_marketplace_list(selenium, browser_id, oz_page,
                                            space_name)
    err_msg = f'Advertised space: {space_name} does not ' \
              f'have right description displayed'

    assert description in space.description, err_msg
