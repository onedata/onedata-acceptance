"""This module contains gherkin steps to run acceptance tests featuring
spaces management in onepanel web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import time

import yaml
import re

from selenium.common.exceptions import StaleElementReferenceException

from tests.gui.steps.common.login import wt_login_using_basic_auth
from tests.utils.bdd_utils import wt, parsers
from tests.utils.utils import repeat_failed
from tests.gui.conftest import (WAIT_FRONTEND, WAIT_BACKEND,
                                SELENIUM_IMPLICIT_WAIT)
from tests.gui.utils.generic import transform, implicit_wait, parse_seq
from tests.gui.steps.common.miscellaneous import _enter_text


@wt(parsers.parse('user of {browser_id} selects "{storage}" from storage '
                  'selector in support space form in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_select_storage_in_support_space_form(selenium, browser_id, storage,
                                            onepanel):
    storage_selector = (onepanel(selenium[browser_id]).content.spaces.form.storage_selector)
    storage_selector.expand()
    storage_selector.options[storage].click()


@wt(parsers.parse('user of {browser_id} clicks on Support space button '
                  'in spaces page in Onepanel if there are some spaces '
                  'already supported'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_on_support_space_btn_on_condition(selenium, browser_id, onepanel):
    driver = selenium[browser_id]
    # set implicit wait in case spaces list take time to load,
    # otherwise one can miss it and not click the button
    with implicit_wait(driver, 1, SELENIUM_IMPLICIT_WAIT):
        spaces_page = onepanel(driver).content.spaces
        if spaces_page.spaces.count() > 0:
            spaces_page.support_space()


@wt(parsers.re('user of (?P<browser_id>.+?) selects (?P<btn>MiB|GiB|TiB) '
               'radio button in support space form in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_select_unit_in_space_support_form(selenium, browser_id, btn,
                                         onepanel):
    onepanel(selenium[browser_id]).content.spaces.form.units[btn].click()


@wt(parsers.re('user of (?P<browser_id>.+?) selects (?P<btn>auto|manual) '
               'radio button in support space form in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_select_mode_in_space_support_form(selenium, browser_id, btn,
                                         onepanel):
    form = onepanel(selenium[browser_id]).content.spaces.form
    form.storage_import_configuration.modes[btn].click()


@wt(parsers.re('user of (?P<browser_id>.+?) clicks on Support space '
               'button in support space form in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_on_btn_in_space_support_form(selenium, browser_id, onepanel):
    onepanel(selenium[browser_id]).content.spaces.form.support_space()


@wt(parsers.parse('user of {browser_id} types received token to Support token '
                  'field in support space form in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_received_token_to_support_token_field(selenium, browser_id,
                                                  onepanel, tmp_memory):
    form = onepanel(selenium[browser_id]).content.spaces.form
    form.token = tmp_memory[browser_id]['mailbox']['token']


@wt(parsers.parse('user of {browser_id} types "{text}" to {input_box} input '
                  'field in support space form in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_text_to_input_box_in_space_support_form(selenium, browser_id, text,
                                                    input_box, onepanel):
    form = onepanel(selenium[browser_id]).content.spaces.form
    setattr(form, transform(input_box), text)


@wt(parsers.re(r'user of (?P<browser_id>.*?) enables '
               r'(?P<toggle>.*) option '
               r'in support space form in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_enable_option_box_in_space_support_form(selenium, browser_id, toggle,
                                               onepanel):
    storage_import_configuration = onepanel(
        selenium[browser_id]).content.spaces.form.storage_import_configuration
    getattr(storage_import_configuration, transform(toggle)).check()


def wt_disable_option_box_in_space_support_form(selenium, browser_id, toggle,
                                                onepanel):
    storage_import_configuration = onepanel(
        selenium[browser_id]).content.spaces.form.storage_import_configuration
    getattr(storage_import_configuration, transform(toggle)).uncheck()


@wt(parsers.parse('user of {browser_id} sees that space support record for '
                  '"{space_name}" has appeared in Spaces page in Onepanel'))
@repeat_failed(timeout=WAIT_BACKEND)
def wt_assert_existence_of_space_support_record(selenium, browser_id,
                                                space_name, onepanel):
    spaces = {space.name for space
              in onepanel(selenium[browser_id]).content.spaces.spaces}
    assert space_name in spaces, ('not found "{}" in spaces in Onepanel'
                                  .format(space_name))


@wt(parsers.parse('user of {browser_id} sees that list of supported spaces '
                  'is empty in Spaces page in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_supported_spaces_list_is_empty(selenium, browser_id, onepanel):
    count = onepanel(selenium[browser_id]).content.spaces.spaces.count()
    assert count == 0, \
        'There is(are) {} supported spaces instead of expected none'.format(count)


@wt(parsers.re(r'user of (?P<browser_id>.*?) selects (?P<strategy>.*?) '
               r'strategy from strategy selector in (?P<conf>IMPORT|UPDATE) '
               r'CONFIGURATION in support space form in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_select_strategy_in_conf_in_support_space_form(selenium, browser_id,
                                                     strategy, conf, onepanel):
    config = getattr(onepanel(selenium[browser_id]).content.spaces.form,
                     conf.lower() + '_configuration')
    strategy_selector = config.strategy_selector
    strategy_selector.expand()
    strategy_selector.options[strategy].click()


@wt(parsers.re(r'user of (?P<browser_id>.*?) types "(?P<text>.*?)" '
               r'to (?P<input_box>.*) input field in support space form '
               r'in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_text_to_input_box_in_storage_import_configuration(selenium,
                                                              browser_id, text,
                                                              input_box,
                                                              onepanel):
    input_name = transform(input_box)
    form = onepanel(
        selenium[browser_id]).content.spaces.form
    if hasattr(form, input_name):
        setattr(form, input_name, text)
    elif hasattr(form.storage_import_configuration, input_name):
        setattr(form.storage_import_configuration, input_name, text)
    else:
        raise RuntimeError(
            (f'failed typing text into {input_box} input field in '
             f'support space form '))


@wt(parsers.re(r'user of (?P<browser_id>.*?) selects (?P<strategy>.*?) '
               r'strategy from strategy selector in (?P<conf>IMPORT|UPDATE) '
               r'CONFIGURATION in "(?P<space>.*?)" record '
               r'in Spaces page in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_select_strategy_in_conf_in_space_record(selenium, browser_id, strategy,
                                               conf, onepanel):
    config = getattr(onepanel(selenium[browser_id]).content.spaces.space.
                     sync_chart, conf.lower() + '_configuration')
    strategy_selector = config.strategy_selector
    strategy_selector.expand()
    strategy_selector.options[strategy].click()


@wt(parsers.re(r'user of (?P<browser_id>.*?) types "(?P<text>.*?)" '
               r'to (?P<input_box>.*) input field in (?P<conf>IMPORT|UPDATE) '
               r'CONFIGURATION in "(?P<space>.*?)" record '
               r'in Spaces page in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_text_to_input_box_in_conf_in_space_record(selenium, browser_id,
                                                      text, input_box, conf,
                                                      onepanel):
    config = getattr(onepanel(selenium[browser_id]).content.spaces.space.
                     sync_chart, conf.lower() + '_configuration')
    setattr(config, transform(input_box), text)


@wt(parsers.parse('user of {browser_id} clicks on {button} '
                  'button in "{space}" record in Spaces page in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_clicks_on_button_in_space_record(selenium, browser_id, onepanel, button):
    driver = selenium[browser_id]
    sync_chart = onepanel(driver).content.spaces.space.sync_chart
    getattr(sync_chart, transform(button)).click()


@wt(parsers.parse('user of {browser_id} opens "{space}" record on '
                  'spaces list in Spaces page in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_open_space_item_in_spaces_page_op_panel(selenium, browser_id, space,
                                               onepanel):
    onepanel(selenium[browser_id]).content.spaces.spaces[space].click()


@wt(parsers.parse('user of {browser_id} sees that {sync_type} strategy '
                  'configuration for "{space_name}" is as follow:\n{conf}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_proper_space_configuration_in_panel(selenium, browser_id,
                                                  sync_type, space_name, conf,
                                                  onepanel):
    """Assert configuration displayed in space record in panel.

    conf should be in yaml format exactly as seen in panel, e.g.
        Mode: auto
        Max depth: 2
        Synchronize ACL: false
        Detect modifications: false
        Detect deletions: false
        Continuous scan: true
        Scan interval [s]: 10

    """

    driver = selenium[browser_id]
    space = onepanel(driver).content.spaces.space
    space.navigation.overview()
    displayed_conf = getattr(space.overview, sync_type.lower() + '_strategy')

    for attr, val in yaml.load(conf).items():
        displayed_val = displayed_conf[attr]
        assert str(val).lower() == displayed_val.lower(), (
            'Displayed {} as {} instead of expected {} in {} strategy of '
            '"{}" configuration'.format(displayed_val, attr, val, sync_type,
                                        space_name))


@wt(parsers.parse('user of {browser_id} copies Id of "{space}" space '
                  'in Spaces page in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_copy_space_id_in_spaces_page_in_onepanel(selenium, browser_id, space,
                                                onepanel, tmp_memory):
    record = onepanel(selenium[browser_id]).content.spaces.space
    tmp_memory['spaces'][space] = record.overview.space_id


@wt(parsers.parse('user of {browser_id} expands toolbar for "{space_name}" '
                  'space record in Spaces page in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_expands_toolbar_icon_for_space_in_onepanel(selenium, browser_id,
                                                  space_name, onepanel):
    driver = selenium[browser_id]
    onepanel(driver).content.spaces.spaces[space_name].expand_menu(driver)


@wt(parsers.re(r"user of (?P<browser_id>.*?) clicks on "
               r"(?P<option>Revoke space support|"
               r"Configure data synchronization|"
               r"Cancel sync. configuration) "
               r"option in space's toolbar in Onepanel"))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_clicks_on_btn_in_space_toolbar_in_panel(selenium, browser_id, option,
                                               popups):
    toolbar = popups(selenium[browser_id]).toolbar
    if toolbar.is_displayed():
        toolbar.options[option].click()
    else:
        raise RuntimeError('no space toolbar found in Onepanel')


@wt(parsers.re(r'user of (?P<browser_id>.*?) clicks on '
               r'(?P<button>Cease support|Cancel) button '
               r'in cease oneprovider support for space modal in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_clicks_on_btn_in_cease_support_modal(selenium, browser_id,
                                            button, modals):
    modal = modals(selenium[browser_id]).cease_support_for_space
    if button == 'Cease support':
        modal.cease_support()
    else:
        modal.cancel()


# TODO: delete after space support revoke fixes in 21.02 (VFS-6383)
@wt(parsers.parse('user of {browser_id} removes space using '
                  'delete space modal invoked from provided link'))
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_space_instead_of_revoke(selenium, browser_id, modals):
    modals(selenium[browser_id]).cease_support_for_space.space_delete_link()
    time.sleep(2)
    modals(selenium[browser_id]).remove_space.understand_notice()
    modals(selenium[browser_id]).remove_space.remove()


# TODO: delete after space support revoke fixes in 21.02 (VFS-6383)
@wt(parsers.parse('user of {browser_id} logs in as "{user}" to Onezone service '
                  'and removes space using delete space modal invoked from '
                  'provided link'))
@repeat_failed(timeout=WAIT_FRONTEND)
def login_and_remove_space_instead_of_revoke(selenium, browser_id, modals, user,
                                             login_page, users):
    modals(selenium[browser_id]).cease_support_for_space.space_delete_link()
    time.sleep(3)
    wt_login_using_basic_auth(selenium, browser_id, user,
                              login_page, users, 'Onezone')
    modals(selenium[browser_id]).remove_space.understand_notice()
    modals(selenium[browser_id]).remove_space.remove()


@wt(parsers.parse('user of {browser_id} checks the understand notice '
                  'in cease oneprovider support for space modal in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_clicks_on_understand_risk_in_cease_support_modal(selenium, browser_id,
                                                        modals):
    (modals(selenium[browser_id]).cease_support_for_space
     .understand_risk_checkbox())


@wt(parsers.parse('user of {browser_id} clicks on '
                  'Configure button in "{space}" '
                  'record in Spaces page in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_clicks_on_configure(selenium, browser_id, onepanel):
    (onepanel(selenium[browser_id]).content.spaces.space.sync_chart.configure())


@wt(parsers.parse('user of {browser_id} clicks '
                  'settings in Storage import in Spaces page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_clicks_on_option_in_spaces_page(selenium, browser_id, onepanel):
    space = onepanel(selenium[browser_id]).content.spaces.space
    space.sync_chart.settings()


@wt(parsers.re(r'user of (?P<browser_id>.*?) sees that number of '
               r'(?P<bar_type>inserted|updated|deleted) files for '
               r'"(?P<space_name>.*?)" shown on Synchronization files '
               r'processing charts equals (?P<num>\d+) '
               r'in Spaces page in Onepanel'))
@repeat_failed(timeout=WAIT_BACKEND*10, interval=2)
def assert_correct_number_displayed_on_sync_charts(selenium, browser_id,
                                                   bar_type, onepanel, num):
    num = int(num)
    record = onepanel(selenium[browser_id]).content.spaces.space
    displayed_num = getattr(record.sync_chart, bar_type)
    assert displayed_num == num, (
        'displayed {} as number of {} files on sync chart instead of '
        'expected {}'.format(displayed_num, bar_type, num))


@wt(parsers.parse('user of {browser_id} sees {tab_list} navigation tabs for '
                  'space "{space_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def are_nav_tabs_for_space_displayed(selenium, browser_id, tab_list, space_name,
                                     onepanel):
    nav = onepanel(selenium[browser_id]).content.spaces.spaces[
        space_name].navigation

    for tab in parse_seq(tab_list):
        assert getattr(nav, transform(tab, strip_char='"')) is not None, \
            'no navigation tab {} found'.format(tab)


@wt(parsers.parse('user of {browser_id} clicks on {tab_name} navigation '
                  'tab in space "{space_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_navigation_tab_in_space(browser_id, tab_name, onepanel, selenium):
    nav = onepanel(selenium[browser_id]).content.spaces.space.navigation
    tab = transform(tab_name, strip_char='"')
    getattr(nav, tab).click()


@wt(parsers.parse('user of {browser_id} clicks on {interval} update view'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_interval_update(browser_id, interval, onepanel, selenium):
    getattr(onepanel(selenium[browser_id]).content.spaces.space.sync_chart,
            transform(interval + ' view')).click()


@wt(parsers.parse('user of {browser_id} cannot click on {tab_name} '
                  'navigation tab in space "{space_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def cannot_click_on_navigation_tab_in_space(browser_id, tab_name, onepanel,
                                            selenium):
    nav = onepanel(selenium[browser_id]).content.spaces.space.navigation
    tab = transform(tab_name, strip_char='"')
    try:
        getattr(nav, tab).click()
    except RuntimeError:
        return
    else:
        raise RuntimeError('can click on {}'.format(tab_name))


@wt(parsers.parse('user of {browser_id} enables {option} '
                  'in "{space}" space in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def enable_space_option_in_onepanel(selenium, browser_id, onepanel, option):
    driver = selenium[browser_id]
    option = option.replace('-', '_')
    tab = getattr(onepanel(driver).content.spaces.space, option)
    toggle = 'enable_{}'.format(option)
    getattr(tab, toggle).check()


@wt(parsers.parse('user of {browser_id} enables selective cleaning '
                  'in auto-cleaning tab in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def enable_selective_cleaning(selenium, browser_id, onepanel):
    driver = selenium[browser_id]
    op = onepanel(driver)
    op.content.spaces.space.auto_cleaning.selective_cleaning.check()


@wt(parsers.parse('user of {browser_id} enables {option} '
                  'in auto-cleaning tab in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def enable_option_in_auto_cleaning(selenium, browser_id, onepanel, option):
    driver = selenium[browser_id]
    tab = onepanel(driver).content.spaces.space.auto_cleaning
    tab.selective_cleaning_form[option].checkbox.check()


@wt(parsers.parse('user of {browser_id} clicks {option} on dropdown '
                  '{rule} rule in auto-cleaning tab in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_option_on_dropdown_rule(selenium, browser_id, onepanel, option, rule):
    driver = selenium[browser_id]
    tab = onepanel(driver).content.spaces.space.auto_cleaning
    for i in range(5):
        if tab.selective_cleaning_form[rule].value_limit != option:
            tab.selective_cleaning_form[rule].dropdown_button()
            tab.selective_cleaning_form[rule].dropdown[option].click()
        else:
            break


@wt(parsers.parse('user of {browser_id} clicks change {quota} quota button '
                  'in auto-cleaning tab in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_change_quota_button(selenium, browser_id, quota, onepanel):
    button = 'click_rename_{}_quota_button'.format(quota)
    driver = selenium[browser_id]
    getattr(onepanel(driver).content.spaces.space.auto_cleaning, button)(driver)


@wt(parsers.parse('user of {browser_id} types "{value}" to {quota} quota '
                  'input field in auto-cleaning tab in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def type_value_to_quota_input(selenium, browser_id, quota, value, onepanel):
    quota = '{}_quota'.format(quota)
    driver = selenium[browser_id]
    _enter_text(getattr(onepanel(driver).content.spaces.space.auto_cleaning,
                        quota).edit_input, value)


@wt(parsers.parse('user of {browser_id} confirms changing value '
                  'of {quota} quota in auto-cleaning tab in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def confirm_quota_value_change(selenium, browser_id, quota, onepanel):
    quota = '{}_quota'.format(quota)
    driver = selenium[browser_id]
    getattr(onepanel(driver).content.spaces.space.auto_cleaning,
            quota).accept_button()


@wt(parsers.parse('user of {browser_id} clicks on "Start cleaning now" button '
                  'in auto-cleaning tab in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_start_cleaning_now(selenium, browser_id, onepanel):
    driver = selenium[browser_id]
    onepanel(driver).content.spaces.space.auto_cleaning.start_cleaning_now()


@wt(parsers.parse('user of {browser_id} sees {size} released size '
                  'in cleaning report in Onepanel'))
@repeat_failed(interval=1, timeout=220,
               exceptions=(AssertionError, StaleElementReferenceException))
def see_released_size_in_cleaning_report(selenium, browser_id, onepanel, size):
    driver = selenium[browser_id]
    cleaning_reports = (onepanel(driver).content.spaces.space
                        .auto_cleaning.cleaning_reports)
    for cleaning_report in cleaning_reports:
        released_size = re.match(r'((\d+) (MiB|B)) '
                                 r'\(out of (\d*\.\d+|\d+) MiB\)',
                                 cleaning_report.released_size.text).group(1)
        if released_size == size:
            return
    err_msg = f'released size: {released_size}  is not expected size: {size}'
    assert False, err_msg


def toggle_in_storage_import_configuration_is_enabled(selenium, browser_id,
                                                      onepanel, toggle_name):
    storage_import_conf = onepanel(
        selenium[browser_id]).content.spaces.form.storage_import_configuration
    return storage_import_conf.is_toggle_checked(transform(toggle_name))


@wt(parsers.parse('user of {browser_id} clicks on "Start scan" button '
                  'in storage import tab in Onepanel'))
def click_start_scan_button_in_storage_import_tab(selenium, browser_id,
                                                  onepanel):
    driver = selenium[browser_id]
    onepanel(driver).content.spaces.space.sync_chart.start_scan()


@wt(parsers.parse('user of {browser_id} waits until scanning is finished '
                  'in storage import tab in Onepanel'))
@repeat_failed(timeout=WAIT_BACKEND, interval=4)
def wait_until_scanning_is_finished_in_storage_import_tab(selenium, browser_id,
                                                          onepanel):
    driver = selenium[browser_id]
    assert onepanel(
        driver).content.spaces.space.sync_chart.start_scan_is_green(), (
        f'Scanning did not finish correctly, "Start scan" button is not green')
