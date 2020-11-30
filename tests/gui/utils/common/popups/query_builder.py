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


class Comparator(PageObject):
    def get_name(self):
        return self.web_elem.text


class QueryBuilderPopup(PageObject):
    and_operator = Button('.operator-and')
    or_operator = Button('.operator-or')
    not_operator = Button('.operator-not')

    property_choice = Button('.ember-basic-dropdown-trigger')
    properties = WebItemsSequence('.ember-power-select-option', cls=Property)

    comparators = WebItemsSequence('.comparator-selector '
                                   '.ember-power-select-option', cls=Comparator)
    comparator_choice = Button(
        '.comparator-selector .ember-basic-dropdown-trigger')

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
