"""Utils to facilitate ceph control in panel GUI.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.common.common import Toggle
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    NamedButton, WebItem, Label, WebElementsSequence, Button, WebItemsSequence)


class StatusPage(PageObject):
    success_alert = Label('.alert-success')
    osds_limit = Label('.current-total-space')
    osds_usage = Label('.occupied-space')


class Node(PageObject):
    manager_and_monitor = Toggle('.manager-and-monitor.one-way-toggle')
    osds = WebElementsSequence('.osd-form')


class ConfigurationPage(PageObject):
    cluster_name = Label('.field-static-name')
    node = WebItem('.ceph-node', cls=Node)


class Pool(PageObject):
    name = id = Label('.pool-name')
    pool_usage = Label('.occupied-space')


class PoolsPage(PageObject):
    create_pool = Button('.create-pool')
    pools = WebItemsSequence('.cluster-ceph-pools '
                             '.one-collapsible-list-item', cls=Pool)


class CephContentPage(PageObject):
    status_tab = NamedButton('.nav-link', text='Status')
    configuration_tab = NamedButton('.nav-link', text='Configuration')
    pools_tab = NamedButton('.nav-link', text='Pools')

    status_page = WebItem('.content-clusters-ceph', cls=StatusPage)
    configuration_page = WebItem('.content-clusters-ceph', cls=ConfigurationPage)
    pools_page = WebItem('.content-clusters-ceph', cls=PoolsPage)
