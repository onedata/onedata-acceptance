"""Utils and fixtures to facilitate operations on cookies popup.
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"


from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Button


class Cookies(PageObject):
    privacy_policy_link = Button('.privacy-policy-link')
    terms_of_use_link = Button('.terms-of-use-link')
    i_understand = Button('.accept-cookies')

    def __str__(self):
        return 'Cookies popup'


