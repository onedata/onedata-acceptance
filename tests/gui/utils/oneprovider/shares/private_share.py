"""Utils and fixtures to facilitate operation on private share view"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2022 ACK CYFRONET AGH"
__license__ = (
    "This software is released under the MIT license cited in LICENSE.txt"
)

from selenium.webdriver.common.by import By
from tests.gui.utils.core import scroll_to_css_selector_bottom
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import Button, Input, Label, WebItem
from tests.gui.utils.oneprovider.shares.public_share import PublicShareView


class DublinCoreMetadata(PageObject):

    def write_to_last_input(self, val, which):
        css_sel = f'.form-control[data-dc-element-type="{which}"]'
        # WebItemsSequence, WebElementsSequence were not working for this
        # case (because of weird selectors)
        inputs = self.driver.find_elements(By.CSS_SELECTOR, css_sel)
        inputs[-1].clear()
        inputs[-1].send_keys(val)

    def click_add_button(self, button_name):
        buttons = self.driver.find_elements(
            By.CSS_SELECTOR, ".btn-add-entry .text"
        )
        for button in buttons:
            if button.text == button_name:
                css_sel = ".metadata-text .one-icon"
                scroll_to_css_selector_bottom(self.driver, css_sel)
                button.click()
                break
        else:
            raise RuntimeError(
                f'{button_name} was not found in "Dublin Core Metadata" form'
            )


class Description(PageObject):
    create_description = Button(".btn-content-info")
    description_field = Input(".textarea-source-editor")
    save = Button(".btn-primary")


class PrivateShareView(PublicShareView):
    dublin_core_metadata_form = WebItem(
        ".opendata-one-carousel", cls=DublinCoreMetadata
    )
    description_form = WebItem(".content-space-shares", cls=Description)

    choose_a_handle_service = Button(".select-handle-service")
    choose_a_metadata_type = Button(".select-metadata-type")
    proceed = Button(".btn-content-info")
    publish_as_open_data = Button(".btn-submit")
    link_name = Label(".ember-power-select-selected-item")

    def __str__(self):
        return "Private Share View"
