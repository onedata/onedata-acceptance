"""Utils and fixtures to facilitate operation on privacy policy view"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

from tests.gui.utils.core.web_elements import WebElement, Button


class PrivacyPolicy(object):
    message = WebElement('.wysiwyg-content')
    back_to_main_page = Button('.back-to-main-page')

    def __init__(self, driver):
        self.driver = driver
        self.web_elem = driver

    def __str__(self):
        return 'Privacy Policy'
