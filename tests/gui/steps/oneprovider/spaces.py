"""This module contains gherkin steps to run acceptance tests featuring
spaces in oneprovider web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from pytest_bdd import when, then, parsers

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.utils.utils import repeat_failed


@when(parsers.parse('user of {browser_id} selects "{space_name}" '
                    'from spaces sidebar list'))
@then(parsers.parse('user of {browser_id} selects "{space_name}" '
                    'from spaces sidebar list'))
def select_sapce_from_sidebar_list(selenium, browser_id, space_name, op_page):
    op_page(selenium[browser_id]).spaces.sidebar.spaces[space_name].click()


@when(parsers.parse('user of {browser_id} clicks on settings icon displayed '
                    'for "{space_name}" item on the spaces sidebar list'))
@then(parsers.parse('user of {browser_id} clicks on settings icon displayed '
                    'for "{space_name}" item on the spaces sidebar list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_settings_icon_for_space(selenium, browser_id, space_name, op_page):
    (op_page(selenium[browser_id])
     .spaces
     .sidebar
     .spaces[space_name]
     .settings
     .expand())


@when(parsers.parse('user of {browser_id} clicks on the "{option_name}" item '
                    'in settings dropdown for space named "{spaces_name}"'))
@then(parsers.parse('user of {browser_id} clicks on the "{option_name}" item '
                    'in settings dropdown for space named "{spaces_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_item_in_space_settings_dropdown(selenium, browser_id, option_name,
                                             space_name, op_page):
    (op_page(selenium[browser_id])
     .spaces
     .sidebar
     .spaces[space_name]
     .settings
     .options[option_name]
     .click())


@when(parsers.re(r'user of (?P<browser_id>.*) sees that "(?P<name>.*)" item '
                 r'has appeared on current (?P<caption>USERS|GROUPS) '
                 r'permissions table in Spaces tab'))
@then(parsers.re(r'user of (?P<browser_id>.*) sees that "(?P<name>.*)" item '
                 r'has appeared on current (?P<caption>USERS|GROUPS) '
                 r'permissions table in Spaces tab'))
@repeat_failed(timeout=WAIT_BACKEND, interval=1.5)
def assert_item_appeared_in_spaces_perm_table(selenium, browser_id, name,
                                              caption, op_page):
    driver = selenium[browser_id]
    items = getattr(op_page(driver).spaces.permission_table, caption.lower())
    items_names = {item.name for item in items}
    if name not in items_names:
        driver.refresh()
        raise RuntimeError('no {} named "{}" found in spaces permission table'
                           ''.format(caption, name))
