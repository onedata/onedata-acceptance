"""Utils to facilitate operations on discovery page in Onezone gui"""

__author__ = "Michal Stanisz, Agnieszka Warchol"
__copyright__ = "Copyright (C) 2018 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import math
import re
from typing import Literal

from selenium.common.exceptions import (
    StaleElementReferenceException,
    TimeoutException,
)
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait

from tests.gui.constants import DEFAULT_SCREEN_SIZE, WAIT_BACKEND, WAIT_FRONTEND, ScreenSize
from tests.gui.utils.core.base import NamedElement, PageObject
from tests.gui.utils.core.web_elements import (
    Button,
    Icon,
    Input,
    Label,
    NamedButton,
    WebElement,
    WebElementsSequence,
    WebItem,
    WebItemsSequence,
)
from tests.gui.utils.core.web_objects import PageObjectNotFoundError
from tests.gui.utils.generic import perform_action
from tests.gui.utils.onezone.generic_page import SidebarPanelPage
from tests.utils.utils import element_has_class, repeat_failed

from .common import EditBox, InputBox
from .members_subpage import MembersPage
from .space_configuration_subpage import SpaceConfigurationPage
from .space_marketplace import SpaceMarketplacePage

SPACE_HEADER_SELECTOR_PREFIX = ".sidebar-spaces .two-level-sidebar .data-row:nth-of-type"
NEXT_SCROLL_SHIFT = 9
CONST_SCROLL_IDX = 24


class Space(NamedElement):
    name = id = Label(".item-name", scroll=False)
    support_size = Label(".status-toolbar-icon:first-of-type", scroll=False)
    supporting_providers_number = Label(".status-toolbar-icon:last-of-type", scroll=False)
    advertised_icon = Icon(".oneicon-cart-checked", scroll=False)
    home_icon = WebElement(".status-toolbar-icon:first-of-type span", scroll=False)

    overview = NamedButton(".one-list-level-2 .item-header", text="Overview")
    files = NamedButton(".one-list-level-2 .item-header", text="Files")
    shares_public_data = NamedButton(".one-list-level-2 .item-header", text="Shares, Public Data")
    transfers = NamedButton(".one-list-level-2 .item-header", text="Transfers")
    datasets_archives = NamedButton(".one-list-level-2 .item-header", text="Datasets, Archives")
    providers = NamedButton(".one-list-level-2 .item-header", text="Providers")
    members = NamedButton(".one-list-level-2 .item-header", text="Members")
    harvesters_discovery = NamedButton(
        ".one-list-level-2 .item-header", text="Harvesters, Discovery"
    )
    automation_workflows = NamedButton(
        ".one-list-level-2 .item-header", text="Automation Workflows"
    )
    configuration = NamedButton(".one-list-level-2 .item-header", text="Configuration")
    menu_button = Button(".collapsible-toolbar-toggle")

    def click_menu(self) -> None:
        self.click()
        self.menu_button.click()

    def is_element_disabled(self, element_name: str) -> bool:
        element = getattr(self, element_name)
        return "disabled" in element.web_elem.get_attribute("class")

    def is_element_enabled(self, element_name: str) -> bool:
        element = getattr(self, element_name)
        return "disabled" not in element.web_elem.get_attribute("class")

    def is_active(self) -> bool:
        return element_has_class(self.web_elem, "active")


class SpaceHeader(NamedElement):
    name = id = Label(".item-name", scroll=False)
    support_size = Label(".status-toolbar-icon:first-of-type", scroll=False)
    supporting_providers_number = Label(".status-toolbar-icon:last-of-type", scroll=False)
    advertised_icon = Icon(".oneicon-cart-checked", scroll=False)
    home_icon = WebElement(".status-toolbar-icon:first-of-type span", scroll=False)
    menu_button = Button(".collapsible-toolbar-toggle", scroll=False)
    clickable_field = WebElement(".item-name", scroll=False)

    def click_menu(self) -> None:
        self.click()
        self.menu_button.click()


class Provider(NamedElement):
    id = name = Label(".one-label")
    support = Label(".outer-text")
    menu_button = Button(".provider-menu-toggle")
    information_button = Button(".oneicon-provider")


class SpaceInfoTile(PageObject):
    rename = Button(".edit-icon")
    edit_name_box = WebItem(".editor", cls=EditBox)
    shares_count = Label(".shares-count")


