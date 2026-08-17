"""Utils and fixtures to facilitate operation on private share view"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from selenium.common.exceptions import ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from tests.gui.utils.common.common import DropdownSelector
from tests.gui.utils.core import scroll_to_css_selector_bottom
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Button,
    Input,
    Label,
    WebElement,
    WebItem,
    WebItemsSequence,
)
from tests.gui.utils.core.web_objects import PageObjectNotFoundError
from tests.gui.utils.oneprovider.shares.public_share import PublicShareView


class DublinCoreMetadata(PageObject):
    add_more_elements = Button(".row-metadata-group-add .ember-basic-dropdown-trigger")
    header = WebElement(".metadata-group-header")

    def click_on_background(self) -> None:
        ActionChains(self.driver).move_to_element_with_offset(
            self.header, 0, 0
        ).click().perform()

    def write_to_last_input(self, driver: WebDriver, val: str, which: str) -> None:
        css_selector = f'.form-control[data-dc-element-type="{which}"]'
        # WebItemsSequence, WebElementsSequence were not working for this
        # case (because of weird selectors)
        inputs = self.driver.find_elements(By.CSS_SELECTOR, css_selector)
        driver.execute_script("arguments[0].scrollIntoView();", inputs[-1])
        inputs[-1].clear()
        inputs[-1].send_keys(val)

    def click_add_button(self, driver: WebDriver, button_name: str) -> None:
        buttons = self.driver.find_elements(By.CSS_SELECTOR, ".btn-add-entry .text")
        for button in buttons:
            if button.text == "":
                driver.execute_script("arguments[0].scrollIntoView();", button)
            if button.text == button_name:
                css_selector = ".metadata-text .one-icon"
                scroll_to_css_selector_bottom(self.driver, css_selector)
                try:
                    button.click()
                except ElementNotInteractableException:
                    driver.execute_script("arguments[0].scrollIntoView();", button)
                    button.click()
                break
        else:
            raise PageObjectNotFoundError(
                f'{button_name} was not found in "Dublin Core Metadata" form'
            )


class EDMBoxForm(PageObject):
    name = id = Label(".edm-property-type-name", scroll=False)
    language = WebElement(".edm-lang-dropdown-trigger", scroll=False)
    input = WebElement(
        ".edm-property-value input, .edm-property-value textarea", scroll=False
    )
    dropdown = WebElement(".edm-property-value", scroll=False)


class EDMMetadataForm(PageObject):
    items = WebItemsSequence(
        ".edm-property-group-box .visual-edm-property", cls=EDMBoxForm, scroll=False
    )
    add_property = Button(".btn.add-edm-property-btn", scroll=False)


class EDMBoxView(PageObject):
    name = id = Label(".edm-property-type-name", scroll=False)
    language = WebElement(".edm-attr-value", scroll=False)
    value = WebElement(".edm-property-value", scroll=False)


class EDMMetadataView(PageObject):
    items = WebItemsSequence(
        ".edm-property-group-box .visual-edm-property", cls=EDMBoxView, scroll=False
    )


class Description(PageObject):
    create_description = Button(".btn-content-info")
    description_field = Input(".textarea-source-editor")
    save = Button(".btn-primary")


class PrivateShareView(PublicShareView):
    dublin_core_metadata_form = WebItem(
        ".publicdata-one-carousel", cls=DublinCoreMetadata
    )
    edm_metadata_form = WebItem(
        ".publicdata-one-carousel", cls=EDMMetadataForm, scroll=False
    )

    dropdown = DropdownSelector(".ember-basic-dropdown-content")

    edm_public_view = WebItem(".visual-edm", cls=EDMMetadataView, scroll=False)
    description_form = WebItem(".content-space-shares", cls=Description)

    choose_a_handle_service = Button(".select-handle-service")
    choose_a_metadata_type = Button(".select-metadata-type")
    proceed = Button(".btn-content-info")
    expose_as_public_data = Button(".btn-submit")
    link_name = Label(".ember-power-select-selected-item")

    alert_warning = WebElement(".alert-warning")

    def __str__(self) -> str:
        return "Private share View"
