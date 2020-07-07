"""Utils to facilitate members operations in op panel GUI.
"""

__author__ = "Michal Dronka"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Button, Label


class MembersContentPage(PageObject):
    invite_using_token = Button('.user-token-container a')
    copy_token = Button('.copy-btn')
    direct_users_number = Label('.direct-users-number')
