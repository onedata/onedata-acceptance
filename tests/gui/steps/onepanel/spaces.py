"""This module contains gherkin steps to run acceptance tests featuring
spaces management in onepanel web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


import yaml

from pytest_bdd import when, then, parsers

from tests.utils.utils import repeat_failed
from tests.gui.conftest import (WAIT_FRONTEND, WAIT_BACKEND,
                                SELENIUM_IMPLICIT_WAIT)
from tests.gui.utils.generic import transform, implicit_wait, parse_seq
from tests.utils.acceptance_utils import wt


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
                    '"{space}" has appeared in Spaces page in Onepanel'))
@then(parsers.parse('user of {browser_id} sees that space support record for '
                    '"{space}" has appeared in Spaces page in Onepanel'))
@repeat_failed(timeout=WAIT_BACKEND)
def wt_assert_existence_of_space_support_record(selenium, browser_id,
                                                space, onepanel):
    spaces = {space.name for space
              in onepanel(selenium[browser_id]).content.spaces.spaces}
    assert space in spaces, 'not found "{}" in spaces in Onepanel'.format(space)


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
                                               conf, space, onepanel):
    config = getattr(onepanel(selenium[browser_id]).content.spaces.
                     spaces[space], conf.lower() + '_configuration')
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
                                                      space, onepanel):
    config = getattr(onepanel(selenium[browser_id]).content.spaces.
                     spaces[space], conf.lower() + '_configuration')
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
                                                 toggle, space, onepanel):
    config = (onepanel(selenium[browser_id]).content.spaces.
              spaces[space].update_configuration)
    getattr(config, transform(toggle)).check()


@when(parsers.parse('user of {browser_id} clicks on Save configuration '
                    'button in "{space}" record in Spaces page in Onepanel'))
@then(parsers.parse('user of {browser_id} clicks on Save configuration '
                    'button in "{space}" record in Spaces page in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_clicks_on_save_config_btn_in_space_record(selenium, browser_id,
                                                 space, onepanel):
    (onepanel(selenium[browser_id]).content.spaces.
     spaces[space].save_configuration())


@when(parsers.parse('user of {browser_id} expands "{space}" record on '
                    'spaces list in Spaces page in Onepanel'))
@then(parsers.parse('user of {browser_id} expands "{space}" record on '
                    'spaces list in Spaces page in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_expand_space_item_in_spaces_page_op_panel(selenium, browser_id,
                                                 space, onepanel):
    onepanel(selenium[browser_id]).content.spaces.spaces[space].expand()


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
    info = onepanel(selenium[browser_id]).content.spaces.spaces[space_name].info
    displayed_conf = getattr(info, sync_type.lower() + '_strategy')
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
    record = onepanel(selenium[browser_id]).content.spaces.spaces[space]
    tmp_memory['spaces'][space] = record.info.space_id


@when(parsers.parse('user of {browser_id} expands toolbar for "{space}" '
                    'space record in Spaces page in Onepanel'))
@then(parsers.parse('user of {browser_id} expands toolbar for "{space}" '
                    'space record in Spaces page in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_expands_toolbar_icon_for_space_in_onepanel(selenium, browser_id,
                                                  space, onepanel):
    record = onepanel(selenium[browser_id]).content.spaces.spaces[space]
    record.toolbar.click()


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


@when(parsers.re(r'user of (?P<browser_id>.*?) clicks on '
                 r'(?P<button>Yes, revoke|No, keep the support) '
                 r'button in REVOKE SPACE SUPPORT modal in Onepanel'))
@then(parsers.re(r'user of (?P<browser_id>.*?) clicks on '
                 r'(?P<button>Yes, revoke|No, keep the support) '
                 r'button in REVOKE SPACE SUPPORT modal in Onepanel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_clicks_on_btn_in_revoke_space_support(selenium, browser_id,
                                             button, modals):
    modal = modals(selenium[browser_id]).revoke_space_support
    if button == 'Yes, revoke':
        modal.yes()
    else:
        modal.no()


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
                                                   bar_type, space_name,
                                                   onepanel, num):
    num = int(num)
    record = onepanel(selenium[browser_id]).content.spaces.spaces[space_name]
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
def click_on_navigation_tab_in_space(browser_id, tab_name, onepanel, selenium,
                                     space_name, tmp_memory):
    nav = onepanel(selenium[browser_id]).content.spaces.spaces[space_name].navigation
    tab = getattr(nav, transform(tab_name, strip_char='"'))
    tab()


@wt(parsers.parse('user of {browser_id} revokes all spaces supports'))
@repeat_failed(timeout=WAIT_FRONTEND)
def revoke_all_space_supports(selenium, browser_id, onepanel, popups, modals):
    spaces_list = onepanel(selenium[browser_id]).content.spaces.spaces
    option = 'Revoke space support'
    button = 'Yes, revoke'
    for space in spaces_list:
        space.toolbar.click()
        wt_clicks_on_btn_in_space_toolbar_in_panel(selenium, browser_id,
                                                   option, popups)
        wt_clicks_on_btn_in_revoke_space_support(selenium, browser_id,
                                                 button, modals)
