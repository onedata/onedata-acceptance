"""Utils to facilitate common operations on clusters sidebar."""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)


from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Input,
    Label,
    NamedButton,
    WebElement,
    WebItemsSequence,
)
from tests.gui.utils.core.web_objects import ButtonWithTextPageObject


class WelcomePage(PageObject):
    create_new_cluster = NamedButton("button", text="Create new cluster")
    create_onezone_cluster = NamedButton(
        ".btn-primary", text="Create Onezone cluster"
    )
    create_oneprovider_cluster = NamedButton(
        ".btn-primary", text="Create Oneprovider cluster"
    )


class ClusterRecord(ButtonWithTextPageObject):
    name = id = Label(
        ".item-header .one-label .item-name", parent_name="clusters sidebar"
    )
    id_hash = Label(".item-header .one-label .conflict-part")
    submenu = WebItemsSequence(
        "ul.one-list-level-2 li", cls=ButtonWithTextPageObject
    )
    status_icon = WebElement(".sidebar-item-icon")

    def __str__(self):
        return f"{self.name} item in {self.parent}"

    def is_not_working(self):
        return "error" in self.status_icon.get_attribute("class")


class ClustersSidebar(PageObject):
    search_box = Input("ul.one-list li.search-bar-item input")
    items = WebItemsSequence(
        ".sidebar-clusters ul.one-list li.one-list-item.resource-item",
        cls=ClusterRecord,
    )

    def scroll_to_bottom(self, driver):
        driver.execute_script(
            "var s = $('#col-sidebar'); s.scrollTo(s.height())"
        )

    def get_all_items(self, driver):
        self.scroll_to_bottom(driver)
        return self.items
