"""This module contains gherkin steps to run acceptance tests featuring
public shares interface in oneprovider web GUI.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import wt, parsers

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.utils.utils import repeat_failed


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
    iframe = driver.find_element_by_tag_name('iframe')
    driver.switch_to.frame(iframe)


@wt(parsers.parse('user of {browser_id} sees that '
                  'public share is named "{share_name}"'))
@repeat_failed(timeout=WAIT_BACKEND, interval=0.5)
def assert_public_share_named(selenium, browser_id, share_name, public_share):
    _change_iframe_for_public_share_page(selenium, browser_id)
    displayed_name = public_share(selenium[browser_id]).name
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

    assert expected_msg == file_browser.error_dir_msg, (f'Displayed empty dir '
                                            f'msg '
                                            f'"{file_browser.error_dir_msg}" '
                                            f'does not match '
                                            f'expected one "{expected_msg}"')


@wt(parsers.parse('user of {browser_id} sees "{error_msg}" error'))
@repeat_failed(timeout=WAIT_FRONTEND)
def no_public_share_view(selenium, browser_id, error_msg, public_share):
    error_msg = error_msg.upper()
    driver = selenium[browser_id]

    assert error_msg == public_share(driver).share_not_found, (
        f'displayed error msg does not contain {error_msg}')


@wt(parsers.parse('user of {browser_id} opens description tab '
                  'on share\'s public interface'))
@repeat_failed(timeout=WAIT_FRONTEND)
def open_description_tab_in_public_share(selenium, browser_id, public_share):
    driver = selenium[browser_id]
    _change_iframe_for_public_share_page(selenium, browser_id)
    public_share(driver).description_tab()


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
