"""Utils and fixtures to facilitate operations on data discovery query builder
popup.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Button, Label, WebItemsSequence


class Property(PageObject):
    name = id = Label('.special-property')


class QueryBuilderPopup(PageObject):
    and_operator = Button('.operator-and')
    or_operator = Button('.operator-or')
    not_operator = Button('.operator-not')
    property_choice = Button('.ember-basic-dropdown-trigger')
    properties = WebItemsSequence('.ember-power-select-option', cls=Property)

    def expand_properties(self):
        self.property_choice()

    def choose_property(self, property_name):
        self.expand_properties()
        self.properties[property_name].click()
