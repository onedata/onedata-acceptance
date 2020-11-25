"""Common steps for Oneprovider.
"""

__author__ = "Jakub Liput"
__copyright__ = "Copyright (C) 2016-2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from selenium.webdriver.support.ui import WebDriverWait as Wait

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.utils.generic import parse_seq
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.utils import repeat_failed


def main_menu_tab_to_url(tab):
    tab_to_url_mapping = {'shared': 'shares'}
    return tab_to_url_mapping.get(tab, tab)


def _click_on_tab_in_main_menu_sidebar(driver, tab):
    def _load_main_menu_tab_page(tab):
        def _check_url(url):
            return tab in driver.current_url

        current_url = driver.current_url
        driver.find_element_by_css_selector(css_path).click()

        return Wait(driver, WAIT_FRONTEND).until(
            lambda _: _check_url(current_url),
            message='waiting for url to change.'
                    'Current url: {:s}'.format(driver.current_url)
        )

    menu_tab = main_menu_tab_to_url(tab)
    css_path = '.primary-sidebar a#main-{:s}'.format(menu_tab)

    Wait(driver, WAIT_BACKEND).until(
        lambda _: _load_main_menu_tab_page(menu_tab),
        message='waiting for {:s} main menu tab page to load'
                ''.format(tab)
    )


@given(parsers.re('users? of (?P<browser_id_list>.*) clicked on the '
                  '"(?P<main_menu_tab>.*)" tab in main menu sidebar'))
def g_click_on_the_given_main_menu_tab(selenium, browser_id_list,
                                       main_menu_tab):
    for browser_id in parse_seq(browser_id_list):
        driver = selenium[browser_id]
        _click_on_tab_in_main_menu_sidebar(driver, main_menu_tab)


@wt(parsers.re('users? of (?P<browser_id_list>.*) clicks on the '
               '"(?P<main_menu_tab>.*)" tab in main menu sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_on_the_given_main_menu_tab(selenium, browser_id_list,
                                        main_menu_tab):
    for browser_id in parse_seq(browser_id_list):
        driver = selenium[browser_id]
        _click_on_tab_in_main_menu_sidebar(driver, main_menu_tab)


def _has_dir_content_been_loaded(driver):
    # find_element_* throws exception if nothing found
    loader = driver.find_elements_by_css_selector('#main-content '
                                                  '.loader-area-'
                                                  'content-with-'
                                                  'secondary-top')
    if loader:
        loader = loader[0]
        Wait(driver, WAIT_BACKEND).until_not(
            lambda _: loader.is_displayed(),
            message='waiting for dir content to end loading'
        )


@given(parsers.parse('user of {browser_id} sees that content of current '
                     'directory has been loaded'))
def g_has_dir_content_been_loaded(selenium, browser_id):
    driver = selenium[browser_id]
    _has_dir_content_been_loaded(driver)


@wt(parsers.parse('user of {browser_id} sees that content of current '
                    'directory has been loaded'))
def wt_has_dir_content_been_loaded(selenium, browser_id):
    driver = selenium[browser_id]
    _has_dir_content_been_loaded(driver)
