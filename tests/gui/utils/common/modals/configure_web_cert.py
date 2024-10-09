"""Utils and fixtures to facilitate operations on modal shown after provider
domain change.
"""

__author__ = "Jakub Liput"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)

from tests.gui.utils.core.web_elements import Input, NamedButton

from .modal import Modal


class ConfigureWebCertModal(Modal):
    discard = NamedButton(".btn-default", text="Discard")
    go_to_web_cert = NamedButton(
        ".btn-primary", text="Go to certificate management"
    )

    def __str__(self):
        return "Configure web cert modal"
