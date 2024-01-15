"""Steps used for details modal handling in various GUI testing scenarios
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from datetime import datetime

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.steps.modals.modal import check_modal_name
from tests.gui.steps.oneprovider.browser import (
    click_menu_for_elem_in_browser, click_option_in_data_row_menu_in_browser)
from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} sees that {which_title} is "{title}" '
                  'in modal "{modal}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_chart_title_in_details_modal(selenium, browser_id, modals, title,
                                        which_title, modal):
    modal = check_modal_name(modal)
    modal = getattr(modals(selenium[browser_id]), modal).size_statistics
    if which_title == 'charts title':
        charts_title = modal.charts_title
    elif which_title == 'count chart title':
        charts_title = modal.chart[0].title
    else:
        charts_title = modal.chart[1].title
    assert charts_title == title, (f'Charts title is {charts_title} not '
                                   f'{title} as expected')


@wt(parsers.parse('user of {browser_id} clicks on chart in modal "{modal}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_chart_in_modal(browser_id, modals, selenium, modal):
    modal = check_modal_name(modal)
    getattr(modals(selenium[browser_id]),
            modal).size_statistics.click_on_chart()


@wt(parsers.parse('user of {browser_id} sees that "{element}" item displayed '
                  'in "{modal}" modal is not active'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_button_in_modal_not_active(browser_id, modal, element, modals,
                                      selenium):
    driver = selenium[browser_id]
    modal = getattr(modals(driver), check_modal_name(modal))
    err_msg = f'"{element}" button is in active state'
    assert not modal.is_element_active(transform(element)), err_msg


@wt(parsers.parse('user of {browser_id} sees that tooltip with size statistics'
                  ' header has date format in modal "{modal}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_tooltip_on_chart_in_modal(browser_id, selenium, popups):
    driver = selenium[browser_id]
    header = popups(driver).chart_statistics.header
    try:
        datetime.strptime(header, '%H:%M %d/%m/%Y')
    except ValueError:
        raise Exception('Header: {header} of tooltip does not have date format')


@wt(parsers.re('user of (?P<browser_id>.*) clicks on "(?P<tab_name>.*)" '
               'navigation tab in "(?P<modal>.*)" modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_navigation_tab_in_modal(selenium, browser_id, tab_name, modals,
                                     modal):
    modal = getattr(modals(selenium[browser_id]), check_modal_name(modal))
    tab = modal.navigation[tab_name]
    tab.web_elem.click()


@wt(parsers.re('user of (?P<browser_id>.*) clicks on "(?P<tab_name>.*)" '
               'navigation tab in (?P<modal>.*) panel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_navigation_tab_in_panel(selenium, browser_id, tab_name, modals,
                                     modal):
    modal = getattr(modals(selenium[browser_id]).details_modal,
                    check_modal_name(modal))
    tab = modal.navigation[tab_name]
    tab.web_elem.click()


@wt(parsers.parse('user of {browser_id} sees that "{modal_name}" modal is '
                  'opened on "{tab}" tab'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_tab_in_modal(selenium, browser_id, tab, modals, modal_name):
    active_tab = getattr(modals(selenium[browser_id]),
                         check_modal_name(transform(modal_name))).active_tab
    err_msg = (f'Expected tab: {tab} does not match actual active tab: '
               f'{active_tab} on modal {modal_name}')
    assert tab in active_tab, err_msg


@wt(parsers.parse('user of {browser_id} sees that "Permissions" panel is opened'
                  ' on "POSIX" tab in "{modal_name}" modal'))
def assert_posix_tab_in_panel(selenium, browser_id, modals, modal_name):
    elem_name = 'posix_permission_edition'
    posix_hidden = getattr(modals(selenium[browser_id]),
                           check_modal_name(transform(modal_name))
                           ).edit_permissions.is_hidden(elem_name)
    assert not posix_hidden, (f'sees that "Permissions" panel is not'
                              f' opened on "POSIX" tab')


@wt(parsers.parse('user of {browser_id} clicks on "{context_menu_item}" in '
                  'context menu for "{item_name}"'))
@wt(parsers.parse('user of {browser_id} clicks on "{context_menu_item}" in '
                  'context menu for {item_name} in file browser'))
def click_on_context_menu_item(selenium, browser_id, popups, item_name,
                               tmp_memory, context_menu_item):
    if item_name[0] == "\"":
        item_name = item_name.replace("\"", "")
    click_menu_for_elem_in_browser(browser_id, item_name, tmp_memory)
    click_option_in_data_row_menu_in_browser(selenium, browser_id,
                                             context_menu_item, popups)


