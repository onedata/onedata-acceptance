"""This module contains gherkin steps to run acceptance tests featuring groups
management in onezone web GUI
"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from pytest_bdd import parsers, when, then

from tests.gui.steps.common import *

@when(parsers.parse('user of {browser_id} clicks on the join button in "{panel}" Onezone panel'))
@then(parsers.parse('user of {browser_id} clicks on the join button in "{panel}" Onezone panel'))
def click_join_in_panel(selenium, browser_id, panel, oz_page):
    oz_page(selenium[browser_id])[panel].join_group.click()
