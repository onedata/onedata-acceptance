"""Utils and fixtures to facilitate operations on file details modal.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from selenium.webdriver import ActionChains
from tests.gui.utils.common.modals.modal import Modal
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (Label, NamedButton, WebItem,
                                               WebItemsSequence, WebElement,
                                               Button)
from tests.gui.utils.generic import strip_path


class HardlinkEntry(PageObject):
    name = id = Label('.file-name')
    path = Label('.file-path .anchor-container')

    def get_path_string(self):
        return strip_path(self.path)


class Hardlinks(PageObject):
    tab = WebElement('.nav-link-hardlinks')
    files = WebItemsSequence('.file-hardlink', cls=HardlinkEntry)

    def is_active(self):
        return 'active' in self.tab.get_attribute('class')


class Charts(PageObject):
    title = Label('.title-content')
    chart = WebElement('.chart')


class SizeStatistics(PageObject):
    tab = Button('.nav-link-size')
    charts_title = Label('.title')
    chart = WebItemsSequence('.one-time-series-chart-plot', cls=Charts)

    def click_on_chart(self):
        ActionChains(self.driver).move_to_element_with_offset(
            self.chart[0].chart, 100, 100).click().perform()


class NavigationTab(PageObject):
    name = id = Label('.nav-link')


class DetailsModal(Modal):
    modal_name = Label('.modal-header h1')
    owner = Label('.file-info-row-owner .property-value')
    close = Button('.close')
    space_id = Button('.file-info-row-space-id .clipboard-btn')
    file_id = Button('.file-info-row-cdmi-object-id .clipboard-btn')
    size_statistics = WebItem('.modal-content', cls=SizeStatistics)
    hardlinks = WebItem('.modal-content', cls=Hardlinks)
    navigation = WebItemsSequence('.nav-tabs-file-info .ember-view',
                                  cls=NavigationTab)
    active_tab = Label('.nav-link.active')

    def __str__(self):
        return 'Details modal'

    def is_element_active(self, element_name):
        element = getattr(self, element_name)
        return 'active' in element.web_elem.get_attribute("class")

