"""Utils and fixtures to facilitate operations on menu popup.
"""

__author__ = "Wojciech Szmelich"
__copyright__ = "Copyright (C) 2024 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label, WebItemsSequence
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


class MenuItem(PageObject):
    name = id = Label('.tag-label')

    def __call__(self):
        self.click()


class OptionsSelector(PageObject):
    menu = WebItemsSequence('.selector-item', cls=MenuItem)

    def __str__(self):
        return 'Options selector'

    def choose_option(self, name):
        self.hover_over()
        # max number of elements in popup list
        for _ in range(30):
            for item in self.menu:
                if item.name.lower() == name:
                    self.menu[item.name].click()
                    return
            self.scroll_down()
        raise RuntimeError(f'item {name} not found in popup')

    def hover_over(self):
        ActionChains(self.driver).move_to_element(
            self.menu[0].web_elem).perform()

    def scroll_down(self):
        ActionChains(self.driver).key_down(Keys.DOWN).perform()
