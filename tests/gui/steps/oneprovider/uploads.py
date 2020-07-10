"""This module contains gherkin steps to run acceptance tests featuring
uploads management in onezone web GUI.
"""

__author__ = "Emilia Kwolek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.conftest import WAIT_FRONTEND, WAIT_BACKEND
from tests.utils.utils import repeat_failed
from tests.utils.bdd_utils import wt, parsers


@wt(parsers.parse('user of {browser_id} sees that number of files uploaded is'
                  ' equal {number}'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_number_of_files_in_uploaded_files_list(selenium, browser_id, oz_page,
                                                  number):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    uploaded_files_list = oz_page(driver)[
        'uploads'].uploaded_content_page.uploaded_items_list
    assert int(number) == len(uploaded_files_list), (
        'number of files uploaded {}'
        'is not equal {}'.format(number, len(uploaded_files_list)))


@wt(parsers.parse(
    'user of {browser_id} sees that file "{file_name}" is uploaded'))
@repeat_failed(timeout=WAIT_BACKEND)
def assert_file_is_uploaded(selenium, browser_id, oz_page, file_name):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    item_list = oz_page(driver)[
        'uploads'].uploaded_content_page.uploaded_items_list
    assert file_name in item_list, 'searched file name not in files uploaded list'


@wt(parsers.re('user of (?P<browser_id>.*?) clicks on '
               '(?P<option>Uploads) in the main menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_uploads_in_the_sidebar(selenium, browser_id, option, oz_page):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    oz_page(driver).uploads.click()


def click_on_provider_in_uploads_sidebar_with_provider_name(selenium,
                                                            browser_id, oz_page,
                                                            provider):
    driver = selenium[browser_id]
    oz_page(driver)['uploads'].elements_list[provider].click()


@wt(parsers.parse('user of {browser_id} clicks on provider "{provider_name}" '
                  'in uploads sidebar'))
@repeat_failed(timeout=WAIT_BACKEND)
def click_on_provider_in_uploads_sidebar(selenium, browser_id, oz_page,
                                         provider_name, hosts):
    provider = hosts[provider_name]['name']
    # import pdb
    # pdb.set_trace()
    click_on_provider_in_uploads_sidebar_with_provider_name(selenium,
                                                            browser_id,
                                                            oz_page, provider)


@wt(parsers.parse('user of {browser_id} clicks on "All uploads" '
                  'in uploads sidebar'))
@repeat_failed(timeout=WAIT_BACKEND)
def click_on_all_uploads_in_uploads_sidebar_with_provider_name(selenium,
                                                               browser_id,
                                                               oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['uploads'].elements_list["All uploads"].click()
