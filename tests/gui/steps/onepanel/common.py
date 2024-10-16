"""This module contains gherkin steps to run acceptance tests featuring
common operations in onepanel web GUI.
"""

__author__ = "Bartosz Walkowicz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

from tests.gui.conftest import WAIT_BACKEND, WAIT_FRONTEND
from tests.gui.steps.onezone.clusters import get_old_or_new_cluster_record_from_list
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
def wt_click_on_btn_in_content(selenium, browser_id_list, btn, content, onepanel):
    for browser_id in parse_seq(browser_id_list):
        content = getattr(onepanel(selenium[browser_id]).content, transform(content))
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
    selenium, browser_id_list, sidebar, sub_item, record, onepanel, hosts
):
    record = hosts[record]["name"]
    for browser_id in parse_seq(browser_id_list):
        nav = getattr(onepanel(selenium[browser_id]).sidebar, transform(sidebar))
        nav.items[record].submenu[sub_item].click()


@given(
    parsers.re(
        "users? of (?P<browser_id_list>.+?) clicks? on "
        '(?P<sub_item>.+?) item in submenu of "(?P<record>.+?)" '
        "item in (?P<sidebar>CLUSTERS) sidebar in Onepanel"
    )
)
def g_click_on_subitem_for_item(
    selenium, browser_id_list, sidebar, sub_item, record, onepanel, hosts
):
    wt_click_on_subitem_for_item(
        selenium, browser_id_list, sidebar, sub_item, record, onepanel, hosts
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
    selenium, browser_id_list, sidebar, sub_item, record, onepanel
):
    for browser_id in parse_seq(browser_id_list):
        nav = getattr(onepanel(selenium[browser_id]).sidebar, transform(sidebar))
        nav.items[record].submenu[sub_item].click()


@wt(
    parsers.re(
        'users? of (?P<browser_id_list>.+?) clicks? on "(?P<record>.+?)"'
        " item in (?P<sidebar>CLUSTERS) sidebar in Onepanel"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def wt_click_on_sidebar_item(selenium, browser_id_list, sidebar, record, onepanel):
    for browser_id in parse_seq(browser_id_list):
        nav = getattr(onepanel(selenium[browser_id]).sidebar, transform(sidebar))
        nav.items[record].click()


@wt(
    parsers.parse(
        "user of {browser_id} clicks info button on warning bar in Onepanel page"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def click_info_button_on_warning_bar(selenium, browser_id, onepage):
    onepage(selenium[browser_id]).warning_bar.info()


@wt(parsers.parse("user of {browser_id} clicks open in onezone in modal"))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_open_in_onezone_in_modal(selenium, browser_id, modals):
    modal = modals(selenium[browser_id])
    modal.emergency_interface.open_in_onezone()


@wt(parsers.parse("user of {browser_id} clicks open in onezone in Onepanel login page"))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_open_in_onezone(selenium, browser_id, login_page):
    login_page(selenium[browser_id]).open_in_onezone()


@wt(
    parsers.parse(
        'user of {browser_id} sees that {age} "{record}" is not '
        "working in clusters sidebar"
    )
)
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_not_working_in_clusters_sidebar(
    selenium, browser_id, age, record, onepanel, hosts, tmp_memory
):
    sidebar = "CLUSTERS"
    nav = getattr(onepanel(selenium[browser_id]).sidebar, transform(sidebar))
    items = nav.get_all_items(selenium[browser_id])
    item = get_old_or_new_cluster_record_from_list(
        record, items, age, tmp_memory, hosts
    )
    assert item.is_not_working(), f"{record} is working in clusters sidebar"


@wt(parsers.parse('user of {browser_id} sees Overview page of "{cluster}" cluster'))
@repeat_failed(timeout=WAIT_BACKEND * 2)
def assert_overview_page_of_cluster(selenium, browser_id, cluster, onepanel, hosts):
    found = onepanel(selenium[browser_id]).content.overview.cluster_name
    expected = hosts[cluster]["name"]
    assert found == expected, f"Overview of {expected} not visible"
