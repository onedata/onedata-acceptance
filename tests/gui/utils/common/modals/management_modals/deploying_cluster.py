"""Utils and fixtures to facilitate operations on File distribution modal."""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.utils.core.web_elements import Label

from ..modal import Modal


class ClusterDeploymentModal(Modal):
    msg = Label("h1")
    progress = Label(".progress-bar")

    def __str__(self):
        return "Deploying cluster modal"
