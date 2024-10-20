"""Utils and fixtures to facilitate operations on archive row menu popup."""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from selenium.webdriver import ActionChains
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label, WebElement, WebItemsSequence


class Options(PageObject):
    name = id = Label(".one-label")

    def get_state(self):
        return (
            "disabled"
            if "disabled" in self.web_elem.get_attribute("class")
            else "enabled"
        )


class ArchiveRowMenu(PageObject):
    options = WebItemsSequence(
        ".left-top .file-actions.dropdown-menu li:not(.separator)", cls=Options
    )
    cancel_archivisation_elem = WebElement(".file-action-cancel")
    edit_description_elem = WebElement(".file-action-editDescription")
    delete_archive_elem = WebElement(".file-action-delete")

    def choose_option(self, name):
        if name not in self.options:
            self.scroll_to_bottom()
        self.options[name].click()

    def return_option(self, name):
        if name not in self.options:
            self.scroll_to_bottom()
        return self.options[name]

    def move_to_elem(self, driver, option):
        element = getattr(self, option + "_elem")
        try:
            ActionChains(driver).move_to_element(element).perform()
        except RuntimeError:
            self.scroll_to_bottom()
            ActionChains(driver).move_to_element(element).perform()

    def scroll_to_bottom(self):
        option_len = len(self.options)
        self.driver.execute_script(
            "arguments[0].scrollIntoView();",
            self.options[option_len - 1].web_elem,
        )

    def __str__(self):
        return "Archive row menu"
