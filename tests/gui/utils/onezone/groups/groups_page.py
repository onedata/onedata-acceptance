"""Utils to facilitate operations on groups page in Onezone gui"""

__author__ = "Michal Stanisz, Lukasz Niemiec"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)


from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Button,
    Input,
    Label,
    NamedButton,
    WebItem,
    WebItemsSequence,
)
from tests.gui.utils.onezone.common import EditBox, InputBox
from tests.gui.utils.onezone.generic_page import Element, GenericPage
from tests.gui.utils.onezone.members_subpage import MembersPage

from .hierarchy_subpage import GroupHierarchyPage


class Group(Element):
    menu = Button(".collapsible-toolbar-toggle")
    members = NamedButton(".one-list-level-2 .item-header", text="Members")
    hierarchy = NamedButton(".one-list-level-2 .item-header", text="Hierarchy")
    edit_box = WebItem(".name-editor", cls=EditBox)


class GroupDetailsPage(PageObject):
    members = WebItem(".content-groups-members", cls=MembersPage)
    hierarchy = WebItem(".content-groups-hierarchy", cls=GroupHierarchyPage)
    error_label = Label(".text-center div h1")
    bulk_edit = NamedButton("button", text="Bulk edit")
    error_header = Label(".content-info-content-container h1")


class MenuItem(PageObject):
    name = id = Label("a.clickable")

    def __call__(self):
        self.click()


class GroupsPage(GenericPage):
    elements_list = WebItemsSequence(
        ".sidebar-groups .one-list>.one-list-item.clickable", cls=Group
    )

    create_group = Button(".create-group-btn")

    menu = WebItemsSequence(
        ".webui-popover-content "
        ".one-collapsible-toolbar-popover "
        ".dropdown-menu .one-collapsible-toolbar-item",
        cls=MenuItem,
    )

    group_search_bar = Input(".one-sidebar li.one-list-item.search-bar-item")

    input_box = WebItem(".content-info-content-container", cls=InputBox)

    main_page = WebItem(".col-content", cls=GroupDetailsPage)
    members_page = WebItem(".main-content", cls=MembersPage)

    selected_group_name = Label(".sidebar-groups .active .one-label .item-name")
