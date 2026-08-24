"""Utils and fixtures to facilitate operations on data discovery query builder
popup.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Button, Input, Label, WebItemsSequence
from tests.gui.utils.core.web_objects import PageObjectNotFoundError
from tests.utils.utils import repeat_failed


class Property(PageObject):
    name = id = Label("span")


class Item(PageObject):
    def get_name(self) -> str:
        return self.web_elem.text


class ExpressionBuilderPopup(PageObject):
    and_operator = Button(".operator-and")
    or_operator = Button(".operator-or")
    not_operator = Button(".operator-not")
    except_operator = Button(".operator-except")

    property_choice = Button(".ember-basic-dropdown-trigger")
    properties = WebItemsSequence(".ember-power-select-option", cls=Property)

    comparators = WebItemsSequence(
        ".comparator-selector + div .ember-power-select-option", cls=Item
    )
    comparator_choice = Button(".comparator-selector.ember-basic-dropdown-trigger")

    values = WebItemsSequence(
        ".comparator-value-editor .ember-power-select-option", cls=Item
    )

    _dropdown_trigger_css_sel = ".comparator-value-editor .ember-basic-dropdown-trigger"
    values_choice = Button(_dropdown_trigger_css_sel)

    value = Input(".comparator-value")
    add_button = Button(".accept-condition")

    def expand_properties(self) -> None:
        self.property_choice()

    def choose_property(self, property_name: str) -> None:
        self.expand_properties()
        self.properties[property_name].click()

    def assert_property(self, property_name: str) -> bool:
        try:
            self.properties[property_name]
        except IndexError:
            return False
        return True

    def expand_comparators(self) -> None:
        self.comparator_choice()

    def choose_comparator(self, comparator_name: str) -> None:
        self.expand_comparators()
        for comparator in self.comparators:
            if comparator.get_name() == comparator_name:
                comparator.click()
                return
        raise PageObjectNotFoundError(f"There is no comparator {comparator_name}")

    @repeat_failed(timeout=WAIT_FRONTEND)
    def expand_values(self) -> None:
        if not self.is_values_dropdown_expanded():
            self.values_choice.click()
            assert self.is_values_dropdown_expanded(), "Values dropdown did not open"

    def is_values_dropdown_expanded(self) -> bool:
        return self.values_choice.web_elem.get_attribute("aria-expanded") == "true"

    def choose_value(self, value_name: str) -> None:
        self.expand_values()
        for value in self.values:
            if value.get_name() == value_name:
                value.click()
                return
        raise PageObjectNotFoundError(f"There is no value {value_name} available")
