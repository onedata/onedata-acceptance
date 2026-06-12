"""Utils for file browser and it's components in Oneprovider GUI tests"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from collections.abc import Iterator
from contextlib import contextmanager
from functools import partial
from platform import system as get_system
from typing import Protocol, cast

from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Button,
    Label,
    NamedButton,
    WebElement,
    WebItem,
)
from tests.gui.utils.generic import rm_css_cls

from ..browser import Browser
from ..browser_row import BrowserRow
from .data_row import DataRow


class FileSelector(Protocol):
    def shift_down(self) -> ActionChains: ...

    def shift_up(self) -> ActionChains: ...

    def ctrl_or_cmd_down(self) -> ActionChains: ...

    def ctrl_or_cmd_up(self) -> ActionChains: ...

    def select(self, item: BrowserRow) -> ActionChains: ...


class FileColumnHeader(PageObject):
    name = id = Label(".column-name")


class _FileBrowser(Browser):
    row_cls = DataRow
    column_header_cls = FileColumnHeader

    new_directory_button = Button(".toolbar-buttons .file-action-newDirectory")
    upload_files_button = Button(".toolbar-buttons .browser-upload")
    place_hard_link_button = Button(".toolbar-buttons .oneicon-text-link")
    place_symbolic_link_button = Button(".toolbar-buttons .oneicon-shortcut")
    selection_menu_button = Button(".one-pill-button-actions-trigger")
    paste_button = Button(".toolbar-buttons .oneicon-browser-paste")

    error_dir_msg = Label(".error-dir-text")
    navigate_root_btn = NamedButton(".btn-default", text="Navigate to root directory")

    _upload_input = WebElement(".fb-upload-trigger input")

    def __str__(self) -> str:
        return f"file browser in {self.parent}"

    def names_of_visible_elems(self) -> list[str]:
        files = self.files_list
        # make sure row is fully loaded in gui
        names = [f.text.split("\n")[0] for f in files if len(f.text.split("\n")) > 1]
        return names

    @contextmanager
    def select_files(self) -> Iterator[FileSelector]:
        ctrl_or_cmd_key = (
            Keys.COMMAND if get_system() == "Darwin" else Keys.LEFT_CONTROL
        )

        action = ActionChains(self.driver)

        action.shift_down = lambda: action.key_down(Keys.LEFT_SHIFT)
        action.shift_up = lambda: action.key_up(Keys.LEFT_SHIFT)
        action.ctrl_or_cmd_down = lambda: action.key_down(ctrl_or_cmd_key)
        action.ctrl_or_cmd_up = lambda: action.key_up(ctrl_or_cmd_key)
        action.select = lambda item: action.click(item.web_elem)

        yield cast(FileSelector, action)

        action.perform()

    def upload_files(self, files: str) -> None:
        """This interaction is very hacky, because uploading files with Selenium
        needs to use input element, but we do not use it directly in frontend.
        So we unhide an input element for a while and pass a local file path to it.
        """
        with rm_css_cls(self.driver, self._upload_input, "hidden") as elem:
            elem.send_keys(files)


FileBrowser = partial(WebItem, cls=_FileBrowser)
