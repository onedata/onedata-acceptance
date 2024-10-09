"""This module contains gherkin steps to run acceptance tests featuring
groups in oneprovider web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from tests.utils.bdd_utils import wt, parsers

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.utils.utils import repeat_failed


def _is_group_present_in_sidebar(driver, op_container, group_name):
    groups = {group.name for group
              in op_container(driver).groups.sidebar.groups}
    return group_name in groups


@wt(parsers.parse('user of {browser_id} sees that group named '
                  '"{name}" has appeared in the groups list'))
@repeat_failed(timeout=2*WAIT_BACKEND, interval=1.5)
def is_present_on_groups_list(selenium, browser_id, name, op_container):
    driver = selenium[browser_id]
    if not _is_group_present_in_sidebar(driver, op_container, name):
        driver.refresh()
        raise RuntimeError(f'no group named "{name}" found in groups sidebar')


@wt(parsers.parse('user of {browser_id} clicks on settings icon displayed '
                  'for "{group_name}" item on the groups sidebar list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_settings_icon_for_group(selenium, browser_id, group_name,
                                  op_container):
    (op_container(selenium[browser_id])
     .groups
     .sidebar
     .groups[group_name]
     .settings
     .expand())


@wt(parsers.parse('user of {browser_id} clicks on the "{option_name}" item '
                  'in settings dropdown for group named "{group_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_item_in_group_settings_dropdown(selenium, browser_id, option_name,
                                             group_name, op_container):
    (op_container(selenium[browser_id])
     .groups
     .sidebar
     .groups[group_name]
     .settings
     .options[option_name]
     .click())


@wt(parsers.re(r'user of (?P<browser_id>.*) sees that "(?P<name>.*)" item '
               r'has appeared on current (?P<caption>USERS|GROUPS) '
               r'permissions table in Groups tab'))
@repeat_failed(timeout=WAIT_BACKEND, interval=1.5)
def assert_item_appeared_in_groups_perm_table(selenium, browser_id, name,
                                              caption, op_container):
    driver = selenium[browser_id]
    items = getattr(op_container(driver).groups.permission_table, caption.lower())
    items_names = {item.name for item in items}
    if name not in items_names:
        driver.refresh()
        raise RuntimeError(
            f'no {caption} named "{name}" found in groups permission table')
