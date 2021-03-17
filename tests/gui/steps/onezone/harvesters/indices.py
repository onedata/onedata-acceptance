"""This module contains gherkin steps to run acceptance tests featuring
harvester indices management in onezone web GUI.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed


@wt(parsers.parse('user of {browser_id} clicks "{text}" in '
                  'harvester indices page menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_member_menu_option_in_harvester_indices_page(selenium, browser_id,
                                                          text, oz_page,
                                                          popups):
    driver = selenium[browser_id]
    oz_page(driver)['discovery'].indices_page.menu_button.click()
    popups(driver).menu_popup_with_text.menu[text]()


@wt(parsers.parse('user of {browser_id} types "{index_name}" '
                  'to name input field in indices page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_index_name_to_input_field_in_indices_page(selenium, browser_id,
                                                   oz_page, index_name):
    driver = selenium[browser_id]
    oz_page(driver)['discovery'].indices_page.name_input = index_name


@wt(parsers.parse('user of {browser_id} clicks on Create button '
                  'in indices page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_create_button_in_indices_page(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['discovery'].indices_page.create_button()


@wt(parsers.parse('user of {browser_id} sees that "{index_name}" '
                  'has appeared on the indices list'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_index_has_appeared_in_indices_page(selenium, browser_id, oz_page,
                                              index_name):
    driver = selenium[browser_id]
    indices_list = oz_page(driver)['discovery'].indices_page.indices_list
    assert index_name in indices_list, 'index "{}" not found'.format(index_name)


@wt(parsers.parse('user of {browser_id} expands "{index_name}" index record '
                  'in indices page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def expand_index_record_in_indices_page(selenium, browser_id, oz_page,
                                        index_name):
    driver = selenium[browser_id]
    indices_list = oz_page(driver)['discovery'].indices_page.indices_list
    indices_list[index_name].click()


@wt(parsers.parse('user of {browser_id} sees "Used by GUI" tag on '
                  '"{index}" index record in indices page'))
def assert_used_by_gui_tag_on_indices_page(selenium, browser_id, oz_page,
                                           index):
    driver = selenium[browser_id]
    indices_list = oz_page(driver)['discovery'].indices_page.indices_list
    assert indices_list[index].is_used_by_gui_tag_visible(), ('Used by GUI '
                                                              'tag is not '
                                                              'visible for '
                                                              f'{index}')


@wt(parsers.parse('user of {browser_id} sees 100% progress for '
                  'all spaces in "{index_name}" index harvesting'))
@repeat_failed(timeout=WAIT_BACKEND * 4)
def assert_progress_in_harvesting(selenium, browser_id, oz_page,
                                  index_name):
    driver = selenium[browser_id]
    value = '100%'
    indices_list = oz_page(driver)['discovery'].indices_page.indices_list
    progress_values = indices_list[index_name].progress_values

    for progress in progress_values:
        assert progress.progress_value == value, ('Harvesting process did not '
                                                  f'finished for '
                                                  f'"{progress.space}"')
