"""Utils and fixtures to facilitate operations on consumer caveat popup."""

from __future__ import annotations

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
    TransformedLabel,
    WebElement,
    WebItemsSequence,
)
from tests.gui.utils.text import transform

if TYPE_CHECKING:
    from tests.gui.utils.onezone.token_caveats import CaveatField
from tests.gui.utils.generic import perform_action
from tests.gui.utils.web_elem_utils import wait_for_visible_element_using_getter
from tests.utils.utils import repeat_failed


class TypeItem(PageObject):
    name = id = TransformedLabel(".text")

    def __call__(self) -> None:
        self.web_elem.click()

    def __str__(self) -> str:
        return f"Consumer type item with text {self.name}"


class Consumer(PageObject):
    name = id = TransformedLabel(".tag-label")

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

    def expand_consumer_types(self) -> None:
        self.consumer_type.click()
        self.wait_for_consumer_types_state(is_open=True)

    def wait_for_consumer_types_state(self, is_open: bool) -> None:
        WebDriverWait(self.driver, WAIT_FRONTEND).until(
            lambda _: (len(self.consumer_types) > 0) == is_open,
            message=f"Consumer types dropdown in {self} did not {'open' if is_open else 'close'}",
        )

    def choose_exact_consumer_value(
        self, get_caveat_field: Callable[[], CaveatField], consumer_value: str
    ) -> None:
        caveat_field: CaveatField = wait_for_visible_element_using_getter(
            self.driver, lambda _: get_caveat_field()
        )
        # ensure caveat field is already present
        if consumer_value in caveat_field.tags:
            return
        self.expand_consumers()

        def get_consumer_by_value() -> Consumer:
            try:
                return self.consumers[transform(consumer_value)]
            except KeyError as exc:
                raise ValueError(
                    f"Consumer with value {consumer_value!r} not found in {self}"
                ) from exc

        consumer = perform_action(get_consumer_by_value, timeout=WAIT_FRONTEND)
        perform_action(consumer.click, timeout=WAIT_FRONTEND)

        WebDriverWait(self.driver, WAIT_FRONTEND).until(
            lambda _: consumer_value in get_caveat_field().tags,
            message=f"Consumer {consumer_value!r} was not selected",
        )

    def select_consumer_type(self, consumer_type: str) -> None:
        consumer_type = transform(consumer_type)

        @repeat_failed(timeout=WAIT_FRONTEND)
        def choose_consumer_type() -> None:
            self.consumer_types[consumer_type].click()

        choose_consumer_type()
        self.wait_for_consumer_types_state(is_open=False)

    def expand_consumers(self) -> None:
        # only try to expand if no consumer loaded within 1 second
        try:
            WebDriverWait(self.driver, WAIT_FRONTEND).until(lambda _: len(self.consumers) > 0)
        except TimeoutException:
            self.list_option.click()
            self.wait_for_consumers_to_load()

    def wait_for_consumers_to_load(self) -> None:
        def assert_consumers_loaded() -> None:
            message = f"Consumers in {self} did not load properly, got: {self.consumers}"
            assert len(self.consumers) > 0, message
            assert all(consumer.name for consumer in self.consumers), message

        WebDriverWait(self.driver, WAIT_FRONTEND, ignored_exceptions=[AssertionError]).until(
            lambda _: assert_consumers_loaded()
        )

    def __str__(self) -> str:
        return "Consumer caveat popup"
