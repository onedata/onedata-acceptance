"""Utils and fixtures to facilitate operations on consumer caveat popup."""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from collections.abc import Callable
from typing import TYPE_CHECKING

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait

from tests.gui.constants import WAIT_FRONTEND
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Button,
    Input,
    Label,
    WebElement,
    WebItemsSequence,
)

if TYPE_CHECKING:
    from tests.gui.utils.onezone.token_caveats import CaveatField
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
        self.wait_for_consumer_types_state(is_open=True)

    @repeat_failed(timeout=WAIT_FRONTEND)
    def wait_for_consumer_types_state(self, is_open: bool) -> None:
        assert (len(self.consumer_types) > 0) == is_open, (
            f"Consumer types dropdown in {self} did not {'open' if is_open else 'close'}"
        )

    @repeat_failed(timeout=WAIT_FRONTEND)
    def choose_exact_consumer_value(
        self, get_caveat_field: Callable[[], "CaveatField"], consumer_value: str
    ) -> None:
        caveat_field = get_caveat_field()
        if consumer_value in caveat_field.tags:
            return
        self.expand_consumers()
        try:
            consumer = self.consumers[consumer_value]
        except KeyError as exc:
            raise ValueError(f"Consumer with value {consumer_value!r} not found in {self}") from exc

        consumer.click()
        WebDriverWait(self.driver, 1).until(
            lambda _: consumer_value in get_caveat_field().tags,
            message=f"Consumer {consumer_value!r} was not selected",
        )

    def select_consumer_type(self, consumer_type: str) -> None:
        self.choose_consumer_type(consumer_type)
        self.wait_for_consumer_types_state(is_open=False)

    @repeat_failed(timeout=WAIT_FRONTEND)
    def choose_consumer_type(self, consumer_type: str) -> None:
        self.consumer_types[consumer_type].click()

    def expand_consumers(self) -> None:
        # only try to expand if no consumer loaded within 1 second
        try:
            WebDriverWait(self.driver, 1).until(lambda _: len(self.consumers) > 0)
        except TimeoutException:
            self.list_option.click()
            self.wait_for_consumers_to_load()

    def are_all_consumers_loaded(self) -> bool:
        return len(self.consumers) > 0 and all(consumer.name for consumer in self.consumers)

    @repeat_failed(timeout=WAIT_FRONTEND)
    def wait_for_consumers_to_load(self) -> None:
        assert self.are_all_consumers_loaded(), (
            f"Consumers in {self} did not load properly, got: {self.consumers}"
        )

    @repeat_failed(timeout=20)
    def select_type(self, consumer_type: str) -> None:
        button = getattr(self, f"{consumer_type}_consumer")
        button.click()

    def __str__(self) -> str:
        return "Consumer caveat popup"
