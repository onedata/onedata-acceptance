"""Utils to facilitate operations on subpage of automation page in Onezone
gui """

__author__ = "Rafał Widziszewski"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import WebItemsSequence, Input, Label, \
    Button
from tests.gui.utils.onezone.generic_page import Element


class Workflow(Element):
    name = id = Label('.text-like-field')
    menu_button = Button('.one-menu-toggle')


class WorkflowsPage(PageObject):
    elements_list = WebItemsSequence('.atm-workflow-schemas-list' 
                                     ' .atm-workflow-schemas-list-entry',
                                     cls=Workflow)
