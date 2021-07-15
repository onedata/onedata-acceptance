__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.utils.generic import transform
from tests.utils.bdd_utils import wt, parsers
from tests.gui.conftest import WAIT_FRONTEND
from tests.utils.utils import repeat_failed
import pdb


@wt(parsers.parse('user of {browser_id} clicks on Files in the space1 sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_the_files_in_the_left_sidebar_menu(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    oz_page(driver)['data'].elements_list['space1'].files()


@wt(parsers.parse('user of {browser_id} clicks on {item_name} options menu'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_the_first_folder_directory_menu(selenium, browser_id, tmp_memory, item_name,
                               op_container):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    iframe = driver.find_element_by_tag_name('iframe')
    driver.switch_to.frame(iframe)

    browser = 'file browser'

    items_browser = op_container(driver).file_browser
    tmp_memory[browser_id][transform(browser)] = items_browser

    items_browser.data[item_name].menu_button()


@wt(parsers.parse('user of {browser_id} clicks on the share option in the '
                  'popover menu in dir2'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_share_in_the_toolbar_menu(selenium, browser_id, popups):
    driver = selenium[browser_id]
    popups(driver).toolbar.options['Share']()


@wt(parsers.parse('user of {browser_id} clicks on the create button in the '
                  'modal window'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_create_in_modal_of_share_directory(selenium, browser_id, modals):
    driver = selenium[browser_id]
    modals(driver).share_directory.create()


@wt(parsers.parse('user of {browser_id} clicks on the close button in the '
                  'second '
                  'modal window'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_close_in_modal_of_share_continue(selenium, browser_id, modals):
    driver = selenium[browser_id]
    modals(driver).share_directory.close()


@wt(parsers.parse('user of {browser_id} clicks on {item_name} options menu to '
                  'make symbolic link'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_the_second_folder_directory_menu(selenium, browser_id, tmp_memory, item_name,
                               op_container):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    iframe = driver.find_element_by_tag_name('iframe')
    driver.switch_to.frame(iframe)

    browser = 'file browser'

    items_browser = op_container(driver).file_browser
    tmp_memory[browser_id][transform(browser)] = items_browser

    items_browser.data[item_name].menu_button()


@wt(parsers.parse('user of {browser_id} clicks on the share option in the '
                  'popover menu in dir1'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_symlink_in_the_toolbar_menu(selenium, browser_id, popups):
    driver = selenium[browser_id]
    popups(driver).toolbar.options['Create symbolic link']()


@wt(parsers.parse('user of {browser_id} doubleclicks on the {item_name} to '
                  'enter it'))
@repeat_failed(timeout=WAIT_FRONTEND)
def enter_the_shared_folder(selenium, browser_id, tmp_memory, item_name,
                               op_container):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    iframe = driver.find_element_by_tag_name('iframe')
    driver.switch_to.frame(iframe)

    browser = 'file browser'

    items_browser = op_container(driver).file_browser
    tmp_memory[browser_id][transform(browser)] = items_browser

    items_browser.data[item_name].double_click()


@wt(parsers.parse('user of {browser_id} clicks on the place_the_symbolic_link '
                  'button in the top right corner'))
@repeat_failed(timeout=WAIT_FRONTEND)
def place_symlink_in_the_shared_folder(selenium, browser_id, tmp_memory, op_container):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    iframe = driver.find_element_by_tag_name('iframe')
    driver.switch_to.frame(iframe)

    browser = 'file browser'

    items_browser = op_container(driver).file_browser
    tmp_memory[browser_id][transform(browser)] = items_browser

    items_browser.symlink_button()


@wt(parsers.parse('user of {browser_id} clicks on the shares button in the '
                  'left sidebar'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_the_shares_in_the_left_sidebar(selenium, browser_id, oz_page):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    oz_page(driver)['data'].elements_list['space1'].shares()


@wt(parsers.parse('user of {browser_id} clicks on the {item_name} button to '
                  'enter it in shares browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_the_shared_folder_in_shares_browser(selenium, browser_id, tmp_memory, op_container,
                               item_name, oz_page):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    iframe = driver.find_element_by_tag_name('iframe')
    driver.switch_to.frame(iframe)

    browser = 'shares browser'

    items_browser = op_container(driver).shares_page
    tmp_memory[browser_id][transform(browser)] = items_browser

    items_browser.shares_browser[item_name].click()


@wt(parsers.parse('user of {browser_id} doubleclicks on the {item_name} '
                  'button in the item browser in shares page'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_the_shared_folder_in_files__browser(selenium, browser_id, tmp_memory, op_container,
                               item_name):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    iframe = driver.find_element_by_tag_name('iframe')
    driver.switch_to.frame(iframe)

    browser = 'shares browser'

    items_browser = op_container(driver).shares_page
    tmp_memory[browser_id][transform(browser)] = items_browser

    items_browser.file_browser.data[item_name].double_click()


@wt(parsers.parse('user of {browser_id} sees error icon in the share_browser'))
@repeat_failed(timeout=WAIT_FRONTEND)
def check_the_icon_of_shared_directory(selenium, browser_id, tmp_memory, op_container,
                               ):
    driver = selenium[browser_id]
    driver.switch_to.default_content()
    iframe = driver.find_element_by_tag_name('iframe')
    driver.switch_to.frame(iframe)

    browser = 'shares browser'

    items_browser = op_container(driver).shares_page
    tmp_memory[browser_id][transform(browser)] = items_browser

    assert  items_browser.file_browser.data['dir1'].is_symbolic_link_invalid(), f'icon not found'