class SpaceMembersTile(PageObject):
    direct_groups = Label(".direct-groups-counter")
    direct_users = Label(".direct-users-counter")
    effective_groups = Label(".effective-groups-counter")
    effective_users = Label(".effective-users-counter")


class SpaceDetailsTile(PageObject):
    organization_name = Label(".organization-name")
    description = Label(".description-row")
    tags = WebElementsSequence(".tag-item")


class SpaceMarketplaceTile(PageObject):
    advertise_info = Label(".figure-bottom-text")
    configure_advertisement = Button(".tile-footer-link")
    show = Button(".more-link")


class ProvidersMap(NamedElement):
    name = id = Label(".one-label")
    providers = WebElementsSequence(".one-atlas-point")

    def click_provider(self, provider_name: str, driver: WebDriver) -> None:
        for provider in self.providers:
            ActionChains(driver).move_to_element(provider).perform()
            name = driver.find_element(By.CSS_SELECTOR, ".tooltip-inner").text
            if name == provider_name:
                provider.click()
                return

        raise PageObjectNotFoundError(f"Provider {provider_name} was not found on the map")

    def hover_and_check_provider(self, provider_name: str, driver: WebDriver) -> None:
        for provider in self.providers:
            ActionChains(driver).move_to_element(provider).perform()
            name = driver.find_element(By.CSS_SELECTOR, ".tooltip-inner").text
            if name == provider_name:
                return

        raise PageObjectNotFoundError(f"Provider {provider_name} was not found on the map")

    def get_provider_horizontal_position(self, provider_name: str, driver: WebDriver) -> float:
        for provider in self.providers:
            ActionChains(driver).move_to_element(provider).perform()
            name = driver.find_element(By.CSS_SELECTOR, ".tooltip-inner").text
            if name == provider_name:
                style = provider.get_attribute("style")
                match = re.search(r"left:\s*(\d+\.*\d*)px", style)
                if match is None:
                    raise ValueError(f"Cannot parse left position from style: {style}")
                position = match.group(1)

                return float(position)

        raise PageObjectNotFoundError(f"Provider {provider_name} was not found on the map")


class SpaceOverviewPage(PageObject):
    space_name = Label(".header-row .one-label")
    info_tile = WebItem(".resource-info-tile", cls=SpaceInfoTile)
    members_tile = WebItem(".resource-members-tile .tile-main", cls=SpaceMembersTile)
    map = WebItem(".map-container", cls=ProvidersMap)
    space_details_tile = WebItem(".space-details-tile", cls=SpaceDetailsTile)
    marketplace_tile = WebItem(".space-marketplace-tile", cls=SpaceMarketplaceTile)


class WelcomePage(PageObject):
    create_a_space = NamedButton(".info .ember-view", text="Create a space")
    join_an_existing_space = NamedButton(".info .ember-view", text="join an existing space")
    join_group = NamedButton(".info .ember-view", text="join a group")


class HarvesterRow(NamedElement):
    name = id = Label(".item-name")
    harvester = WebElement(".item-name")
    harvester_menu_button = WebElement(".collapsible-toolbar-toggle")

    def click_harvester_menu_button(self, driver: WebDriver) -> None:
        ActionChains(driver).move_to_element(self.harvester).perform()
        self.harvester_menu_button.click()


class HarvestersPage(PageObject):
    harvesters_list = WebItemsSequence(".main-content .one-collapsible-list-item", cls=HarvesterRow)
    add_one_of_harvesters = NamedButton(
        ".add-harvester-to-space-trigger.btn", text="Add one of your harvesters"
    )
    invite_harvester_using_token = NamedButton(
        ".generate-invite-token-action.btn", text="Invite harvester using token"
    )


class GetSupportPage(PageObject):
    request_support_modal = NamedButton(".nav-link", text="Request support")
    deploy_provider_modal = NamedButton(".nav-link", text="Deploy your own Oneprovider")
    expose_existing_data_modal = NamedButton(".nav-link", text="Expose existing data set")

    token_textarea = Label(".active textarea")
    copy = Button(".request-support-tab .copy-btn")
    forbidden_alert = WebElement(".error")
    insufficient_privileges = Label(".text-center .col-xs-12")


class SpaceProvidersHeader(PageObject):
    providers_tab = WebElementsSequence(".provider-online")
    overview_tab = WebElement(".item-overview")

    def get_current_active_tab(self) -> str | None:
        for tab in self.providers_tab + [self.overview_tab]:
            if "active" in tab.get_attribute("class"):
                return tab.text
        return None


