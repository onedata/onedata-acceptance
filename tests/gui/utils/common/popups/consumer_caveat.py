"""Utils and fixtures to facilitate operations on consumer caveat popup."""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.types import GuiObject
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Button,
    Input,
    Label,
    WebElement,
    WebItemsSequence,
)
from tests.utils.utils import repeat_failed


class TypeItem(PageObject):
    name = id = Label(".text")

    def __call__(self) -> None:
        self.web_elem.click()

    def __str__(self) -> str:
        return f"Consumer type item with text {self.name}"


class Consumer(PageObject):
    name = id = Label(".tag-label")

    def __call__(self) -> None:
        self.click()

    def __str__(self) -> str:
        return "Consumer item"


class ConsumerCaveat(PageObject):
    list_option = Button(".btn-list")
    id_option = Button(".btn-by-id")
    consumer_type = WebElement(".ember-basic-dropdown-trigger--in-place")
    consumer_types = WebItemsSequence(".ember-power-select-option", cls=TypeItem)
    consumers = WebItemsSequence(".selector-list .selector-item", cls=Consumer)
    input = Input(".record-id")
    add_button = Button(".add-id")

    user_consumer = Button(".option-container .oneicon-user")
    group_consumer = Button(".option-container .oneicon-groups")
    oneprovider_consumer = Button(".option-container .oneicon-provider")

    def expand_consumer_types(self) -> None:
        self.consumer_type.click()

    def __str__(self) -> str:
        return "Consumer caveat popup"

    @repeat_failed(timeout=20)
    def select_type(self, consumer_type: GuiObject) -> None:
        button = getattr(self, f"{consumer_type}_consumer")
        button()
