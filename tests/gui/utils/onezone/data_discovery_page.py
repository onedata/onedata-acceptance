"""Utils to facilitate operations on data discovery page in Onezone gui"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)

from tests.gui.utils.common.query_builder import QueryBuilder
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Button,
    Label,
    WebElementsSequence,
    WebItem,
    WebItemsSequence,
)


class ResultSample(PageObject):
    text = Label(".result-sample")
    source_button = Button(".go-to-file-link")


class XattrsTreeNode(PageObject):
    name = id = Label(".tree-label")
    checkbox = Button(".tree-checkbox")


class OnedataTreeNode(PageObject):
    name = id = Label(".tree-label")
    checkbox = Button(".tree-checkbox")
    expander = Button(".tree-toggle")
    xattrs_tree_nodes = WebItemsSequence(
        ".tree-branch .tree-node", cls=XattrsTreeNode
    )


class TreeNode(PageObject):
    name = id = Label(".tree-label")
    checkbox = Button(".tree-checkbox")
    expander = Button(".tree-toggle")
    onedata_tree_nodes = WebItemsSequence(
        ".tree-branch .tree-node", cls=OnedataTreeNode
    )


class FilterTree(PageObject):
    tree_nodes = WebItemsSequence(".tree-node", cls=TreeNode)


class DataDiscoveryPage(object):
    page_size = Label(".page-size-selector .ember-power-select-selected-item")
    next_page = Button(".next-page")
    query_button = Button(".submit-query")
    filter_properties_button = Button(".filtered-properties-selector")
    rest_api_button = Button(".generate-query-request")

    sorting_parameter_selector = Button(".property-selector")
    sorting_order_selector = Button(".direction-selector")
    items = WebElementsSequence(".ember-power-select-option")

    query_builder = WebItem(".query-builder", cls=QueryBuilder)
    results_list = WebItemsSequence(
        ".results-list .query-results-result", cls=ResultSample
    )
    error_message = Label(".error-container .main-message")

    ecrin_gui_app_logo = Label(".app-logo")

    filter_properties_tree = WebItem(".tree", cls=FilterTree)

    def choose_item(self, property_name):
        for item in self.items:
            if item.text == property_name:
                item.click()
                return

    def __init__(self, driver):
        self.web_elem = self.driver = driver

    def __str__(self):
        return "Data discovery page"
