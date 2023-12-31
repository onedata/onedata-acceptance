"""Utils to facilitate operations on pages in Onezone gui"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from abc import ABCMeta
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import NamedButton, Label


class Element(PageObject):
    name = id = Label('.one-label')

    def __call__(self, *args, **kwargs):
        self.web_elem.click()


class GenericPage(PageObject):
    __metaclass__ = ABCMeta

    name = id = Label('.row-heading .col-title')
    get_started = NamedButton('.btn-default', text='Get started')

    def __getitem__(self, item):
        return self.elements_list[item]
