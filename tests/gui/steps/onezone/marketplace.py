"""This module contains gherkin steps to run acceptance tests featuring
Space Marketplace management in onezone web GUI.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2023 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from tests.gui.conftest import WAIT_FRONTEND
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed


@wt(parsers.re('user of (?P<browser_id>.*) clicks on "Advertise your space" '
               'button in Space Marketplace subpage'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_in_marketplace_subpage(selenium, browser_id,  oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['data'].space_marketplace_page.advertise_space_button()


@wt(parsers.re('user of (?P<browser_id>.*) sees that "(?P<space_name>.*)" '
               'space is advertised in the marketplace in space sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_marketplace_icon_in_space_sidebar(selenium, browser_id,  oz_page,
                                             space_name):
    driver = selenium[browser_id]
    err_msg = "Space: {space_name} does not have marketplace indicator visible"
    assert oz_page(driver)['data'].elements_list[space_name].advertised_icon, \
        err_msg

