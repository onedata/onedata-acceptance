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
from tests.gui.utils.generic import parse_seq


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


@wt(parsers.parse('user of {browser_id} unchecks all toggles apart from '
                  '{stay_checked} in indices page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def uncheck_toggles_on_create_index_page(selenium, browser_id, oz_page,
                                         stay_checked):
    driver = selenium[browser_id]
    stay_checked = parse_seq(stay_checked)
    for toggle in oz_page(driver)['discovery'].indices_page.toggles:
        if toggle not in stay_checked:
            getattr(oz_page(driver)['discovery'].indices_page,
                    toggle).check()


@wt(parsers.parse('user of {browser_id} changes indices to "{index_name}" '
                  'on GUI plugin tab on harvester configuration page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def change_indices_on_gui_plugin_tab(selenium, browser_id, oz_page, index_name,
                                     popups):
    driver = selenium[browser_id]
    (oz_page(driver)['discovery'].configuration_page
     .gui_plugin_tab.indices_edit())
    (oz_page(driver)['discovery'].configuration_page
     .gui_plugin_tab.choose_indices_expand())
    popups(driver).power_select.choose_item(index_name)
    (oz_page(driver)['discovery'].configuration_page
     .gui_plugin_tab.indices_save())


@wt(parsers.parse('user of {browser_id} does not see "{text}" in'
                  ' results list on data discovery page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_not_text_on_data_discovery_page(selenium, browser_id,
                                           data_discovery, text):
    driver = selenium[browser_id]
    assert (text not in data_discovery(driver).results_list[0].text,
            f'{text} in result list')


@wt(parsers.parse('user of {browser_id} sees rejected "{text}"'
                  ' in results list on data discovery page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_rejected_on_data_discovery_page(selenium, browser_id,
                                           data_discovery, text):
    driver = selenium[browser_id]
    text = f' __rejected: {text}'
    assert (text in data_discovery(driver).results_list[0].text,
            f'{text} not in result list')


@wt(parsers.parse('user of browser sees that rejection is caused by field '
                  '{key} of type {field_type} in document dir1'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_rejection_reason_on_data_discovery_page(selenium, browser_id,
                                                   data_discovery, key,
                                                   field_type, clipboard,
                                                   displays):
    driver = selenium[browser_id]
    file_id = clipboard.paste(display=displays[browser_id])
    text = (f'__rejectionReason: "failed to parse field {key} of type'
            f' {field_type} in document with id {file_id}')
    assert (text in data_discovery(driver).results_list[0].text,
            f'{text} not in result list {data_discovery(driver).results_list[0].text}')

