"""Utils for operations on token caveats in GUI tests"""

__author__ = "Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import time
from datetime import datetime, timedelta
from typing import Callable, Iterable, Protocol, TypedDict, cast

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver

from tests.conftest import Hosts, SeleniumDrivers, Users
from tests.gui.types import TmpMemory
from tests.gui.utils.common.common import Toggle
from tests.gui.utils.common.popups import Popups
from tests.gui.utils.core.base import PageObject
from tests.gui.utils.core.web_elements import (
    Button,
    Input,
    Label,
    WebElement,
    WebItemsSequence,
)

RegionCaveat = TypedDict(
    "RegionCaveat", {"allow": bool, "region codes": list[str]}, total=False
)
CountryCaveat = TypedDict(
    "CountryCaveat", {"allow": bool, "country codes": list[str]}, total=False
)
ConsumerCaveatConfig = TypedDict(
    "ConsumerCaveatConfig", {"type": str, "by": str, "consumer name": str}
)


class PathCaveatConfig(TypedDict):
    space: str
    path: str


TokenCaveats = TypedDict(
    "TokenCaveats",
    {
        "expiration": dict[str, bool],
        "region": RegionCaveat,
        "country": CountryCaveat,
        "ASN": list[int],
        "IP": list[str],
        "consumer": list[ConsumerCaveatConfig],
        "service": dict[str, list[str]],
        "interface": str,
        "path": list[PathCaveatConfig],
        "object id": list[str],
    },
    total=False,
)


type PopupFactory = Callable[[WebDriver], Popups]


class CreateTokenPage(Protocol):
    def hide_caveats(self) -> None: ...

    def expand_caveats(self) -> None: ...


class TokensArea(Protocol):
    create_token_page: CreateTokenPage


class ZonePage(Protocol):
    def __getitem__(self, item: str) -> TokensArea: ...


class CaveatTag(PageObject):
    name = id = Label(".tag-label")
    icon = WebElement(".tag-icon")

    def is_icon_type(self, i_type: str) -> bool:
        if i_type == "oneprovider":
            i_type = "provider"
        return i_type in self.icon.get_attribute("class")


class PathEntry(PageObject):
    space_name = id = Label(".pathSpace-field")
    path = Label(".pathString-field")


class ObjectIdEntry(PageObject):
    name = id = Label(".text-like-field")


