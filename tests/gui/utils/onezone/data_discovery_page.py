"""Utils to facilitate operations on data discovery page in Onezone gui"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    WebItem, WebItemsSequence, Button, Label)


class QueryBuilder(PageObject):
    root_block = Button('.root-block')
    query_button = Button('.submit-query')


class ResultSample(PageObject):
    text = Label('.result-sample')
    source_button = Button('.go-to-file-link')


class DataDiscoveryPage(object):
    query_builder = WebItem('.query-builder', cls=QueryBuilder)
    results_list = WebItemsSequence('.results-list .query-results-result',
                                    cls=ResultSample)
    error_message = Label('.error-container .main-message')

    def __init__(self, driver):
        self.web_elem = self.driver = driver

    def __str__(self):
        return 'Data discovery page'
