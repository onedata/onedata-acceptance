"""Utils for operations on modals in GUI tests
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.core.web_elements import WebItem
from .upload_presenter import UploadPresenter
from .user_account_menu import UserAccountPopup
from .toolbar import ToolbarPopup
from .deregister_provider import DeregisterProvider
from .member_menu import MemberMenu


class Popups(object):
    toolbar = WebItem('.webui-popover.in ul.dropdown-menu', cls=ToolbarPopup)
    deregister_provider = WebItem('.popover-deregister-provider',
                                  cls=DeregisterProvider)
    user_account_menu = WebItem('.webui-popover-content .user-account-menu',
                                cls=UserAccountPopup)
    member_menu = WebItem('.webui-popover.in', cls=MemberMenu)
    upload_presenter = WebItem('.hidden-xs .up-single-upload',
                               cls=UploadPresenter)

    def __init__(self, driver):
        self.driver = self.web_elem = driver

    def __str__(self):
        return 'popups'

    def is_upload_presenter(self):
        try:
            self.upload_presenter
        except RuntimeError:
            return False
        else:
            return True
