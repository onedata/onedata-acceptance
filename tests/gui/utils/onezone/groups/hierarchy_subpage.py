"""Utils to facilitate operations on groups hierarchy
subpage page in Onezone gui"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from selenium.webdriver import ActionChains
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Button,
    Label,
    WebElement,
    WebItemsSequence,
)


class Group(PageObject):
    name = id = Label(".group-name")
    group = WebElement(".group-name")
    group_menu_button = WebElement(".group-box .group-actions-trigger")

    line_to_child = WebElement(".line-to-child")
    line_to_parent = WebElement(".line-to-parent")

    child_relation_menu_button = WebElement(".line-to-child .actions-trigger")
    parent_relation_menu_button = WebElement(".line-to-parent .actions-trigger")

    def click_group_menu_button(self, driver):
        ActionChains(driver).move_to_element(self.group).perform()
        self.group_menu_button.click()

    def click_relation_menu_button(self, driver, relation):
        line_to = f"line_to_{relation}"
        relation = f"{relation}_relation_menu_button"

        ActionChains(driver).move_to_element(getattr(self, line_to)).perform()
        getattr(self, relation).click()


class GroupHierarchyPage(PageObject):
    show_parent_groups = Button(".group-box.active .group-box-relation.parents")
    show_children_groups = Button(".group-box.active .group-box-relation.children")

    groups = WebItemsSequence(
        ".content-groups-hierarchy .group-boxes-container .group-box", cls=Group
    )

    children = WebItemsSequence(
        ".content-groups-hierarchy .children .group-boxes-container .group-box",
        cls=Group,
    )
    parents = WebItemsSequence(
        ".content-groups-hierarchy .parents .group-boxes-container .group-box",
        cls=Group,
    )
    hierarchy_view_menu = Button(
        ".content-groups-hierarchy .collapsible-toolbar-toggle"
    )
