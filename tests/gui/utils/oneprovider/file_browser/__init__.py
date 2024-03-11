"""Utils for file browser and it's components in Oneprovider GUI tests
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from functools import partial
from contextlib import contextmanager

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (WebElement, WebElementsSequence,
                                               Label, WebItemsSequence, WebItem,
                                               Button, Input)
from tests.gui.utils.generic import iter_ahead, rm_css_cls
from .data_row import DataRow
from ..breadcrumbs import Breadcrumbs
from ...core import scroll_to_css_selector


class FileColumnHeader(PageObject):
    name = id = Label('.column-name')


class _FileBrowser(PageObject):
    breadcrumbs = Breadcrumbs('.fb-breadcrumbs')
    new_directory_button = Button('.toolbar-buttons .file-action-newDirectory')
    upload_files_button = Button('.toolbar-buttons .browser-upload')
    refresh_button = Button('.toolbar-buttons .file-action-refresh')
    place_hard_link_button = Button('.toolbar-buttons .oneicon-text-link')
    place_symbolic_link_button = Button('.toolbar-buttons .oneicon-shortcut')
    selection_menu_button = Button('.one-pill-button-actions-trigger')
    paste_button = Button('.toolbar-buttons .oneicon-browser-paste')

    data = WebItemsSequence('.data-row.fb-table-row', cls=DataRow)
    _data = WebElementsSequence('.data-row.fb-table-row')

    browser_msg_header = Label('.content-info-content-container h1')
    empty_dir_msg = Label('.empty-dir-text')
    _empty_dir_icon = WebElement('.empty-dir-image')
    _bottom_of_visible_fragment = WebElement('.table-bottom-spacing')
    error_dir_msg = Label('.error-dir-text')

    _upload_input = WebElement('.fb-upload-trigger input')
    header = WebElement('.file-browser-head-container')
    jump_input = Input('.jump-input')

    configure_columns = Button('.columns-configuration-button')
    column_headers = WebItemsSequence(
        '.fb-table-head-row .fb-table-secondary-col', cls=FileColumnHeader)

    def __str__(self):
        return 'file browser in {}'.format(self.parent)

    def is_empty(self):
        try:
            self._empty_dir_icon
        except RuntimeError:
            return False
        else:
            return True

    def scroll_visible_fragment(self):
        self.driver.execute_script('arguments[0].scrollTo(arguments[1]);',
                                   self.web_elem,
                                   self._bottom_of_visible_fragment)

    def click_header(self):
        action = ActionChains(self.driver)
        action.click(self.header).perform()

    def scroll_one_file_down(self):
        action = ActionChains(self.driver)
        action.key_down(Keys.DOWN).key_down(Keys.DOWN).perform()

    def names_of_visible_elems(self):
        files = self._data
        # make sure row is fully loaded in gui
        names = [f.text.split('\n')[0] for f in files
                 if len(f.text.split('\n')) > 1]
        return names

    @contextmanager
    def select_files(self):
        from platform import system as get_system

        ctrl_or_cmd_key = \
            Keys.COMMAND if get_system() == 'Darwin' else Keys.LEFT_CONTROL

        action = ActionChains(self.driver)

        action.shift_down = lambda: action.key_down(Keys.LEFT_SHIFT)
        action.shift_up = lambda: action.key_up(Keys.LEFT_SHIFT)
        action.ctrl_or_cmd_down = lambda: action.key_down(ctrl_or_cmd_key)
        action.ctrl_or_cmd_up = lambda: action.key_up(ctrl_or_cmd_key)
        action.select = lambda item: action.click(item.web_elem)

        yield action

        action.perform()

    def upload_files(self, files):
        """This interaction is very hacky, because uploading files with Selenium
        needs to use input element, but we do not use it directly in frontend.
        So we unhide an input element for a while and pass a local file path to it.
        """
        with rm_css_cls(self.driver, self._upload_input, 'hidden') as elem:
            elem.send_keys(files)

    def click_on_background(self):
        ActionChains(self.driver).move_to_element_with_offset(
            self.header, 0, 0).click().perform()

    def scroll_to_top(self):
        self.driver.execute_script(
            "document.querySelector('.perfect-scrollbar-element.ps--active-y')"
            ".scrollTo(0, 0)")

    def get_css_selector(self):
        css_selector = self.web_elem.get_attribute('class')
        css_selector = css_selector.replace(' ', '.')
        css_selector = '.' + css_selector
        return css_selector

    def scroll_to_number_file(self, driver, number, browser):
        selector = (browser.get_css_selector() + ' ' +
                    f'.data-row:nth-of-type({number})')
        scroll_to_css_selector(driver, selector)


FileBrowser = partial(WebItem, cls=_FileBrowser)