class SpaceProvidersPage(PageObject):
    header = WebItem(".content-header-section", cls=SpaceProvidersHeader)
    settings_message = Label(".space-settings-info")
    providers_list = WebItemsSequence(
        ".space-providers-list li.one-collapsible-list-item", cls=Provider
    )
    get_support_page = WebItem(".ember-view", cls=GetSupportPage)
    add_support = Button(".btn-add-support")
    map = WebItem(".space-providers-atlas", cls=ProvidersMap)


class _Provider(PageObject):
    name = id = Label(".record-name-general")


class DatasetHeader(PageObject):
    detached = Button(".btn-effecitve")
    attached = Button(".select-attached-datasets-btn")


class ArchiveHeader(PageObject):
    back_to_dataset_page = Button(".content-back-arrow-icon")


class DataPage(SidebarPanelPage):
    panel_name = "data"

    create_space_button = Button(".one-sidebar-toolbar-button .oneicon-add-filled")

    marketplace_button = Button(".one-sidebar-toolbar-button .oneicon-cart")

    spaces_headers_list = WebItemsSequence(
        ".sidebar-spaces li.one-list-item.clickable.resource-item .item-header:not(.truncate)",
        cls=SpaceHeader,
    )
    sidebar_element = WebElement(".sidebar-spaces .two-level-sidebar", scroll=False)

    def scroll_to_top(self, timeout: float = 2 * WAIT_BACKEND) -> None:
        self.driver.execute_script(
            "document.querySelector('.perfect-scrollbar-element.ps--active-y').scrollTo(0, 0)"
        )

        def is_top_window_loaded(_: WebDriver) -> bool:
            visible_headers = self.get_visible_spaces_list()
            return bool(visible_headers and visible_headers[0].name)

        WebDriverWait(
            self.driver,
            timeout=timeout,
            ignored_exceptions=(StaleElementReferenceException,),
        ).until(is_top_window_loaded)

    spaces_list = WebItemsSequence(
        ".sidebar-spaces li.one-list-item.clickable.resource-item", cls=Space
    )

    save_icon = Button(".sidebar-item-title .save-icon")
    input_rename = Input(".sidebar-item-title .form-control")

    input_box = WebItem(".content-info-content-container", cls=InputBox)

    overview_page = WebItem(".main-content", cls=SpaceOverviewPage)
    providers_page = WebItem(".main-content", cls=SpaceProvidersPage)
    members_page = WebItem(".main-content", cls=MembersPage)
    welcome_page = WebItem(".main-content", cls=WelcomePage)
    harvesters_page = WebItem(".main-content", cls=HarvestersPage)
    dataset_header = WebItem(".main-content", cls=DatasetHeader)
    archive_header = WebItem(".main-content", cls=ArchiveHeader)
    configuration_page = WebItem(".main-content", cls=SpaceConfigurationPage)
    space_marketplace_page = WebItem(".main-content", cls=SpaceMarketplacePage)

    # button in top right corner on all subpages
    menu_button = Button(".with-menu .collapsible-toolbar-toggle")

    get_started = Button(".btn.btn-default.hide-sm-active.ember-view")

    tab_name = Label(".header-row")

    current_provider = Label(".current-oneprovider-bar .record-name-general")
    providers = WebItemsSequence(".provider-online", cls=_Provider)
    choose_other_provider = Button(".choose-oneprovider-link")
    error_header = Label(".content-info-content-container h1")

    def choose_space(self, name: str) -> None:
        for space in self.spaces_list:
            if space.name in (name, ""):
                space.click()
                if space.name == name:
                    return
        raise PageObjectNotFoundError(f"{name} space not found")

    @repeat_failed(timeout=WAIT_FRONTEND)
    def get_visible_spaces_list(self) -> list[SpaceHeader]:
        return [space for space in self.spaces_headers_list if space.name != ""]

    def scroll_by_arrow(self, direction: Literal["up", "down"] = "up") -> None:
        key = Keys.ARROW_DOWN if direction == "down" else Keys.ARROW_UP
        ActionChains(self.driver).move_to_element(self.sidebar_element).send_keys(key).perform()

    def get_element_names(self) -> list[str]:
        return [space.name for space in self.get_visible_spaces_list()]

    def get_first_window_bounds_and_number_of_items_per_window(
        self, initial_scroll_idx
    ) -> tuple[int, int]:
        initial_items_count = len(self.get_element_names())

        if initial_items_count == len(self.spaces_headers_list):
            # all files are within first window
            return {
                "bounds": {"start": 0, "end": initial_items_count - 1},
            }

        # Do first scroll, then revert it, to render first visible items
        self.scroll_to_nth_type_selector(SPACE_HEADER_SELECTOR_PREFIX, initial_scroll_idx)
        self.scroll_to_top()
        self.scroll_to_nth_type_selector(SPACE_HEADER_SELECTOR_PREFIX, initial_scroll_idx)

        next_visible_count = len(self.get_element_names())
        return {
            "window_bounds": [
                {"start": 0, "end": initial_items_count - 1},
                {
                    "start": NEXT_SCROLL_SHIFT - 2,
                    "end": (NEXT_SCROLL_SHIFT - 2) + next_visible_count - 1,
                },
            ],
            "next_visible": next_visible_count,
        }

    def get_space_header_by_index(self, index: int, initial_scroll_idx: int = 24) -> SpaceHeader:
        self.scroll_to_top()
        loaded_headers = self.get_visible_spaces_list()

        if index < len(loaded_headers):
            return loaded_headers[index]

        params = self.get_first_window_bounds_and_number_of_items_per_window(initial_scroll_idx)

        first_window = params["window_bounds"][0]
        if len(params["window_bounds"]) == 1 and index > first_window["end"]:
            raise IndexError(f"Index {index} is larger than number of elements")

        second_window = params["window_bounds"][1]
        if index > second_window["end"]:
            additional_scrolls = math.ceil((index - second_window["end"]) / NEXT_SCROLL_SHIFT)
        else:
            additional_scrolls = 0

        prev_name = self.get_space_header()

        for _ in range(additional_scrolls):
            name = self.scroll_and_get_space_header(prev_name)
            prev_name = name

        if additional_scrolls == 0:
            window_start = second_window["start"]
        else:
            window_start = second_window["start"] + additional_scrolls * NEXT_SCROLL_SHIFT

        local_index = index - window_start
        return self.get_visible_spaces_list()[local_index]

    def scroll_and_get_space_header(self, prev_name: str, idx: int = CONST_SCROLL_IDX) -> str:
        self.scroll_to_nth_type_selector(SPACE_HEADER_SELECTOR_PREFIX, idx)
        return self.get_element_and_wait(
            prev_name,
            SpaceHeader,
            SPACE_HEADER_SELECTOR_PREFIX,
            idx,
            timeout=WAIT_FRONTEND // 2,
        ).name

    def get_space_header(self, idx: int = CONST_SCROLL_IDX) -> str:
        return self.get_item_row(
            SpaceHeader,
            SPACE_HEADER_SELECTOR_PREFIX,
            idx,
        ).name

    def count_space_headers(self, initial_scroll_idx: int = 24) -> int:
        self.scroll_to_top()
        params = self.get_first_window_bounds_and_number_of_items_per_window(initial_scroll_idx)
        scroll_windows = params["window_bounds"]

        if len(params["window_bounds"]) == 1:
            return scroll_windows[0]["end"] + 1

        prev_name = self.get_element_and_wait("", SpaceHeader, SPACE_HEADER_SELECTOR_PREFIX, CONST_SCROLL_IDX).name
        first_item_next_window = self.get_space_header(
            idx=CONST_SCROLL_IDX - 14 + NEXT_SCROLL_SHIFT
        )

        additional_scrolls = 0
        partial_scroll = False
        while True:
            self.scroll_to_nth_type_selector(SPACE_HEADER_SELECTOR_PREFIX, CONST_SCROLL_IDX)

            try:
                new_name = self.get_element_and_wait(prev_name, SpaceHeader, SPACE_HEADER_SELECTOR_PREFIX, CONST_SCROLL_IDX).name
            except TimeoutException:
                break

            first_item_this_window = self.get_space_header(idx=CONST_SCROLL_IDX - 10)
            if first_item_this_window != first_item_next_window:
                partial_scroll = True
                break

            first_item_next_window = self.get_space_header(
                idx=CONST_SCROLL_IDX - 10 + NEXT_SCROLL_SHIFT
            )

            prev_name = new_name
            additional_scrolls += 1

        elements_count = scroll_windows[1]["start"] + additional_scrolls * NEXT_SCROLL_SHIFT
        elements = self.get_element_names()

        if partial_scroll:
            elements_count += NEXT_SCROLL_SHIFT - elements.index(first_item_next_window)

        elements_count += len(elements)
        return elements_count
