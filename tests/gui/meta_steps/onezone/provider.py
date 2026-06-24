"""Utils and fixtures to facilitate operations on providers in Onezone
using web GUI
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"


from tests.gui.steps.common.copy_paste import send_copied_item_to_other_users
from tests.gui.steps.common.docker import wt_assert_file_in_path_with_content
from tests.gui.steps.common.notifies import notify_visible_with_text
from tests.gui.steps.common.url import refresh_site
from tests.gui.steps.onepanel.spaces import (
    wt_clicks_on_btn_in_cease_support_modal,
    wt_clicks_on_understand_risk_in_cease_support_modal,
)
from tests.gui.steps.onezone.clusters import (
    click_button_in_cluster_page,
    copy_registration_cluster_token,
)
from tests.gui.steps.onezone.providers import (
    assert_provider_hostname_matches_known_domain,
    assert_provider_hostname_matches_test_hostname,
    assert_provider_is_not_in_providers_list_in_data_sidebar,
    click_on_cease_support_in_menu_of_provider_on_providers_list,
    click_on_menu_button_of_provider_on_providers_list,
    click_on_provider_in_providers_sidebar_with_provider_name,
)
from tests.gui.steps.onezone.spaces import click_on_option_in_the_sidebar
from tests.gui.types import Clipboard, TmpMemory
from tests.types import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import parsers, wt


def assert_provider_has_name_and_hostname_in_oz_gui(
    selenium: SeleniumDrivers,
    user: str,
    provider_name: str,
    domain_provider: str,
    hosts: Hosts,
    with_refresh: bool = False,
    test_domain: bool = False,
) -> None:
    option = "Data"

    if with_refresh:
        refresh_site(selenium, user)

    click_on_option_in_the_sidebar(selenium, user, option)
    click_on_provider_in_providers_sidebar_with_provider_name(
        selenium, user, provider_name
    )

    if test_domain:
        request = selenium["request"]
        displays = request.getfixturevalue("displays")
        clipboard = request.getfixturevalue("clipboard")
        assert_provider_hostname_matches_test_hostname(
            selenium,
            user,
            domain_provider,
            hosts,
            displays,
            clipboard,
        )
    else:
        assert_provider_hostname_matches_known_domain(
            selenium, user, domain_provider, hosts
        )


def assert_there_is_no_provider_in_oz_gui(
    selenium: SeleniumDrivers, user: str, provider_name: str, hosts: Hosts
) -> None:
    option = "Data"

    refresh_site(selenium, user)
    click_on_option_in_the_sidebar(selenium, user, option)
    assert_provider_is_not_in_providers_list_in_data_sidebar(
        selenium, user, provider_name, hosts
    )


def send_copied_invite_token_in_oz_gui(
    selenium: SeleniumDrivers,
    user: str,
    browser_list: str,
    tmp_memory: TmpMemory,
    displays: dict[str, str],
    clipboard: Clipboard,
) -> None:
    item_type = "token"
    button = "add new provider cluster"

    click_button_in_cluster_page(selenium, user, button)
    copy_registration_cluster_token(selenium, user)
    send_copied_item_to_other_users(
        user, item_type, browser_list, tmp_memory, displays, clipboard
    )


@wt(
    parsers.parse(
        'user of {browser_id} revokes space support of "{provider}" '
        "provider in oneproviders list in data sidebar"
    )
)
def revoke_support_of_provider_in_list(
    selenium: SeleniumDrivers, browser_id: str, provider: str, hosts: Hosts
) -> None:
    driver = selenium[browser_id]
    button = "Cease support"
    notify_type = "info"
    notify_text_regexp = "Ceased.*[Ss]upport.*"

    click_on_menu_button_of_provider_on_providers_list(
        selenium, browser_id, provider, hosts
    )
    click_on_cease_support_in_menu_of_provider_on_providers_list(driver)
    wt_clicks_on_understand_risk_in_cease_support_modal(selenium, browser_id)
    wt_clicks_on_btn_in_cease_support_modal(selenium, browser_id, button)
    notify_visible_with_text(selenium, browser_id, notify_type, notify_text_regexp)


@wt(
    parsers.parse(
        "a file under the path from the user of {browser_id} "
        'clipboard exists, with content "{content}" in provider\'s '
        "storage mount point"
    )
)
def assert_file_with_content_in_provider_storage(
    browser_id: str,
    clipboard: Clipboard,
    displays: dict[str, str],
    content: str,
    hosts: Hosts,
) -> None:
    path = clipboard.paste(display=displays[browser_id])
    wt_assert_file_in_path_with_content(path, content, hosts)
