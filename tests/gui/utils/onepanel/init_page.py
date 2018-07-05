"""Utils to facilitate steps in panel GUI.
"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import NamedButton, Input


class PanelInitPage(PageObject):
    create_new_cluster = NamedButton('.btn-primary', text='Create a new cluster')
    join_cluster = NamedButton('.btn-primary', text='Join a cluster')

    username = Input('input[placeholder="Username"]')
    password = Input('input[placeholder="Password"]')
    confirm_password = Input('input[placeholder="Confirm password"]')

    create_button = NamedButton('.btn-primary', text='Create')
    back_button = NamedButton('.btn-primary', text='Back')
