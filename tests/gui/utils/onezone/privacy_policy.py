"""Utils and fixtures to facilitate operation on privacy policy view"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from selenium.webdriver.remote.webdriver import WebDriver

from tests.gui.utils.core.web_elements import Button, WebElement


class PrivacyPolicy:
    message = WebElement(".wysiwyg-content")
    back_to_main_page = Button(".back-to-main-page")

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.web_elem = driver

    def __str__(self) -> str:
        return "Privacy Policy"
