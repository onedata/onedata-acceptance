"""This module contains gherkin steps to run acceptance tests featuring
spaces management in onepanel web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


import yaml
import re

from pytest_bdd import when, then, parsers
from selenium.common.exceptions import StaleElementReferenceException

from tests.utils.utils import repeat_failed
from tests.gui.conftest import (WAIT_FRONTEND, WAIT_BACKEND,
                                SELENIUM_IMPLICIT_WAIT)
from tests.gui.utils.generic import transform, implicit_wait, parse_seq
from tests.utils.acceptance_utils import wt
from tests.gui.steps.common.miscellaneous import _enter_text


@when(parsers.parse('user of {browser_id} selects "{storage}" from storage '
                    'selector in support space form in Onepanel'))
@then(parsers.parse('user of {browser_id} selects "{storage}" from storage '
                    'selector in support space form in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_select_storage_in_support_space_form(selenium, browser_id,
                                            storage, onepanel):
    storage_selector = (onepanel(selenium[browser_id]).content.spaces.
                        form.storage_selector)
    storage_selector.expand()
    storage_selector.options[storage].click()


@when(parsers.parse('user of {browser_id} clicks on Support space button '
                    'in spaces page in Onepanel if there are some spaces '
                    'already supported'))
@then(parsers.parse('user of {browser_id} clicks on Support space button '
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


@when(parsers.re('user of (?P<browser_id>.+?) selects (?P<btn>MiB|GiB|TiB) radio '
                 'button in support space form in Onepanel'))
@then(parsers.re('user of (?P<browser_id>.+?) selects (?P<btn>MiB|GiB|TiB) radio '
                 'button in support space form in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_select_unit_in_space_support_add_form(selenium, browser_id,
                                             btn, onepanel):
    onepanel(selenium[browser_id]).content.spaces.form.units[btn].click()


@when(parsers.re('user of (?P<browser_id>.+?) clicks on Support space '
                 'button in support space form in Onepanel'))
@then(parsers.re('user of (?P<browser_id>.+?) clicks on Support space '
                 'button in support space form in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_on_btn_in_space_support_add_form(selenium, browser_id, onepanel):
    onepanel(selenium[browser_id]).content.spaces.form.support_space()


@when(parsers.parse('user of {browser_id} types received token to Support token '
                    'field in support space form in Onepanel'))
@then(parsers.parse('user of {browser_id} types received token to Support token '
                    'field in support space form in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_received_token_to_support_token_field(selenium, browser_id,
                                                  onepanel, tmp_memory):
    form = onepanel(selenium[browser_id]).content.spaces.form
    form.token = tmp_memory[browser_id]['mailbox']['token']


@when(parsers.parse('user of {browser_id} types "{text}" to {input_box} input '
                    'field in support space form in Onepanel'))
@then(parsers.parse('user of {browser_id} types "{text}" to {input_box} input '
                    'field in support space form in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_text_to_input_box_in_space_support_form(selenium, browser_id, text,
                                                    input_box, onepanel):
    form = onepanel(selenium[browser_id]).content.spaces.form
    setattr(form, transform(input_box), text)


@when(parsers.re(r'user of (?P<browser_id>.*?) enables '
                 r'(?P<toggle>Mount in root|Import storage data) option '
                 r'in support space form in Onepanel'))
@then(parsers.re(r'user of (?P<browser_id>.*?) enables '
                 r'(?P<toggle>Mount in root|Import storage data) option '
                 r'in support space form in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_enable_option_box_in_space_support_form(selenium, browser_id,
                                               toggle, onepanel):
    form = onepanel(selenium[browser_id]).content.spaces.form
    getattr(form, transform(toggle)).check()


@when(parsers.parse('user of {browser_id} sees that space support record for '
                    '"{space_name}" has appeared in Spaces page in Onepanel'))
@then(parsers.parse('user of {browser_id} sees that space support record for '
                    '"{space_name}" has appeared in Spaces page in Onepanel'))
@repeat_failed(timeout=WAIT_BACKEND)
def wt_assert_existence_of_space_support_record(selenium, browser_id,
                                                space_name, onepanel):
    spaces = {space.name for space
              in onepanel(selenium[browser_id]).content.spaces.spaces}
    assert space_name in spaces, ('not found "{}" in spaces in Onepanel'
                                  .format(space_name))


@when(parsers.parse('user of {browser_id} sees that list of supported spaces '
                    'is empty in Spaces page in Onepanel'))
@then(parsers.parse('user of {browser_id} sees that list of supported spaces '
                    'is empty in Spaces page in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_supported_spaces_list_is_empty(selenium, browser_id, onepanel):
    count = onepanel(selenium[browser_id]).content.spaces.spaces.count()
    assert count == 0, \
        'There is(are) {} supported spaces instead of expected none'.format(count)


@when(parsers.re(r'user of (?P<browser_id>.*?) selects (?P<strategy>.*?) '
                 r'strategy from strategy selector in (?P<conf>IMPORT|UPDATE) '
                 r'CONFIGURATION in support space form in Onepanel'))
@then(parsers.re(r'user of (?P<browser_id>.*?) selects (?P<strategy>.*?) '
                 r'strategy from strategy selector in (?P<conf>IMPORT|UPDATE) '
                 r'CONFIGURATION in support space form in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_select_strategy_in_conf_in_support_space_form(selenium, browser_id,
                                                     strategy, conf, onepanel):
    config = getattr(onepanel(selenium[browser_id]).content.spaces.
                     form, conf.lower() + '_configuration')
    strategy_selector = config.strategy_selector
    strategy_selector.expand()
    strategy_selector.options[strategy].click()


@when(parsers.re(r'user of (?P<browser_id>.*?) types "(?P<text>.*?)" '
                 r'to (?P<input_box>.*) input field in (?P<conf>IMPORT|UPDATE) '
                 r'CONFIGURATION in support space form in Onepanel'))
@then(parsers.re(r'user of (?P<browser_id>.*?) types "(?P<text>.*?)" '
                 r'to (?P<input_box>.*) input field in (?P<conf>IMPORT|UPDATE) '
                 r'CONFIGURATION in support space form in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_type_text_to_input_box_in_conf_in_space_support_form(selenium, browser_id,
                                                            text, input_box,
                                                            conf, onepanel):
    config = getattr(onepanel(selenium[browser_id]).content.spaces.form,
                     conf.lower() + '_configuration')
    setattr(config, transform(input_box), text)


@when(parsers.re(r'user of (?P<browser_id>.*?) enables '
                 r'(?P<toggle>Write once|Delete enabled) option '
                 r'UPDATE CONFIGURATION in support space form in Onepanel'))
@then(parsers.re(r'user of (?P<browser_id>.*?) enables '
                 r'(?P<toggle>Write once|Delete enabled) option '
                 r'UPDATE CONFIGURATION in support space form in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_enable_option_box_in_conf_in_space_support_form(selenium, browser_id,
                                                       toggle, onepanel):
    conf = onepanel(selenium[browser_id]).content.spaces.form.update_configuration
    getattr(conf, transform(toggle)).check()


@when(parsers.re(r'user of (?P<browser_id>.*?) selects (?P<strategy>.*?) '
                 r'strategy from strategy selector in (?P<conf>IMPORT|UPDATE) '
                 r'CONFIGURATION in "(?P<space>.*?)" record '
                 r'in Spaces page in Onepanel'))
@then(parsers.re(r'user of (?P<browser_id>.*?) selects (?P<strategy>.*?) '
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


@when(parsers.re(r'user of (?P<browser_id>.*?) types "(?P<text>.*?)" '
                 r'to (?P<input_box>.*) input field in (?P<conf>IMPORT|UPDATE) '
                 r'CONFIGURATION in "(?P<space>.*?)" record '
                 r'in Spaces page in Onepanel'))
@then(parsers.re(r'user of (?P<browser_id>.*?) types "(?P<text>.*?)" '
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


@when(parsers.re(r'user of (?P<browser_id>.*?) enables '
                 r'(?P<toggle>Write once|Delete enabled) option UPDATE '
                 r'CONFIGURATION in "(?P<space>.*?)" record in Spaces page '
                 r'in Onepanel'))
@then(parsers.re(r'user of (?P<browser_id>.*?) enables '
                 r'(?P<toggle>Write once|Delete enabled) option UPDATE '
                 r'CONFIGURATION in "(?P<space>.*?)" record in Spaces page '
                 r'in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_enable_option_box_in_conf_in_space_record(selenium, browser_id,
                                                 toggle, onepanel):
    config = (onepanel(selenium[browser_id]).content.spaces.space.
              sync_chart.update_configuration)
    getattr(config, transform(toggle)).check()


@when(parsers.parse('user of {browser_id} clicks on {button} '
                    'button in "{space}" record in Spaces page in Onepanel'))
@then(parsers.parse('user of {browser_id} clicks on {button} '
                    'button in "{space}" record in Spaces page in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_clicks_on_button_in_space_record(selenium, browser_id, onepanel, button):
    driver = selenium[browser_id]
    sync_chart = onepanel(driver).content.spaces.space.sync_chart
    getattr(sync_chart, transform(button)).click()


@when(parsers.parse('user of {browser_id} expands "{space}" record on '
                    'spaces list in Spaces page in Onepanel'))
@then(parsers.parse('user of {browser_id} expands "{space}" record on '
                    'spaces list in Spaces page in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_expand_space_item_in_spaces_page_op_panel(selenium, browser_id,
                                                 space, onepanel):
    onepanel(selenium[browser_id]).content.spaces.spaces[space].click()


@when(parsers.parse('user of {browser_id} sees that {sync_type} strategy '
                    'configuration for "{space_name}" is as follow:\n{conf}'))
@then(parsers.parse('user of {browser_id} sees that {sync_type} strategy '
                    'configuration for "{space_name}" is as follow:\n{conf}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_assert_proper_space_configuration_in_panel(selenium, browser_id,
                                                  sync_type, space_name,
                                                  conf, onepanel):
    """Assert configuration displayed in space record in panel.

    conf should be in yaml format exactly as seen in panel, e.g.

        Update strategy: Simple scan
        Max depth: 20
        Scan interval [s]: 10
        Write once: true
        Delete enabled: false

    """

    driver = selenium[browser_id]
    space = onepanel(driver).content.spaces.space
    space.navigation.overview()
    displayed_conf = getattr(space.overview, sync_type.lower() + '_strategy')

    for attr, val in yaml.load(conf).items():
        displayed_val = displayed_conf[attr]
        assert str(val).lower() == displayed_val.lower(), \
            ('Displayed {} as {} instead of expected {} in {} strategy of '
             '"{}" configuration'.format(displayed_val, attr, val,
                                         sync_type, space_name))


@when(parsers.parse('user of {browser_id} copies Id of "{space}" space '
                    'in Spaces page in Onepanel'))
@then(parsers.parse('user of {browser_id} copies Id of "{space}" space '
                    'in Spaces page in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_copy_space_id_in_spaces_page_in_onepanel(selenium, browser_id,
                                                space, onepanel, tmp_memory):
    record = onepanel(selenium[browser_id]).content.spaces.space
    tmp_memory['spaces'][space] = record.overview.space_id


@when(parsers.parse('user of {browser_id} expands toolbar for "{space_name}" '
                    'space record in Spaces page in Onepanel'))
@then(parsers.parse('user of {browser_id} expands toolbar for "{space_name}" '
                    'space record in Spaces page in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_expands_toolbar_icon_for_space_in_onepanel(selenium, browser_id,
                                                  space_name, onepanel):
    driver = selenium[browser_id]
    onepanel(driver).content.spaces.spaces[space_name].expand_menu(driver)


@when(parsers.re(r"user of (?P<browser_id>.*?) clicks on "
                 r"(?P<option>Revoke space support|"
                 r"Configure data synchronization|"
                 r"Cancel sync. configuration) "
                 r"option in space's toolbar in Onepanel"))
@then(parsers.re(r"user of (?P<browser_id>.*?) clicks on "
                 r"(?P<option>Revoke space support|"
                 r"Configure data synchronization|"
                 r"Cancel sync. configuration) "
                 r"option in space's toolbar in Onepanel"))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_clicks_on_btn_in_space_toolbar_in_panel(selenium, browser_id,
                                               option, popups):
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


@wt(parsers.parse('user of {browser_id} checks the understand notice '
                  'in cease oneprovider support for space modal in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_clicks_on_understand_risk_in_cease_support_modal(selenium, browser_id,
                                                        modals):
    (modals(selenium[browser_id]).cease_support_for_space
     .understand_risk_checkbox())


@when(parsers.parse('user of {browser_id} clicks on '
                    'Configure button in "{space}" '
                    'record in Spaces page in Onepanel'))
@then(parsers.parse('user of {browser_id} clicks on '
                    'Configure button in "{space}" '
                    'record in Spaces page in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_clicks_on_configure(selenium, browser_id, onepanel):
    (onepanel(selenium[browser_id]).content.spaces.space
     .sync_chart.configure())


@when(parsers.parse('user of {browser_id} clicks '
                    'settings in Storage synchronization in Spaces page'))
@then(parsers.parse('user of {browser_id} clicks '
                    'settings in Storage synchronization in Spaces page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_clicks_on_option_in_spaces_page(selenium, browser_id, onepanel):
    space = onepanel(selenium[browser_id]).content.spaces.space
    space.sync_chart.settings()


@when(parsers.re(r'user of (?P<browser_id>.*?) sees that number of '
                 r'(?P<bar_type>inserted|updated|deleted) files for '
                 r'"(?P<space_name>.*?)" shown on Synchronization files '
                 r'processing charts equals (?P<num>\d+) '
                 r'in Spaces page in Onepanel'))
@then(parsers.re(r'user of (?P<browser_id>.*?) sees that number of '
                 r'(?P<bar_type>inserted|updated|deleted) files for '
                 r'"(?P<space_name>.*?)" shown on Synchronization files '
                 r'processing charts equals (?P<num>\d+) '
                 r'in Spaces page in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_correct_number_displayed_on_sync_charts(selenium, browser_id,
                                                   bar_type, onepanel, num):
    num = int(num)
    record = onepanel(selenium[browser_id]).content.spaces.space
    displayed_num = getattr(record.sync_chart, bar_type)
    assert displayed_num == num, \
        ('displayed {} as number of {} files on sync chart instead of '
         'expected {}'.format(displayed_num, bar_type, num))

matcher_are_nav_tabs_for_space_displayed = parsers.parse(
    'user of {browser_id} sees {tab_list} navigation tabs for space "{space_name}"')
@when(matcher_are_nav_tabs_for_space_displayed)
@then(matcher_are_nav_tabs_for_space_displayed)
@repeat_failed(timeout=WAIT_FRONTEND)
def are_nav_tabs_for_space_displayed(selenium, browser_id, tab_list, space_name,
                                     onepanel):
    nav = onepanel(selenium[browser_id]).content.spaces.spaces[space_name].navigation
    
    for tab in parse_seq(tab_list):
        assert getattr(nav, transform(tab, strip_char='"')) is not None, \
            'no navigation tab {} found'.format(tab)


matcher_click_on_navigation_tab_in_space = parsers.parse(
    'user of {browser_id} clicks on {tab_name} navigation '
    'tab in space "{space_name}"')
@when(matcher_click_on_navigation_tab_in_space)
@then(matcher_click_on_navigation_tab_in_space)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_navigation_tab_in_space(browser_id, tab_name, onepanel, selenium):
    nav = onepanel(selenium[browser_id]).content.spaces.space.navigation
    tab = transform(tab_name, strip_char='"')
    getattr(nav, tab).click()



@wt(parsers.parse('user of {browser_id} cannot click on {tab_name} '
                  'navigation tab in space "{space_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def cannot_click_on_navigation_tab_in_space(browser_id, tab_name, onepanel, selenium):
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
    onepanel(driver).content.spaces.space.auto_cleaning.selective_cleaning.check()


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
    tab.selective_cleaning_form[rule].dropdown_button()
    tab.selective_cleaning_form[rule].dropdown[option].click()


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
@repeat_failed(interval=1, timeout=90,
               exceptions=(AssertionError, StaleElementReferenceException))
def see_released_size_in_cleaning_report(selenium, browser_id, onepanel, size):
    driver = selenium[browser_id]
    cleaning_reports = (onepanel(driver).content.spaces.space
                        .auto_cleaning.cleaning_reports)
    for cleaning_report in cleaning_reports:
        released_size = re.match(r'((\d+) (MiB|B)) \(out of (\d*\.\d+|\d+) MiB\)',
                                 cleaning_report.released_size.text).group(1)
        if released_size == size:
            return
    assert False, f'released size is not {size}'

