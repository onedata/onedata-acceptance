"""Utils to facilitate nodes operations in panel GUI.
"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in " 
               "LICENSE.txt")

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Label


class ClusterOverviewPage(PageObject):
    cluster_name = Label('.main-content .header-row .one-label')
