"""Utils to facilitate nodes operations in panel GUI."""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)


from tests.gui.utils.common.common import Toggle
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label, WebItemsSequence


class HostRecord(PageObject):
    name = id = Label(
        "td[data-option=name]",
        parent_name="hosts table in cluster deployment step",
    )
    database = Toggle(".one-way-toggle[data-option=database]")
    cluster_worker = Toggle(".one-way-toggle[data-option=clusterWorker]")
    cluster_manager = Toggle(".one-way-toggle[data-option=clusterManager]")
    primary_cluster_manager = Toggle(
        ".one-way-toggle[data-option=primaryClusterManager]"
    )

    def __str__(self):
        return "{} record in {}".format(self.name, self.parent)


class NodesContentPage(PageObject):
    hosts = WebItemsSequence("tr.cluster-host-table-row", cls=HostRecord)
