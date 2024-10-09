"""Utils to facilitate steps in panel GUI."""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)


from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Input, NamedButton


class PanelInitPage(PageObject):
    create_new_cluster = NamedButton(
        ".btn-primary", text="Create a new cluster"
    )
    join_cluster = NamedButton(".btn-primary", text="Join a cluster")

    username = Input('input[placeholder="Username"]')
    passphrase = Input('input[placeholder="Passphrase"]')
    confirm_passphrase = Input('input[placeholder="Confirm passphrase"]')

    submit_button = NamedButton(".btn-primary", text="Submit")
    back_button = NamedButton(".btn-back", text="Back")
