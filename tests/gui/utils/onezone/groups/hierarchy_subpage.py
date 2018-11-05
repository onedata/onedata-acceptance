"""Utils to facilitate operations on groups hierarchy
subpage page in Onezone gui"""


__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label, WebElement, \
    WebItemsSequence
from selenium.webdriver import ActionChains


class Children(PageObject):
    name = id = Label('.group-name')


class GroupHierarchyPage(PageObject):
    active_group = WebElement('.group-box.active')
    trigger = WebElement('.group-box.active .group-actions-trigger')
    children_groups = WebItemsSequence('.content-groups-hierarchy .children '
                                       '.group-boxes-container .group-box',
                                       cls=Children)

    def click_trigger(self, driver):
        hover = ActionChains(driver).move_to_element(self.active_group)
        hover.perform()
        ActionChains(driver).move_to_element(self.trigger).perform()
        self.trigger.click()
