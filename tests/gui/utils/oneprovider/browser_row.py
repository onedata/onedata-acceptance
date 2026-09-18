"""Utils and fixtures to facilitate operation on file row in file, dataset
and archive browsers in oneprovider web GUI.
"""

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver

from tests.gui.utils.core.base import NamedElement
from tests.gui.utils.core.web_elements import Button, Label, WebElement
from tests.gui.utils.generic import click_on_web_elem, transform
from tests.utils.utils import element_has_class


class BrowserRow(NamedElement):
    first_column = WebElement(".fb-table-col-files", scroll=False)
    name = id = Label(".file-name-inner", scroll=False)
    clickable_field = WebElement(".file-name", scroll=False)
    menu_button = Button(".file-row-actions-trigger", scroll=False)
    description = Label(".secondary-description", scroll=False)
    _status_tag = WebElement(".file-status-tag")
    _icon = WebElement(".file-icon")
    _icon_tag = WebElement(".one-icon-tag")

    def is_selected(self) -> bool:
        return element_has_class(self.web_elem, "file-selected")

    def is_highlighted(self) -> bool:
        return element_has_class(self.first_column, "animate-attention")

    def is_file(self) -> bool:
        return element_has_class(self.web_elem, "fb-table-row-file")

    def is_directory(self) -> bool:
        return element_has_class(self.web_elem, "fb-table-row-dir")

    def wait_for_selected(self) -> None:
        for _ in range(30):
            time.sleep(0.1)
            if self.is_selected():
                return

        raise TimeoutError("Waited too long for being selected")

    def click_and_enter(self) -> None:
        time.sleep(0.1)
        ActionChains(self.driver).click(self.clickable_field).perform()
        self.wait_for_selected()
        ActionChains(self.driver).key_down(Keys.ENTER).perform()

    def click(self) -> None:
        ActionChains(self.driver).click(self.clickable_field).perform()
        self.wait_for_selected()

    def get_tag_text(self, name: str) -> str:
        return getattr(self, f"{transform(name)}_tag").text

    def click_on_status_tag(self, name: str) -> None:
        tag = getattr(self, f"{name.lower()}_tag")
        click_on_web_elem(self.driver, tag, f'cannot click on "{name}" in {self}')

    def hover_to_btn_and_click(self, btn_name: str, driver: WebDriver) -> None:
        btn = getattr(self, btn_name)
        ActionChains(driver).move_to_element(btn.web_elem).click(btn.web_elem).perform()

    def is_tag_visible(self, name: str) -> bool:
        try:
            getattr(self, f"{transform(name)}_tag")
        except NoSuchElementException:
            return False
        return True
