"""This module contains gherkin steps to run acceptance tests featuring
common operations in onepanel web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.conftest import Hosts, SeleniumDrivers
from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.steps.onezone.clusters import get_old_or_new_cluster_record_from_list
from tests.gui.types import Clipboard, DisplayMap, TmpMemory
from tests.gui.utils import LoginPage, Modals, OnePage, Onepanel
from tests.gui.utils.generic import parse_seq, transform
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.utils import repeat_failed


@wt(
    parsers.re(
        "users? of (?P<browser_id_list>.+?) clicks? on (?P<btn>.+?) "
        "button in (?P<content>welcome|spaces|account management|"
        "storages|provider|member) page in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_on_btn_in_content(
    selenium: SeleniumDrivers, browser_id_list: str, btn: str, content: str
) -> None:
    for browser_id in parse_seq(browser_id_list):
        content = getattr(Onepanel(selenium[browser_id]).content, transform(content))
        getattr(content, transform(btn)).click()


@wt(
    parsers.re(
        "users? of (?P<browser_id_list>.+?) clicks? on "
        '(?P<sub_item>.+?) item in submenu of "(?P<record>.+?)" '
        "item in (?P<sidebar>CLUSTERS) sidebar in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def wt_click_on_subitem_for_item(
    selenium: SeleniumDrivers,
    browser_id_list: str,
    sidebar: str,
    sub_item: str,
    record: str,
    hosts: Hosts,
) -> None:
    record = hosts[record]["name"]
    for browser_id in parse_seq(browser_id_list):
        nav = getattr(Onepanel(selenium[browser_id]).sidebar, transform(sidebar))
        nav.items[record].submenu[sub_item].click()


@given(
    parsers.re(
        "users? of (?P<browser_id_list>.+?) clicks? on "
        '(?P<sub_item>.+?) item in submenu of "(?P<record>.+?)" '
        "item in (?P<sidebar>CLUSTERS) sidebar in Onepanel"
    )
)
def g_click_on_subitem_for_item(
    selenium: SeleniumDrivers,
    browser_id_list: str,
    sidebar: str,
    sub_item: str,
    record: str,
    hosts: Hosts,
) -> None:
    wt_click_on_subitem_for_item(
        selenium, browser_id_list, sidebar, sub_item, record, hosts
    )


@wt(
    parsers.re(
        "users? of (?P<browser_id_list>.+?) clicks? on "
        "(?P<sub_item>.+?) item in submenu of item named "
        '"(?P<record>.+?)" in (?P<sidebar>CLUSTERS) sidebar in '
        "Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_on_subitem_for_item_with_name(
    selenium: SeleniumDrivers,
    browser_id_list: str,
    sidebar: str,
    sub_item: str,
    record: str,
) -> None:
    for browser_id in parse_seq(browser_id_list):
        nav = getattr(Onepanel(selenium[browser_id]).sidebar, transform(sidebar))
        nav.items[record].submenu[sub_item].click()


@wt(
    parsers.re(
        'users? of (?P<browser_id_list>.+?) clicks? on "(?P<record>.+?)"'
        " item in (?P<sidebar>CLUSTERS) sidebar in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_on_sidebar_item(
    selenium: SeleniumDrivers,
    browser_id_list: str,
    sidebar: str,
    record: str,
) -> None:
    for browser_id in parse_seq(browser_id_list):
        nav = getattr(Onepanel(selenium[browser_id]).sidebar, transform(sidebar))
        nav.items[record].click()


@wt(
    parsers.parse(
        "user of {browser_id} clicks info button on warning bar in Onepanel page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_info_button_on_warning_bar(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    OnePage(selenium[browser_id]).warning_bar.info()


@wt(parsers.parse("user of {browser_id} clicks open in onezone in modal"))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_open_in_onezone_in_modal(selenium: SeleniumDrivers, browser_id: str) -> None:
    modal = Modals(selenium[browser_id])
    modal.emergency_interface.open_in_onezone()


@wt(parsers.parse("user of {browser_id} clicks open in onezone in Onepanel login page"))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_open_in_onezone(selenium: SeleniumDrivers, browser_id: str) -> None:
    LoginPage(selenium[browser_id]).open_in_onezone()


@wt(
    parsers.parse(
        'user of {browser_id} sees that {age} "{record}" is not '
        "working in clusters sidebar"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_not_working_in_clusters_sidebar(
    selenium: SeleniumDrivers,
    browser_id: str,
    age: str,
    record: str,
    hosts: Hosts,
    tmp_memory: TmpMemory,
) -> None:
    sidebar = "CLUSTERS"
    nav = getattr(Onepanel(selenium[browser_id]).sidebar, transform(sidebar))
    items = nav.get_all_items(selenium[browser_id])
    item = get_old_or_new_cluster_record_from_list(
        record, items, age, tmp_memory, hosts
    )
    assert item.is_not_working(), f"{record} is working in clusters sidebar"


@wt(parsers.parse('user of {browser_id} sees Overview page of "{cluster}" cluster'))
@repeat_failed(timeout=WAIT_BACKEND * 2)
def assert_overview_page_of_cluster(
    selenium: SeleniumDrivers, browser_id: str, cluster: str, hosts: Hosts
) -> None:
    found = Onepanel(selenium[browser_id]).content.overview.cluster_name
    expected = hosts[cluster]["name"]
    assert found == expected, f"Overview of {expected} not visible"


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "{link}" link in {view_name} view in Onepanel'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_sidebar_submenu_link(
    selenium: SeleniumDrivers, browser_id: str, view_name: str
) -> None:
    nav = getattr(Onepanel(selenium[browser_id]).content, transform(view_name))
    nav.documentation_link.click()


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "{link}" link at subdomain delegation section'
        " in {view_name} view in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_sidebar_submenu_subdomain_delegation_link(
    selenium: SeleniumDrivers, browser_id: str, view_name: str
) -> None:
    nav = getattr(Onepanel(selenium[browser_id]).content, transform(view_name))
    nav.subdomain_delegation_documentation_link.click()


@wt(
    parsers.parse(
        'user of {browser_id} checks "{toggle}" toggle in {view_name} view in Onepanel'
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_toggle_in_onepanel_view(
    selenium: SeleniumDrivers, browser_id: str, view_name: str, toggle: str
) -> None:
    nav = getattr(Onepanel(selenium[browser_id]).content, transform(view_name))
    getattr(nav, transform(toggle.replace("-", "_"))).check()


@wt(
    parsers.parse(
        'user of {browser_id} sees that "{toggle}" toggle is {option} in {view_name}'
        " view in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_toggle_checked_in_onepanel_view(
    selenium: SeleniumDrivers,
    browser_id: str,
    view_name: str,
    toggle: str,
    option: str,
) -> None:
    nav = getattr(Onepanel(selenium[browser_id]).content, transform(view_name))
    toggle_elem = getattr(nav, transform(toggle.replace("-", "_")))
    assert getattr(
        toggle_elem, f"is_{option}"
    )(), f"toggle {toggle} is not {option} in {view_name}"


@wt(
    parsers.parse(
        'user of {browser_id} sees that "{label}" is "{label_content}" in {view_name}'
        " view in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_label_content_in_onepanel_view(
    selenium: SeleniumDrivers,
    browser_id: str,
    view_name: str,
    label: str,
    label_content: str,
) -> None:
    nav = getattr(Onepanel(selenium[browser_id]).content, transform(view_name))
    actual_label = getattr(nav, transform(label))
    err_msg = f"{label} should be {label_content} but is {actual_label}"
    assert actual_label == label_content, err_msg


@wt(
    parsers.parse(
        'user of {browser_id} sees that "{label}" ends with "{suffix}" in {view_name}'
        " view in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_label_ends_with_in_onepanel_view(
    selenium: SeleniumDrivers,
    browser_id: str,
    view_name: str,
    label: str,
    suffix: str,
) -> None:
    nav = getattr(Onepanel(selenium[browser_id]).content, transform(view_name))
    actual_label = getattr(nav, transform(label))
    err_msg = f"{label} should end with {suffix} but it is {actual_label}"
    assert actual_label.endswith(suffix), err_msg


@wt(
    parsers.parse(
        "user of {browser_id} sees that {host} {domain_type} domain is included in"
        ' "{label}" in {view_name} view in Onepanel'
    )
)
@repeat_failed(timeout=WAIT_BACKEND * 2)
def assert_label_contains_prov_domain_in_onepanel_view(
    selenium: SeleniumDrivers,
    browser_id: str,
    host: str,
    label: str,
    view_name: str,
    hosts: Hosts,
) -> None:
    nav = getattr(Onepanel(selenium[browser_id]).content, transform(view_name))
    actual_label = getattr(nav, transform(label))
    expected_domain = hosts[host]["hostname"]
    err_msg = f"Expected domain: {expected_domain} is not in {actual_label}"
    assert expected_domain in actual_label, err_msg


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) sees "(?P<warning>.*)" warning in '
        r"DNS names section in (?P<view_name>\w+( \w+)?) view in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_BACKEND)
def assert_warning_in_dns_names_in_onepanel_view(
    selenium: SeleniumDrivers, browser_id: str, warning: str, view_name: str
) -> None:
    nav = getattr(Onepanel(selenium[browser_id]).content, transform(view_name))
    actual_warning = nav.dns_names_warning
    warning = warning.replace("\\", "")
    err_msg = f"Actual warning {actual_warning} does not match expected {warning}"
    assert warning in actual_warning, err_msg


@wt(
    parsers.parse(
        'user of {browser_id} sees {property_name} is "{property_value}" in info'
        " tile in {view_name} view in Onepanel"
    )
)
def assert_value_in_info_tile_in_overview_onepanel_view(
    selenium: SeleniumDrivers,
    browser_id: str,
    view_name: str,
    property_name: str,
    property_value: str,
    clipboard: Clipboard,
    displays: DisplayMap,
) -> None:
    nav = getattr(Onepanel(selenium[browser_id]).content, transform(view_name))
    properties = nav.tile_info.properties
    for _property in properties:
        if _property.name != property_name:
            continue
        if _property.value == "":
            _property.copy()
            value = clipboard.paste(display=displays[browser_id])
        else:
            value = _property.value
        assert (
            value == property_value
        ), f"Expected {property_name} to be {property_value}, but got {value}"
        break
