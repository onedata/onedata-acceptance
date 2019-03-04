"""Utils to facilitate common operations on clusters sidebar.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (WebItemsSequence, Label,
                                               NamedButton, Input)
from tests.gui.utils.core.web_objects import ButtonWithTextPageObject


class WelcomePage(PageObject):
    create_new_cluster = NamedButton('button', text='Create new cluster')
    create_onezone_cluster = NamedButton('.btn-primary',
                                         text='Create Onezone cluster')
    create_oneprovider_cluster = NamedButton('.btn-primary',
                                             text='Create Oneprovider cluster')


class ClusterRecord(ButtonWithTextPageObject):
    name = id = Label('.item-header .one-label', parent_name='clusters sidebar')
    submenu = WebItemsSequence('ul.one-list-level-2 li',
                               cls=ButtonWithTextPageObject)

    def __str__(self):
        return '{} item in {}'.format(self.name, self.parent)


class ClustersSidebar(PageObject):
    search_box = Input('ul.one-list li.search-bar-item input')
    items = WebItemsSequence('.sidebar-clusters ul.one-list '
                             'li.one-list-item.active',
                             cls=ClusterRecord)
