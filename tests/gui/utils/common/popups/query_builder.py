"""Utils and fixtures to facilitate operations on data discovery query builder
popup.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import time

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Button, Label, WebItemsSequence, Input)


class Property(PageObject):
    name = id = Label('span')


class Item(PageObject):
    def get_name(self):
        return self.web_elem.text


class ExpressionBuilderPopup(PageObject):
    and_operator = Button('.operator-and')
    or_operator = Button('.operator-or')
    not_operator = Button('.operator-not')
    except_operator = Button('.operator-except')

    property_choice = Button('.ember-basic-dropdown-trigger')
    properties = WebItemsSequence('.ember-power-select-option', cls=Property)

    comparators = WebItemsSequence('.comparator-main-container '
                                   '.ember-power-select-option', cls=Item)
    comparator_choice = Button(
        '.comparator-main-container .ember-basic-dropdown-trigger')

    values = WebItemsSequence('.comparator-main-container '
                              '.ember-power-select-option', cls=Item)
    values_choice = Button(
        '.comparator-main-container .ember-basic-dropdown-trigger')
    qos_values_choice = Button(
        '.comparator-value-editor .ember-basic-dropdown-trigger')

    value = Input('.comparator-value')
    add_button = Button('.accept-condition')

    def expand_properties(self):
        self.property_choice()

    def choose_property(self, property_name):
        self.expand_properties()
        self.properties[property_name].click()

    def assert_property(self, property_name):
        try:
            self.properties[property_name]
        except IndexError:
            return False
        return True

    def expand_comparators(self):
        self.comparator_choice()

    def choose_comparator(self, comparator_name):
        self.expand_comparators()
        for comparator in self.comparators:
            if comparator.get_name() == comparator_name:
                comparator.click()
                return
        raise RuntimeError(f'There is no comparator {comparator_name}')

    def expand_values(self):
        self.values_choice()

    def choose_value(self, value_name):
        self.expand_values()
        for value in self.values:
            if value.get_name() == value_name:
                value.click()
                return
        raise RuntimeError(f'There is no value {value_name} available')
