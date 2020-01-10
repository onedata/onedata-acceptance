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
                                               Button)
from tests.gui.utils.generic import iter_ahead, rm_css_cls
from .data_row import DataRow
from .metadata_row import MetadataRow
from ..breadcrumbs import Breadcrumbs


class _FileBrowser(PageObject):
    breadcrumbs = Breadcrumbs('.fb-breadcrumbs')
    new_directory = Button('.toolbar-buttons .file-action-newDirectory')
    upload_file = Button('.toolbar-buttons .browser-upload')

    data = WebItemsSequence('.data-row.fb-table-row', cls=DataRow)

    empty_dir_msg = Label('.empty-dir-text')
    _empty_dir_icon = WebElement('.empty-dir-image')
    _files_with_metadata = WebElementsSequence('tbody tr.first-level')
    _bottom = WebElement('.file-row-load-more')

    _upload_input = WebElement('.fb-upload-trigger input')

    def __str__(self):
        return 'file browser in {}'.format(self.parent)

    def is_empty(self):
        try:
            self._empty_dir_icon
        except RuntimeError:
            return False
        else:
            return True

    def get_metadata_for(self, name):
        for item1, item2 in iter_ahead(self._files_with_metadata):
            if 'file-row' in item1.get_attribute('class'):
                if 'file-row' not in item2.get_attribute('class'):
                    if DataRow(self.driver, item1, self).name == name:
                        return MetadataRow(self.driver, item2, self)
        else:
            raise RuntimeError('no metadata row for "{name}" in {item} '
                               'found'.format(name=name, item=self))

    def scroll_to_bottom(self):
        self.driver.execute_script('arguments[0].scrollIntoView();',
                                   self._bottom)

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


FileBrowser = partial(WebItem, cls=_FileBrowser)
