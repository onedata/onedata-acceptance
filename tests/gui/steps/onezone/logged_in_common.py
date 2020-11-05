"""This module contains gherkin steps to run acceptance tests featuring
common operations in onezone web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.utils.acceptance_utils import list_parser
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.utils import repeat_failed


@repeat_failed(timeout=WAIT_BACKEND)
def _expand_oz_panel(oz_page, driver, panel):
    oz_page(driver)[panel].expand()


@given(parsers.re(r'users? of (?P<browser_id_list>.*) expanded the '
                  r'"(?P<panel_name>.*)" Onezone sidebar panel'))
def g_expand_oz_panel(selenium, browser_id_list, panel_name, oz_page):
    for browser_id in list_parser(browser_id_list):
        _expand_oz_panel(oz_page, selenium[browser_id], panel_name)


@wt(parsers.re('users? of (?P<browser_id_list>.*) expands? the '
               '"(?P<panel_name>.*)" Onezone sidebar panel'))
def wt_expand_oz_panel(selenium, browser_id_list, panel_name, oz_page):
    for browser_id in list_parser(browser_id_list):
        _expand_oz_panel(oz_page, selenium[browser_id], panel_name)


@wt(parsers.parse('user of {browser_id} sees alert with title "{title}" '
                  'on Onezone page'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_alert_with_title_in_oz(selenium, browser_id, title, oz_page):
    driver = selenium[browser_id]
    alert = oz_page(driver).provider_alert_message
    err_msg = f'expected alert: {title}, found: {alert}'
    assert alert == title, err_msg


@wt(parsers.re('user of (?P<browser_id>.+?) clicks on '
               '"(?P<btn>Create new space|Join space)" button in expanded '
               '"(?P<oz_panel>DATA SPACE MANAGEMENT)" Onezone panel'))
@wt(parsers.re('user of (?P<browser_id>.+?) clicks on '
               '"(?P<btn>Join a group)" button in expanded '
               '"(?P<oz_panel>GROUP MANAGEMENT)" Onezone panel'))
@repeat_failed(timeout=WAIT_BACKEND)
def click_on_btn_in_oz_panel(selenium, browser_id, btn, oz_panel, oz_page):
    driver = selenium[browser_id]
    action = getattr(oz_page(driver)[oz_panel], btn.lower().replace(' ', '_'))
    action()


@wt(parsers.re('user of (?P<browser_id>.+?) sees that there is '
               '(?P<item_type>provider) "(?P<item_name>.+?)" '
               'in expanded "(?P<oz_panel>GO TO YOUR FILES)" Onezone panel'))
@wt(parsers.re('user of (?P<browser_id>.+?) sees that (?P<item_type>provider) '
               '"(?P<item_name>.+?)" has appeared in expanded '
               '"(?P<oz_panel>GO TO YOUR FILES)" Onezone panel'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_there_is_item_with_known_name_in_oz_panel_list(selenium, browser_id,
                                                          item_type, item_name,
                                                          oz_panel, oz_page,
                                                          hosts):
    driver = selenium[browser_id]
    item_name = hosts[item_name]['name']
    items = getattr(oz_page(driver)[oz_panel], '{}s'.format(item_type))
    assert item_name in items, \
        'no {} named "{}" found in {} oz panel'.format(item_type, item_name,
                                                       oz_panel)


@wt(parsers.re('user of (?P<browser_id>.+?) sees that there is '
               '(?P<item_type>provider) named "(?P<item_name>.+?)" '
               'in expanded "(?P<oz_panel>GO TO YOUR FILES)" Onezone panel'))
@wt(parsers.re('user of (?P<browser_id>.+?) sees that (?P<item_type>provider) '
               'named "(?P<item_name>.+?)" has appeared in expanded '
               '"(?P<oz_panel>GO TO YOUR FILES)" Onezone panel'))
@wt(parsers.re('user of (?P<browser_id>.+?) sees that there is '
               '(?P<item_type>space) named "(?P<item_name>.+?)" in expanded '
               '"(?P<oz_panel>DATA SPACE MANAGEMENT)" Onezone panel'))
@wt(parsers.re('user of (?P<browser_id>.+?) sees that (?P<item_type>space) '
               'named "(?P<item_name>.+?)" has appeared in expanded '
               '"(?P<oz_panel>DATA SPACE MANAGEMENT)" Onezone panel'))
@wt(parsers.re('user of (?P<browser_id>.+?) sees that there is '
               '(?P<item_type>group) named "(?P<item_name>.+?)" in expanded '
               '"(?P<oz_panel>GROUP MANAGEMENT)" Onezone panel'))
@wt(parsers.re('user of (?P<browser_id>.+?) sees that (?P<item_type>group) '
               'named "(?P<item_name>.+?)" has appeared in expanded '
               '"(?P<oz_panel>GROUP MANAGEMENT)" Onezone panel'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_there_is_item_named_in_oz_panel_list(selenium, browser_id, item_type,
                                                item_name, oz_panel, oz_page):
    driver = selenium[browser_id]
    items = getattr(oz_page(driver)[oz_panel], '{}s'.format(item_type))
    assert item_name in items, \
        'no {} named "{}" found in {} oz panel'.format(item_type, item_name,
                                                       oz_panel)


@wt(parsers.re('user of (?P<browser_id>.+?) sees that (?P<item_type>provider) '
               'named "(?P<item_name>.+?)" has disappeared from expanded '
               '"(?P<oz_panel>GO TO YOUR FILES)" Onezone panel'))
@wt(parsers.re('user of (?P<browser_id>.+?) sees that there is no '
               '(?P<item_type>provider) named "(?P<item_name>.+?)" '
               'in expanded "(?P<oz_panel>GO TO YOUR FILES)" Onezone panel'))
@wt(parsers.re('user of (?P<browser_id>.+?) sees that (?P<item_type>space) '
               'named "(?P<item_name>.+?)" has disappeared from expanded '
               '"(?P<oz_panel>DATA SPACE MANAGEMENT)" Onezone panel'))
@wt(parsers.re('user of (?P<browser_id>.+?) sees that there is no '
               '(?P<item_type>space) named "(?P<item_name>.+?)" in expanded '
               '"(?P<oz_panel>DATA SPACE MANAGEMENT)" Onezone panel'))
@wt(parsers.re('user of (?P<browser_id>.+?) sees that (?P<item_type>group) '
               'named "(?P<item_name>.+?)" has disappeared from expanded '
               '"(?P<oz_panel>GROUP MANAGEMENT)" Onezone panel'))
@wt(parsers.re('user of (?P<browser_id>.+?) sees that there is no '
               '(?P<item_type>group) named "(?P<item_name>.+?)" in expanded '
               '"(?P<oz_panel>GROUP MANAGEMENT)" Onezone panel'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_there_is_no_item_named_in_oz_panel_list(selenium, browser_id,
                                                   item_type, item_name,
                                                   oz_panel, oz_page, hosts):
    driver = selenium[browser_id]
    if item_type == 'provider':
        item_name = hosts[item_name]['name']
    items = {item.name for item in getattr(oz_page(driver)[oz_panel],
                                           '{}s'.format(item_type))}
    assert item_name not in items, \
        ('{} named "{}" found in {} oz panel while it should not be '
         'found'.format(item_type, item_name, oz_panel))


@wt(parsers.re(r'user of (?P<browser_id>.+?) sees that '
               r'(?P<counter_type>space)s counter for (?P<item_type>provider) '
               r'"(?P<item_name>.+?)" displays (?P<number>\d+) in expanded '
               r'"(?P<oz_panel>GO TO YOUR FILES)" Onezone panel'))
@wt(parsers.re(r'user of (?P<browser_id>.+?) sees that '
               r'(?P<counter_type>provider)s counter for (?P<item_type>space) '
               r'named "(?P<item_name>.+?)" displays (?P<number>\d+) '
               r'in expanded "(?P<oz_panel>DATA SPACE MANAGEMENT)" '
               r'Onezone panel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_item_counter_match_given_num(selenium, browser_id, counter_type,
                                        item_type, item_name, number,
                                        oz_panel, oz_page, hosts):
    driver = selenium[browser_id]
    if item_type == 'provider':
        item_name = hosts[item_name]['name']
    items = getattr(oz_page(driver)[oz_panel], '{}s'.format(item_type))
    item = items[item_name]
    item_counter = int(getattr(item, '{}s_count'.format(counter_type)))

    msg = 'expected {counter_type}s number {num} does not match ' \
          'displayed {counter_type}s counter {displayed} ' \
          'for {type} named "{name}"'
    assert item_counter == int(number), msg.format(type=item_type,
                                                   name=item_name,
                                                   counter_type=counter_type,
                                                   displayed=item_counter,
                                                   num=number)


@wt(parsers.re(r'user of (?P<browser_id>.+?) sees that '
               r'(?P<counter_type>space)s counter for "(?P<item_name>.+?)" '
               r'match number of displayed  supported spaces in expanded '
               r'submenu of given (?P<item_type>provider) in expanded '
               r'"(?P<oz_panel>GO TO YOUR FILES)" Onezone panel'))
@wt(parsers.re(r'user of (?P<browser_id>.+?) sees that '
               r'(?P<counter_type>provider)s '
               r'counter for "(?P<item_name>.+?)" match number of displayed '
               r'supporting providers in expanded submenu '
               r'of given (?P<item_type>space) in expanded '
               r'"(?P<oz_panel>DATA SPACE MANAGEMENT)" Onezone panel'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_number_of_items_match_items_counter(selenium, browser_id, item_name,
                                               item_type, counter_type, oz_panel,
                                               oz_page, hosts):
    driver = selenium[browser_id]
    if item_type == 'provider':
        item_name = hosts[item_name]['name']
    items = getattr(oz_page(driver)[oz_panel], '{}s'.format(item_type))
    item = items[item_name]
    subitems = getattr(item, '{}s'.format(counter_type))
    counter = int(getattr(item, '{}s_count'.format(counter_type)))

    err_msg = ('{type}s counter number {counter} does not match displayed '
               'number of {type}s {list_len}')
    assert counter == subitems.count(), err_msg.format(type=counter_type,
                                                       counter=counter,
                                                       list_len=subitems.count())


@wt(parsers.re(r'user of (?P<browser_id>.+?) expands submenu of '
               r'(?P<item_type>provider) "(?P<item_name>.+?)" by '
               r'clicking on cloud in provider record in expanded '
               r'"(?P<oz_panel>GO TO YOUR FILES)" Onezone panel'))
@wt(parsers.re(r'user of (?P<browser_id>.+?) expands submenu of '
               r'(?P<item_type>space) named "(?P<item_name>.+?)" '
               r'by clicking on space record in expanded '
               r'"(?P<oz_panel>DATA SPACE MANAGEMENT)" Onezone panel'))
@repeat_failed(timeout=WAIT_BACKEND)
def expand_items_submenu_in_oz_panel(selenium, browser_id, item_type,
                                     item_name, oz_panel, oz_page, hosts):
    driver = selenium[browser_id]
    if item_type == 'provider':
        item_name = hosts[item_name]['name']
    items = getattr(oz_page(driver)[oz_panel], '{}s'.format(item_type))
    item = items[item_name]
    item.expand()
    err_msg = 'submenu for {type} named "{name}" has not been expanded'
    assert item.is_expanded(), err_msg.format(type=item_type, name=item_name)


@wt(parsers.re('user of (?P<browser_id>.+?) sees that there is '
               '(?P<subitem_type>provider) "(?P<subitem_name>.+?)" in '
               'submenu of (?P<item_type>space) named "(?P<item_name>.+?)" '
               'in expanded "(?P<oz_panel>DATA SPACE MANAGEMENT)" '
               'Onezone panel'))
@wt(parsers.re('user of (?P<browser_id>.+?) sees that there is '
               '(?P<subitem_type>space) named "(?P<subitem_name>.+?)" '
               'in submenu of (?P<item_type>provider) "(?P<item_name>.+?)" '
               'in expanded "(?P<oz_panel>GO TO YOUR FILES)" Onezone panel'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_item_in_submenu_of_item_in_oz_panel(selenium, browser_id, subitem_type,
                                               subitem_name, item_type, item_name,
                                               oz_panel, oz_page, hosts):
    driver = selenium[browser_id]
    if item_type == 'provider':
        item_name = hosts[item_name]['name']
    if subitem_type == 'provider':
        subitem_name = hosts[subitem_name]['name']
    items = getattr(oz_page(driver)[oz_panel], '{}s'.format(item_type))
    item = items[item_name]
    subitems = getattr(item, '{}s'.format(subitem_type))
    assert subitem_name in subitems, \
        'no "{}" found in subitems of "{}" in {}'.format(subitem_name,
                                                         item_name, oz_panel)
