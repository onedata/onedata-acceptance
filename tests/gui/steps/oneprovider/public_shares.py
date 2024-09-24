"""This module contains gherkin steps to run acceptance tests featuring
public shares interface in oneprovider web GUI.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.utils.generic import transform, parse_seq
from tests.utils.bdd_utils import wt, parsers

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.utils.utils import repeat_failed

from selenium.webdriver.common.by import By


@wt(parsers.parse('user of {browser_id} changes current working directory '
                  'to {path} using breadcrumbs on share\'s public interface'))
@repeat_failed(timeout=WAIT_FRONTEND)
def change_public_share_cwd_using_breadcrumbs(selenium, browser_id, path,
                                              public_share):
    public_share(selenium[browser_id]).breadcrumbs.chdir(path)


@wt(parsers.parse('user of {browser_id} changes current working '
                  'directory to current share using breadcrumbs on '
                  'share\'s '
                  'public interface'))
@repeat_failed(timeout=WAIT_FRONTEND)
def change_public_share_to_home_cwd_using_breadcrumbs(selenium, browser_id,
                                                      public_share):
    public_share(selenium[browser_id]).breadcrumbs.home.click()


def _change_iframe_for_public_share_page(selenium, browser_id):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    iframe = driver.find_element(By.TAG_NAME, 'iframe')
    driver.switch_to.frame(iframe)


@wt(parsers.parse('user of {browser_id} sees that '
                  'public share is named "{share_name}"'))
@repeat_failed(timeout=WAIT_BACKEND, interval=0.5)
def assert_public_share_named(selenium, browser_id, share_name, public_share):
    _change_iframe_for_public_share_page(selenium, browser_id)
    displayed_name = public_share(selenium[browser_id]).share_name
    assert displayed_name == share_name, (f'displayed public share name '
                                          f'is "{displayed_name}" instead of '
                                          f'expected "{share_name}"')


@wt(parsers.parse('user of {browser_id} sees that current working directory '
                  'path visible in share\'s public interface file browser '
                  'is as follows: {cwd}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def is_public_share_cwd_correct(selenium, browser_id, cwd, public_share):
    displayed_cwd = public_share(selenium[browser_id]).breadcrumbs.pwd()
    assert displayed_cwd == cwd, (f'displayed share cwd in file browser'
                                  f' is {displayed_cwd} '
                                  f'instead of expected {cwd}')


@wt(parsers.parse('user of {browser_id} sees file browser '
                  'on share\'s public interface'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_file_browser_in_public_share(selenium, browser_id, public_share,
                                        tmp_memory):
    file_browser = public_share(selenium[browser_id]).file_browser
    tmp_memory[browser_id]['file_browser'] = file_browser


@wt(parsers.parse('user of {browser_id} sees "{expected_msg}" sign in the '
                  'file browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_empty_file_browser_in_public_share(selenium, browser_id, tmp_memory,
                                              public_share, expected_msg):
    file_browser = public_share(selenium[browser_id]).file_browser
    tmp_memory[browser_id]['file_browser'] = file_browser

    assert expected_msg == file_browser.error_dir_msg, (
        f'Displayed empty dir msg "{file_browser.error_dir_msg}" does not '
        f'match expected one "{expected_msg}"')


@wt(parsers.parse('user of {browser_id} sees "{error_msg}" error'))
@repeat_failed(timeout=WAIT_FRONTEND)
def no_public_share_view(selenium, browser_id, error_msg, public_share):
    error_msg = error_msg.upper()
    driver = selenium[browser_id]

    assert error_msg == public_share(driver).share_not_found, (
        f'displayed error msg does not contain {error_msg}')


@wt(parsers.parse('user of {browser_id} sees "{description}" description '
                  'on share\'s public interface'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_proper_description(selenium, browser_id,
                              description, public_share):
    driver = selenium[browser_id]
    _change_iframe_for_public_share_page(selenium, browser_id)

    description_on_page = public_share(driver).description
    err_msg = f'found {description_on_page} instead of {description}'
    assert description_on_page == description, err_msg


@wt(parsers.parse('user of {browser_id} sees "{message}" '
                  'instead of file browser on share\'s public interface'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_message_no_file_browser(selenium, browser_id, message, public_share):
    driver = selenium[browser_id]
    _change_iframe_for_public_share_page(selenium, browser_id)
    msg = public_share(driver).no_files_message_header
    assert msg == message, f'{message} not on share\'s public interface'


@wt(parsers.parse('user of {browser_id} clicks share link type selector '
                  'on share\'s public interface'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_public_share_link_type_selector(selenium, browser_id, public_share):
    public_share(selenium[browser_id]).link_type_selector()


@wt(parsers.parse('user of {browser_id} chooses "{url_type}" share link type '
                  'on share\'s public interface'))
@repeat_failed(timeout=WAIT_FRONTEND)
def choose_public_share_link_type(selenium, browser_id, url_type, public_share):
    driver = selenium[browser_id]
    type_popup = public_share(driver).url_type_popup
    getattr(type_popup, transform(url_type))()


@wt(parsers.parse('user of {browser_id} copies public REST endpoint '
                  'on share\'s public interface'))
@repeat_failed(timeout=WAIT_FRONTEND)
def copy_public_share_link(selenium, browser_id, public_share):
    public_share(selenium[browser_id]).copy_icon()


@wt(parsers.re('user of (?P<browser_id>.*) opens "(?P<tab>.*)" tab on share\'s'
               ' (public|private) interface'))
@repeat_failed(timeout=WAIT_FRONTEND)
def open_tab_in_public_share(selenium, browser_id, public_share, tab):
    tab = transform(tab) + '_tab'
    driver = selenium[browser_id]
    _change_iframe_for_public_share_page(selenium, browser_id)
    getattr(public_share(driver), tab)()


@wt(parsers.re('user of (?P<browser_id>.*) sees "(?P<tab_name>.*)" tab '
               'on share\'s (public|private) interface'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_tab_in_public_share(selenium, browser_id, tab_name):
    tab_name = transform(tab_name)
    driver = selenium[browser_id]
    _change_iframe_for_public_share_page(selenium, browser_id)
    tabs = driver.find_elements(By.CSS_SELECTOR, '.nav-tabs-share-mode li')
    for tab in tabs:
        if transform(tab.text) == tab_name:
            err_msg = f'tab {tab_name} is not active'
            assert 'active' in tab.get_attribute('class'), err_msg
            return
    raise AssertionError(f'did not manage to find tab {tab_name}')


@wt(parsers.re('user of (?P<browser_id>.*) clicks "(?P<button>.*)" button on '
               'share\'s (?P<option>public|private) interface'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_button_in_share(selenium, browser_id, public_share, private_share,
                          button, option):
    driver = selenium[browser_id]
    if option == 'public':
        getattr(public_share(driver), transform(button))()
    else:
        getattr(private_share(driver), transform(button))()


def check_item_presence_in_dublin_core_metadata(item, data):
    for info in data:
        if info.text == item:
            break
    else:
        raise Exception(f'{item} was not found in "Dublin Core Metadata"')


@wt(parsers.re('user of (?P<browser_id>.*?) sees that (?P<which>.*?) (is|are) '
               '(?P<data>.*?) in "Dublin Core Metadata" on share\'s '
               '(public|private) interface'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_data_in_dublin_core_metadata(browser_id, data, selenium,
                                        public_share):
    driver = selenium[browser_id]
    dublin_core = public_share(driver).dublin_core_metadata_data

    for item in parse_seq(data):
        check_item_presence_in_dublin_core_metadata(item, dublin_core)


@wt(parsers.re('user of (?P<browser_id>.*?) copies "(?P<link>.*?)" from'
               ' share\'s (public|private) interface'))
@repeat_failed(timeout=WAIT_FRONTEND)
def copies_link_in_shares_interface(browser_id, selenium, public_share):
    driver = selenium[browser_id]
    public_share(driver).copy_link()


@wt(parsers.re('user of (?P<browser_id>.*?) sees that XML data contains '
               '(?P<data>.*?) on share\'s (public|private) interface'))
def assert_xml_data_in_shares(selenium, browser_id, data, public_share):
    driver = selenium[browser_id]
    xml_data = public_share(driver).xml_data
    for item in parse_seq(data):
        assert item in xml_data, (f'{item} not in XML data on share\'s public '
                                  f'interface')