class CaveatField(PageObject):
    name = id = Label(".control-label")
    toggle = Toggle(".one-way-toggle")

    new_item = Button(".oneicon-plus")
    add_item = Button(".add-field-button")

    item_label = Label(".dropdown-field")
    expander = Button(".ember-power-select-trigger")
    time_input = Input(".form-control.date-time-picker")
    time_label = Label(".datetime-field")
    inner_input = Input(".tag-creator .text-editor-input")
    input = Input(".text-like-field .form-control")
    input_object_id = Input(".objectIdCaveat-field .text-like-field .form-control")

    rest_control = Button(".option-rest .one-way-radio-control")
    oneclient_control = Button(".option-oneclient .one-way-radio-control")

    tags = WebItemsSequence(".tag-item", cls=CaveatTag)
    interface_label = Label(".radio-field")
    readonly_toggle = Toggle(".readonlyView-field .one-way-toggle")
    path_entries = WebItemsSequence(".pathEntry-collapse", cls=PathEntry)
    object_id_entries = WebItemsSequence(".objectIdEntry-field", cls=ObjectIdEntry)

    def activate(self) -> None:
        self.toggle.check()

    def deactivate(self) -> None:
        self.toggle.uncheck()

    def is_allow(self) -> bool:
        return self.item_label == "Allow"

    def set_allow(
        self,
        popups: PopupFactory,
        selenium: SeleniumDrivers,
        browser_id: str,
    ) -> None:
        if not self.is_allow():
            self.expander()
            popups(selenium[browser_id]).power_select.choose_item("Allow")

    def set_deny(
        self,
        popups: PopupFactory,
        selenium: SeleniumDrivers,
        browser_id: str,
    ) -> None:
        if self.is_allow():
            self.expander()
            popups(selenium[browser_id]).power_select.choose_item("Deny")

    def set_allowance(
        self,
        allow: bool,
        popups: PopupFactory,
        selenium: SeleniumDrivers,
        browser_id: str,
    ) -> None:
        if allow:
            self.set_allow(popups, selenium, browser_id)
        else:
            self.set_deny(popups, selenium, browser_id)

    def assert_allowance(self, allow: bool) -> None:
        if allow:
            assert self.is_allow(), "Caveat type should be Allow but is Deny"
        else:
            assert not self.is_allow(), "Caveat type should be Deny but is Allow"

    def assert_num_caveats_equal(self, exp_items: Iterable[object]) -> None:
        msg = (
            f"Number of expected items {exp_items} does not equal actual "
            f"number of items {[tag.name for tag in self.tags]}"
        )
        assert len(list(exp_items)) == len(self.tags), msg

    # setters

    def set_item_in_inner_input(
        self, selenium: SeleniumDrivers, browser_id: str, item: str
    ) -> None:
        self.new_item()
        self.inner_input = item
        driver = selenium[browser_id]
        driver.switch_to.active_element.send_keys(Keys.RETURN)

    # expiration caveat
    def set_expiration_caveat(
        self,
        expire_caveat: dict[str, int],
        tmp_memory: dict[str, object],
    ) -> None:
        self.activate()
        min_delta = expire_caveat["after"]
        _time = self.get_time_after_delta(min_delta)
        self.time_input = _time
        tmp_memory["expire_time"] = _time

    def get_time_after_delta(self, delta: int) -> str:
        now = datetime.now()
        delta_td = timedelta(minutes=delta)
        then = now + delta_td
        return then.strftime("%Y/%m/%d %-H:%M")

    # region caveat
    def set_region_caveats(
        self,
        selenium: SeleniumDrivers,
        browser_id: str,
        region_caveat: RegionCaveat,
        popups: PopupFactory,
    ) -> None:
        self.activate()
        caveat_allow = region_caveat.get("allow", True)
        regions = region_caveat.get("region codes", [])
        self.set_allowance(caveat_allow, popups, selenium, browser_id)
        for region in regions:
            self.set_region_in_region_caveat(selenium, browser_id, region, popups)

    def set_region_in_region_caveat(
        self,
        selenium: SeleniumDrivers,
        browser_id: str,
        region: str,
        popups: PopupFactory,
    ) -> None:
        self.new_item()
        driver = selenium[browser_id]
        popups(driver).selector_popup.selectors[region]()

    # country caveat
    def set_country_caveats(
        self,
        selenium: SeleniumDrivers,
        browser_id: str,
        country_caveat: CountryCaveat,
        popups: PopupFactory,
    ) -> None:
        self.activate()
        caveat_allow = country_caveat.get("allow", True)
        countries = country_caveat.get("country codes", [])
        self.set_allowance(caveat_allow, popups, selenium, browser_id)
        for country in countries:
            self.set_item_in_inner_input(selenium, browser_id, country)

    # asn caveat
    def set_asn_caveats(
        self, selenium: SeleniumDrivers, browser_id: str, asn_list: Iterable[int]
    ) -> None:
        self.activate()
        for asn in asn_list:
            self.set_item_in_inner_input(selenium, browser_id, str(asn))

    # ip caveat
    def set_ip_caveats(
        self, selenium: SeleniumDrivers, browser_id: str, ips: Iterable[str]
    ) -> None:
        self.activate()
        for ip in ips:
            self.set_item_in_inner_input(selenium, browser_id, ip)

    # consumer caveat
    def set_consumer_caveats(
        self,
        selenium: SeleniumDrivers,
        browser_id: str,
        popups: PopupFactory,
        consumer_caveats: Iterable[ConsumerCaveatConfig],
        users: Users,
        groups: dict[str, str],
        hosts: Hosts,
        oz_page: Callable[[WebDriver], ZonePage],
    ) -> None:
        self.activate()
        oz_page(selenium[browser_id])["tokens"].create_token_page.hide_caveats()
        for consumer in consumer_caveats:
            consumer_type = cast(str, consumer.get("type"))
            method = cast(str, consumer.get("by"))
            value = cast(str, consumer.get("consumer name"))
            if method == "id":
                if consumer_type == "user":
                    value = users[value].user_id
                elif consumer_type == "group":
                    value = groups[value]
            if (
                consumer_type == "oneprovider"
                and method == "name"
                and "GuiObject" not in value
            ):
                value = hosts[value]["name"]
            self.set_consumer_in_consumer_caveat(
                selenium, browser_id, popups, consumer_type, method, value
            )
        oz_page(selenium[browser_id])["tokens"].create_token_page.expand_caveats()

    def set_consumer_in_consumer_caveat(
        self,
        selenium: SeleniumDrivers,
        browser_id: str,
        popups: PopupFactory,
        consumer_type: str,
        method: str,
        value: str,
    ) -> None:
        self.new_item()
        driver = selenium[browser_id]
        popup = popups(driver).consumer_caveat_popup
        popup.expand_consumer_types()
        popup.select_type(consumer_type)
        if method == "name":
            popup.list_option()
            popup.consumers[value]()
        else:
            popup.id_option()
            popup.input = value
            popup.add_button()

    # service caveat
    def set_service_caveats(
        self,
        selenium: SeleniumDrivers,
        browser_id: str,
        service_caveats: dict[str, list[str]],
        popups: PopupFactory,
    ) -> None:
        self.activate()
        service_cav = service_caveats.get("Service", [])
        service_onepanel_cav = service_caveats.get("Service Onepanel", [])
        for service in service_cav:
            self.set_service_in_service_caveat(
                selenium, browser_id, popups, "Service", service
            )
        for service in service_onepanel_cav:
            self.set_service_in_service_caveat(
                selenium, browser_id, popups, "Service Onepanel", service
            )

    def set_service_in_service_caveat(
        self,
        selenium: SeleniumDrivers,
        browser_id: str,
        popups: PopupFactory,
        consumer_type: str,
        value: str,
    ) -> None:
        self.new_item()
        driver = selenium[browser_id]
        popup = popups(driver).consumer_caveat_popup
        popup.expand_consumer_types()
        time.sleep(0.5)
        popup.consumer_types[consumer_type]()
        time.sleep(0.5)
        popup.list_option()

        # this line is to load elements, test fails without it
        _ = [consumer.name for consumer in popup.consumers]
        time.sleep(0.5)
        popup.consumers[value]()

    # interface caveat
    def set_interface_caveat(self, caveat: str) -> None:
        self.activate()
        getattr(self, f"{caveat.lower()}_control").click()

    # readonly caveat
    def set_readonly_caveat(self) -> None:
        self.activate()

    # path caveat
    def set_path_caveats(self, path_caveats: Iterable[PathCaveatConfig]) -> None:
        self.activate()
        for path_caveat in path_caveats:
            self.set_path_caveat(path_caveat)

    def set_path_caveat(self, path_caveat: PathCaveatConfig) -> None:
        space = path_caveat["space"]
        path = path_caveat["path"]
        self.add_item()
        if not self.item_label == space:
            self.expander()
            if hasattr(self, "options"):
                self.options[space]()
            else:
                raise ValueError("there is not options member in class instance")
        self.input = path

    # object id caveat
    def set_object_id_caveats(self, ids: Iterable[str]) -> None:
        self.activate()
        for object_id in ids:
            self.set_object_id_caveat(object_id)

    def set_object_id_caveat(self, object_id: str) -> None:
        self.add_item()
        self.input_object_id = str(object_id)

    # assertions

    # expiration caveat
    def assert_expiration_caveat(
        self, exp_caveat: dict[str, bool], tmp_memory: TmpMemory
    ) -> None:
        value_set = exp_caveat.get("set", False)
        if value_set:
            expected_time = tmp_memory.get("expire_time", None)
            actual_time = self.time_label
            msg = f"Expected time {expected_time} does not match actual {actual_time}"
            assert expected_time == actual_time, msg
        else:
            msg = "Time should not be set but it is"
            assert tmp_memory.get("expire_time", None) is None, msg

    # region caveat
    def assert_region_caveats(self, region_caveat: RegionCaveat) -> None:
        caveat_allow = region_caveat.get("allow", True)
        regions = region_caveat.get("region codes", [])
        self.assert_allowance(caveat_allow)
        self.assert_num_caveats_equal(regions)
        for region in regions:
            self.assert_region_in_region_caveat(region)

    def assert_region_in_region_caveat(self, region: str) -> None:
        assert (
            region in self.tags
        ), f"{region} should be amongst region caveats but is not"

    # country caveat
    def assert_country_caveats(self, country_caveat: CountryCaveat) -> None:
        caveat_allow = country_caveat.get("allow", True)
        countries = country_caveat.get("country codes", [])
        self.assert_allowance(caveat_allow)
        self.assert_num_caveats_equal(countries)
        for country in countries:
            self.assert_region_in_region_caveat(country)

    def assert_country_in_country_caveat(self, country: str) -> None:
        assert (
            country in self.tags
        ), f"{country} should be amongst country caveats but is not"

    # asn caveat
    def assert_asn_caveats(self, asn_list: Iterable[int]) -> None:
        self.assert_num_caveats_equal(asn_list)
        for asn in asn_list:
            self.assert_asn_in_asn_caveats(str(asn))

    def assert_asn_in_asn_caveats(self, asn: str) -> None:
        assert asn in self.tags, f"{asn} should be amongst asn caveats but is not"

    # ip caveat
    def assert_ip_caveats(self, ips: Iterable[str]) -> None:
        self.assert_num_caveats_equal(ips)
        for ip in ips:
            self.assert_ip_in_ip_caveats(ip)

    def assert_ip_in_ip_caveats(self, ip: str) -> None:
        assert ip in self.tags, f"{ip} should be amongst ip caveats but is not"

    # consumer caveat
    # creation parameter is to check if assertion is done directly after
    # creation - then consumer is checked only by name
    def assert_consumer_caveats(
        self,
        consumer_caveats: Iterable[ConsumerCaveatConfig],
        users: Users,
        groups: dict[str, str],
        hosts: Hosts,
        creation: bool,
    ) -> None:
        for consumer in consumer_caveats:
            consumer_type = consumer["type"]
            if creation:
                method = "name"
            else:
                method = consumer["by"]
            value = consumer["consumer name"]
            if method == "id":
                if consumer_type == "user":
                    value = users[value].user_id
                elif consumer_type == "group":
                    value = groups[value]
            if (
                consumer_type == "oneprovider"
                and method == "name"
                and "GuiObject" not in value
            ):
                value = hosts[value]["name"]
            self.assert_consumer_in_consumer_caveat(consumer_type, method, value)

    def assert_consumer_in_consumer_caveat(
        self, consumer_type: str, method: str, value: str
    ) -> None:
        if method == "name":
            tag = self.tags[value]
        else:
            tag = self.tags["ID: " + value]
        assert tag.is_icon_type(
            consumer_type
        ), f"Consumer caveat for {value} is not {consumer_type}"

    # service caveat
    def assert_service_caveats(self, services: Iterable[str]) -> None:
        self.assert_num_caveats_equal(services)
        for service in services:
            self.assert_ip_in_ip_caveats(service)

    def assert_service_in_service_caveat(self, service: str) -> None:
        assert (
            service in self.tags
        ), f"{service} should be amongst services caveats but is not"

    # interface caveat
    def assert_interface_caveat(self, interface: str) -> None:
        assert self.interface_label == interface

    # readonly caveat
    def assert_readonly_caveat(self) -> None:
        assert self.readonly_toggle.is_checked(), "Readonly not set"

    # path caveat
    def assert_path_caveats(self, paths: Iterable[PathCaveatConfig]) -> None:
        for path in paths:
            self.assert_path_caveat(path)

    def assert_path_caveat(self, path_caveat: PathCaveatConfig) -> None:
        space = path_caveat["space"]
        path = path_caveat["path"]
        entry = self.path_entries[space]
        assert (
            entry.path == path
        ), f"Invalid path: {space} {path}. Actual: {entry.space_name} {entry.path}"

    # object id caveat
    def assert_object_id_caveats(self, ids: Iterable[str]) -> None:
        for object_id in ids:
            self.assert_object_id_caveat(object_id)

    def assert_object_id_caveat(self, object_id: str) -> None:
        assert (
            object_id in self.object_id_entries
        ), f"Object id {object_id} not in object ids"
