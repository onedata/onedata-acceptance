"""Utils to facilitate operations on pages in Onezone gui"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from collections.abc import Iterable
from typing import ClassVar

from tests.gui.utils.common.constants import WAIT_FRONTEND
from tests.gui.utils.core.base import NamedElement, PageObject, PageObjectMeta
from tests.gui.utils.core.web_elements import Label, NamedButton
from tests.gui.utils.generic import ListItemMainField, PageName
from tests.utils.utils import repeat_failed


@repeat_failed(timeout=WAIT_FRONTEND)
def get_visible_elements_list[T: NamedElement](
    elements_list: Iterable[T],
    main_field: ListItemMainField = "name",
) -> list[T]:
    return [element for element in elements_list if getattr(element, main_field)]


class GenericPage(PageObject, metaclass=PageObjectMeta):
    name = id = Label(".row-heading .col-title")
    get_started = NamedButton(".btn-default", text="Get started")


class ListPage(PageObject):
    """
    Base class for Onezone pages exposing one or more element lists.
    This class is basically needed for function get_visible_items_list
    """


class SidebarPanelPage(GenericPage, ListPage):
    panel_name: ClassVar[PageName]
