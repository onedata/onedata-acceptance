"""This module contains meta steps for operations on tokens in Onezone
using web GUI.
"""

__author__ = "Agnieszka Warchol, Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in LICENSE.txt"

import time
from typing import Optional

import yaml

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.meta_steps.oneprovider.data import (
    _click_menu_for_elem_somewhere_in_file_browser,
)
from tests.gui.steps.common.common import (
    close_alert_popup_if_present,
    wait_for_error_modal_to_disappear,
    wait_for_sliding_panel_to_stop_moving,
    wait_till_error_modal_disappear,
)
from tests.gui.steps.modals.modal import (
    assert_error_modal_with_text_appeared,
    click_modal_button,
    close_modal,
    get_error_modal_text,
)
from tests.gui.steps.oneprovider.browser import click_option_in_data_row_menu_in_browser
from tests.gui.steps.oneprovider.common import wait_for_item_to_disappear
from tests.gui.steps.onezone.spaces import click_on_option_in_the_sidebar
from tests.gui.steps.onezone.tokens import (
    assert_alert_on_tokens_page,
    assert_invite_target,
    assert_invite_type,
    assert_token_name,
    assert_token_revoked,
    assert_token_type,
    assert_token_usage_count_value,
    choose_invite_select,
    choose_invite_type_in_oz_token_page,
    choose_token_template,
    choose_token_type_to_create,
    click_and_get_create_token_button,
    click_copy_button_in_token_view,
    click_create_custom_token,
    click_menu_button_of_tokens_page,
    click_on_button_in_tokens_sidebar,
    click_on_confirm_button_on_tokens_page,
    click_on_token_containing_name,
    click_on_token_on_tokens_list,
    click_option_for_token_row_menu,
    click_option_in_token_page_menu,
    click_save_button_on_tokens_page,
    get_caveat_by_name,
    get_privileges_tree,
    select_member_from_dropdown,
    select_token_usage_limit,
    show_inactive_caveats,
    switch_toggle_to_change_token,
    type_new_token_name,
    wt_click_on_btn_for_oz_token,
)
from tests.gui.type_definitions import Clipboard, TmpMemory
from tests.gui.utils import Modals, OZLoggedIn, Popups
from tests.gui.utils.common.popups.generic import AlertPopup
from tests.gui.utils.generic import is_element_with_selector_visible_on_page
from tests.gui.utils.onezone.token_caveats import TokenCaveats
from tests.gui.utils.onezone.tokens_page import TokensPage
from tests.type_definitions import Hosts, SeleniumDrivers
from tests.utils.bdd_utils import given, parsers, wt
from tests.utils.user_utils import Users


def _paste_token_into_text_field(
    selenium: SeleniumDrivers, browser_id: str, token: str
) -> None:
    page = OZLoggedIn(selenium[browser_id]).tokens
    page.input_name = token


@wt(parsers.parse("user of {browser_id} pastes copied token into token text field"))
def paste_copied_token_into_text_field(
    selenium: SeleniumDrivers,
    browser_id: str,
    clipboard: Clipboard,
    displays: dict[str, str],
) -> None:
    token = clipboard.paste(display=displays[browser_id])
    _paste_token_into_text_field(selenium, browser_id, token)


@wt(parsers.parse("user of {browser_id} pastes received token into token text field"))
def paste_received_token_into_text_field(
    selenium: SeleniumDrivers, browser_id: str, tmp_memory: TmpMemory
) -> None:
    token = tmp_memory[browser_id]["mailbox"]["token"]
    _paste_token_into_text_field(selenium, browser_id, token)


@wt(
    parsers.parse(
        'user of {browser_id} clicks on "Create token" button '
        'in "Create new token" view'
    )
)
def click_create_token_button_in_create_token_page(
    selenium: SeleniumDrivers, browser_id: str
) -> None:
    driver = selenium[browser_id]
    # prevent clicking when there is ongoing animation, because the click can have no result
    wait_for_sliding_panel_to_stop_moving(
        driver, WAIT_FRONTEND, '[data-one-carousel-slide-id="form"]'
    )
    create_token_button = click_and_get_create_token_button(selenium, browser_id)
    # ensure clicking at create token succeeded
    wait_for_item_to_disappear(create_token_button, driver, timeout=2 * WAIT_FRONTEND)


@wt(
    parsers.parse(
        'user of {browser_id} succeeds to consume token using "Confirm" button'
    )
)
def succeed_to_consume_token_using_confirm_button(
    selenium: SeleniumDrivers,
    browser_id: str,
) -> None:
    driver = selenium[browser_id]
    click_on_confirm_button_on_tokens_page(selenium, browser_id)
    # Case when popup did not appear or the test didn't catch it in time
    if not close_alert_popup_if_present(driver, AlertPopup.SUCCESSFULLY_JOINED):
        assert not is_element_with_selector_visible_on_page(
            driver, ".alert-global.modal.in .modal-dialog"
        ), "Error modal appeared"


def fail_to_consume_token_using_confirm_button(
    selenium: SeleniumDrivers,
    browser_id: str,
    message: str,
    close_error_modal: bool = True,
) -> None:
    driver = selenium[browser_id]
    click_on_confirm_button_on_tokens_page(selenium, browser_id)
    assert_error_modal_with_text_appeared(selenium, browser_id, text=message)
    if close_error_modal:
        wait_for_error_modal_to_disappear(driver)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) succeeds to join "
        r"(?P<option>group|space|inventory|harvester) using received token"
    )
)
def paste_and_consume_received_token(
    selenium: SeleniumDrivers, browser_id: str, tmp_memory: TmpMemory
) -> None:
    _paste_received_token_for_consumption(selenium, browser_id, tmp_memory)
    succeed_to_consume_token_using_confirm_button(selenium, browser_id)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) fails to join "
        r"(?P<option>group|space|inventory|harvester) using received token "
        r"and sees error modal"
    )
)
def paste_and_fail_to_consume_received_token(
    selenium: SeleniumDrivers, browser_id: str, tmp_memory: TmpMemory
) -> None:
    _paste_received_token_for_consumption(selenium, browser_id, tmp_memory)
    fail_to_consume_token_using_confirm_button(
        selenium,
        browser_id,
        message="is invalid",
        close_error_modal=False,
    )


@wt(
    parsers.parse(
        "user of {browser_id} closes error modal with info about "
        'invalid target with id of "{target_name}" {target_type}'
    )
)
def assert_invalid_id_in_error_modal_and_close_modal(
    selenium: SeleniumDrivers,
    browser_id: str,
    target_name: str,
    target_type: str,
    groups: dict[str, str],
    spaces: dict[str, str],
    inventories: dict[str, str],
    harvesters: dict[str, str],
) -> None:
    driver = selenium[browser_id]
    error_modal = Modals(driver).error
    modal_text = get_error_modal_text(selenium, browser_id)
    error_message = (
        f"There is no info about id of invalid target {target_name} in error modal"
    )
    wait_till_error_modal_disappear(
        driver, ".alert-global.modal.in .modal-dialog", lambda _: error_modal.close
    )
    match target_type:
        case "group":
            assert groups[target_name] in modal_text, error_message
        case "space":
            assert spaces[target_name] in modal_text, error_message
        case "inventory":
            assert inventories[target_name] in modal_text, error_message
        case "harvester":
            assert harvesters[target_name] in modal_text, error_message
        case _:
            raise ValueError(f"Unknown type {target_type}")


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) joins (cluster|group|inventory) using copied "
        r"token"
    )
)
@wt(parsers.parse("user of {browser_id} joins to harvester in Onezone page"))
def consume_token_from_copied_token(
    selenium: SeleniumDrivers,
    browser_id: str,
    clipboard: Clipboard,
    displays: dict[str, str],
) -> None:
    _paste_copied_token_for_consumption(selenium, browser_id, clipboard, displays)
    succeed_to_consume_token_using_confirm_button(selenium, browser_id)


@wt(
    parsers.parse(
        "user of {browser_id} fails to join group using copied token "
        "and sees error modal"
    )
)
def fail_to_consume_copied_token(
    selenium: SeleniumDrivers,
    browser_id: str,
    clipboard: Clipboard,
    displays: dict[str, str],
) -> None:
    _paste_copied_token_for_consumption(selenium, browser_id, clipboard, displays)
    fail_to_consume_token_using_confirm_button(
        selenium, browser_id, message="Consuming token failed"
    )


def open_consume_token_view(selenium: SeleniumDrivers, browser_id: str) -> None:
    click_on_option_in_the_sidebar(selenium, browser_id, "Tokens")
    click_on_button_in_tokens_sidebar(selenium, browser_id, "Consume token")


def _paste_received_token_for_consumption(
    selenium: SeleniumDrivers, browser_id: str, tmp_memory: TmpMemory
) -> None:
    open_consume_token_view(selenium, browser_id)
    paste_received_token_into_text_field(selenium, browser_id, tmp_memory)


def _paste_copied_token_for_consumption(
    selenium: SeleniumDrivers,
    browser_id: str,
    clipboard: Clipboard,
    displays: dict[str, str],
) -> None:
    open_consume_token_view(selenium, browser_id)
    paste_copied_token_into_text_field(selenium, browser_id, clipboard, displays)


@wt(
    parsers.re(
        r'user of (?P<browser_id>.*) adds group "(?P<elem_name>.*)" '
        r"as subgroup using copied token"
    )
)
@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) adds "
        r'(space|harvester|group) "(?P<elem_name>.*)" '
        r"to (harvester|space|inventory) using copied token"
    )
)
def add_element_with_copied_token(
    selenium: SeleniumDrivers,
    browser_id: str,
    elem_name: str,
    clipboard: Clipboard,
    displays: dict[str, str],
) -> None:
    _open_token_consume_view_for_member_and_paste_token(
        selenium, browser_id, elem_name, clipboard, displays
    )
    succeed_to_consume_token_using_confirm_button(selenium, browser_id)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) fails to add group "
        r'"(?P<elem_name>.*)" as subgroup using copied token '
        r"and sees error modal"
    )
)
@wt(
    parsers.re(
        r"user of (?P<browser_id>.*) fails to add "
        r'(space|harvester|group) "(?P<elem_name>.*)" '
        r"to (harvester|space|inventory) using copied token "
        r"and sees error modal"
    )
)
def fail_to_add_element_with_copied_token(
    selenium: SeleniumDrivers,
    browser_id: str,
    elem_name: str,
    clipboard: Clipboard,
    displays: dict[str, str],
) -> None:
    _open_token_consume_view_for_member_and_paste_token(
        selenium, browser_id, elem_name, clipboard, displays
    )
    fail_to_consume_token_using_confirm_button(
        selenium, browser_id, message="Consuming token failed", close_error_modal=False
    )


def _open_token_consume_view_for_member_and_paste_token(
    selenium: SeleniumDrivers,
    browser_id: str,
    token_consumer_name: str,
    clipboard: Clipboard,
    displays: dict[str, str],
) -> None:
    _paste_copied_token_for_consumption(selenium, browser_id, clipboard, displays)
    select_member_from_dropdown(selenium, browser_id, token_consumer_name)


@wt(
    parsers.parse(
        'user of {browser_id} opens token consume view for "{elem_name}" {elem}, '
        "pastes token and proceeds"
    )
)
def consume_token_for_member(
    selenium: SeleniumDrivers,
    browser_id: str,
    elem_name: str,
    clipboard: Clipboard,
    displays: dict[str, str],
) -> None:
    _open_token_consume_view_for_member_and_paste_token(
        selenium, browser_id, elem_name, clipboard, displays
    )
    succeed_to_consume_token_using_confirm_button(selenium, browser_id)


@wt(
    parsers.parse(
        'user of {browser_id} opens token consume view for "{elem_name}" {elem}, '
        "pastes token, fails to proceed and sees error modal"
    )
)
def fail_to_consume_token_for_member(
    selenium: SeleniumDrivers,
    browser_id: str,
    elem_name: str,
    clipboard: Clipboard,
    displays: dict[str, str],
) -> None:
    _open_token_consume_view_for_member_and_paste_token(
        selenium, browser_id, elem_name, clipboard, displays
    )
    fail_to_consume_token_using_confirm_button(
        selenium, browser_id, message="Consuming token failed", close_error_modal=False
    )


@wt(
    parsers.parse(
        'user of {browser_id} sees alert with text: "{text}" on '
        "tokens page while trying to consume token"
    )
)
def assert_alert_while_consuming_token(
    selenium: SeleniumDrivers,
    browser_id: str,
    clipboard: Clipboard,
    displays: dict[str, str],
    text: str,
) -> None:
    open_consume_token_view(selenium, browser_id)
    paste_copied_token_into_text_field(selenium, browser_id, clipboard, displays)
    assert_alert_on_tokens_page(browser_id, text, selenium)


@wt(parsers.parse("user of {browser_id} consumes token and sees success notify"))
def consume_token_and_see_success_notify(
    selenium: SeleniumDrivers,
    browser_id: str,
    clipboard: Clipboard,
    displays: dict[str, str],
) -> None:
    _paste_copied_token_for_consumption(selenium, browser_id, clipboard, displays)
    click_on_confirm_button_on_tokens_page(selenium, browser_id)
    # sometimes the popup appears and disappears too quickly to be catched
    assert close_alert_popup_if_present(
        selenium[browser_id], AlertPopup.SUCCESSFULLY_JOINED
    ), "Success notify did not appear"


def _create_token_of_type(
    selenium: SeleniumDrivers,
    browser_id: str,
    token_type: str,
    iteration: Optional[int] = None,
) -> None:
    token_name = f"{token_type}_token"
    if iteration:
        token_name = token_name + str(iteration)

    click_on_button_in_tokens_sidebar(selenium, browser_id, "Create new token")
    click_create_custom_token(selenium, browser_id)
    type_new_token_name(selenium, browser_id, token_name)
    choose_token_type_to_create(selenium, browser_id, token_type)

    if token_type == "invite":
        choose_invite_type_in_oz_token_page(
            selenium, browser_id, "Register Oneprovider"
        )
    click_create_token_button_in_create_token_page(selenium, browser_id)
    close_alert_popup_if_present(selenium[browser_id], AlertPopup.TOKEN_CREATED)


@wt(
    parsers.re(
        r"user of (?P<browser_id>.*?) creates (?P<number>\d*?) "
        r"(?P<token_type>.*?) tokens?"
    )
)
def create_number_of_typed_token(
    selenium: SeleniumDrivers, browser_id: str, number: str, token_type: str
) -> None:
    for i in range(int(number)):
        _create_token_of_type(selenium, browser_id, token_type, i)


@wt(
    parsers.parse(
        "user of {browser_id} creates token with following configuration:\n{config}"
    )
)
def create_token_with_config(
    selenium: SeleniumDrivers,
    browser_id: str,
    config: str,
    users: Users,
    groups: dict[str, str],
    hosts: Hosts,
    tmp_memory: TmpMemory,
) -> None:
    """Create invite token according to given config.

    Config format given in yaml is as follows:

            name: token_name                       ---> optional
            type: access/identity/invite
            invite type: type_of_invite
            invite target: target of invite        ---> optional
            usage limit: number > 0 or infinity    ---> optional, default:
                                                                  infinity
            privileges:                            ---> optional
                privilege_type:
                    granted: True/False/Partially
                    privilege subtypes:            ---> always and only when
                                                        granted is Partially
                        privilege_subtype: True/False
            caveats:                               ---> optional
                caveat_type_1:
                    caveat config:
            ...

    Example configuration:

          type: invite
          invite type: Invite harvester to space
          invite target: space1
          usage limit: infinity
          caveats:
            expiration:
                after: count (in minutes)
            region:
                allow: True/False, default True
                region codes:
                    - Europe
                    - Asia
            IP:
              - 127.0.0.1
            consumer:
              - type: group
                by: id
                consumer name: group2
              - type: user
                by: name
                consumer name: user1

    """
    _create_token_with_config(
        selenium,
        browser_id,
        config,
        users,
        groups,
        hosts,
        tmp_memory,
    )


def _create_token_with_config(
    selenium: SeleniumDrivers,
    browser_id: str,
    config: str,
    users: Users,
    groups: dict[str, str],
    hosts: Hosts,
    tmp_memory: TmpMemory,
) -> None:
    click_on_option_in_the_sidebar(selenium, browser_id, "Tokens")
    click_on_button_in_tokens_sidebar(selenium, browser_id, "Create new token")
    click_create_custom_token(selenium, browser_id)

    data = yaml.load(config, yaml.Loader)
    name = data.get("name", False)
    token_type = data["type"]
    invite_type = data.get("invite type", False)
    invite_target = data.get("invite target", False)
    usage_limit = data.get("usage limit", False)
    caveats = data.get("caveats", False)
    privileges = data.get("privileges", False)

    if name:
        type_new_token_name(selenium, browser_id, name)

    choose_token_type_to_create(selenium, browser_id, token_type)

    if invite_type:
        choose_invite_type_in_oz_token_page(selenium, browser_id, invite_type)
    if invite_target:
        choose_invite_select(selenium, browser_id, invite_target, hosts)
    if usage_limit:
        select_token_usage_limit(selenium, browser_id, str(usage_limit))
    if privileges:
        tree = get_privileges_tree(selenium, browser_id)
        tree.set_privileges(selenium, browser_id, privileges)
    if caveats:
        show_inactive_caveats(selenium, browser_id)
        _set_tokens_caveats(
            selenium,
            browser_id,
            caveats,
            users,
            groups,
            hosts,
            tmp_memory,
        )
    click_create_token_button_in_create_token_page(selenium, browser_id)
    close_alert_popup_if_present(selenium[browser_id], AlertPopup.TOKEN_CREATED)


def _set_tokens_caveats(
    selenium: SeleniumDrivers,
    browser_id: str,
    caveats: TokenCaveats,
    users: Users,
    groups: dict[str, str],
    hosts: Hosts,
    tmp_memory: TmpMemory,
) -> None:
    expiration_caveat = caveats.get("expiration")
    region_caveats = caveats.get("region")
    country_caveats = caveats.get("country")
    asn_caveats = caveats.get("ASN")
    ip_caveats = caveats.get("IP")
    consumer_caveats = caveats.get("consumer")
    service_caveats = caveats.get("service")
    interface_caveat = caveats.get("interface")
    readonly_caveat = caveats.get("read only")
    path_caveats = caveats.get("path")
    object_id_caveats = caveats.get("object ID")

    if expiration_caveat:
        caveat = get_caveat_by_name(selenium, browser_id, "expiration")
        caveat.set_expiration_caveat(expiration_caveat, tmp_memory)
    if region_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, "region")
        caveat.set_region_caveats(selenium, browser_id, region_caveats, Popups)
    if country_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, "country")
        caveat.set_country_caveats(selenium, browser_id, country_caveats, Popups)
    if asn_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, "asn")
        caveat.set_asn_caveats(selenium, browser_id, asn_caveats)
    if ip_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, "ip")
        caveat.set_ip_caveats(selenium, browser_id, ip_caveats)
    if consumer_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, "consumer")
        caveat.set_consumer_caveats(
            selenium,
            browser_id,
            Popups,
            consumer_caveats,
            users,
            groups,
            hosts,
            OZLoggedIn,
        )
    if service_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, "service")
        caveat.set_service_caveats(selenium, browser_id, service_caveats, Popups)
    if interface_caveat:
        caveat = get_caveat_by_name(selenium, browser_id, "interface")
        caveat.set_interface_caveat(interface_caveat)
    if readonly_caveat:
        caveat = get_caveat_by_name(selenium, browser_id, "readonly")
        caveat.set_readonly_caveat()
    if path_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, "path")
        caveat.set_path_caveats(path_caveats)
    if object_id_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, "object_id")
        time.sleep(0.5)
        caveat.set_object_id_caveats(object_id_caveats)


@wt(
    parsers.parse(
        "user of {browser_id} sees that created token configuration "
        "is as following:\n{config}"
    )
)
def assert_token_configuration(
    selenium: SeleniumDrivers,
    browser_id: str,
    config: str,
    users: Users,
    groups: dict[str, str],
    hosts: Hosts,
    tmp_memory: TmpMemory,
    spaces: dict[str, str],
) -> None:
    """Assert token is corresponding to given config.

    Config format given in yaml is as follows:

            name: name_of_invite                           ---> optional
            revoked: True/False                            ---> optional
                                                          (False by default)
            type: token_type
            invite type: invite type if token is invite    ---> optional
            invite target: target_name                     ---> optional
            privileges: privileges                         ---> optional
            usage count: count                             ---> optional
            caveats:                                       ---> optional
                caveat_type_1:
                    caveat config:
            ...

    Example configuration:

        name: Token1
        revoked: False
        type: invite
        invite type: Invite harvester to space
        invite target: space1
        caveats:
            expiration:
                set: True/False              <--- not a value, too many
                                                possibilities in time
                                                changes (e.g. end of the
                                                day, month) this value,
                                                if set, is taken from
                                                tmp_memory
            region:
                allow: True/False
                region codes:
                  - Asia
                  - Europe
            consumer:
              - type: group
                by: id
                consumer name: group2
              - type: user
                by: name
                consumer name: user1
    """
    _assert_token_configuration(
        selenium,
        browser_id,
        config,
        users,
        groups,
        hosts,
        tmp_memory,
        spaces,
    )


def assert_token_configuration_gui(
    selenium: SeleniumDrivers,
    browser_id: str,
    config: str,
    users: Users,
    groups: dict[str, str],
    hosts: Hosts,
    tmp_memory: TmpMemory,
    spaces: dict[str, str],
) -> None:
    token_name = yaml.load(config, yaml.Loader)["name"]
    click_on_token_on_tokens_list(selenium, browser_id, token_name)
    _assert_token_configuration(
        selenium,
        browser_id,
        config,
        users,
        groups,
        hosts,
        tmp_memory,
        spaces,
    )


def _assert_token_configuration(
    selenium: SeleniumDrivers,
    browser_id: str,
    config: str,
    users: Users,
    groups: dict[str, str],
    hosts: Hosts,
    tmp_memory: TmpMemory,
    spaces: dict[str, str],
    creation: bool = False,
) -> None:
    data = yaml.load(config, yaml.Loader)
    token_name = data.get("name", False)
    revoked = data.get("revoked", False)
    token_type = data.get("type", False)
    invite_type = data.get("invite type", False)
    invite_target = data.get("invite target", False)
    usage_count = data.get("usage count", False)
    usage_limit = data.get("usage limit", False)
    privileges = data.get("privileges", False)
    caveats = data.get("caveats", False)

    if token_name:
        assert_token_name(selenium, browser_id, token_name)
    assert_token_revoked(selenium, browser_id, revoked)
    if token_type:
        assert_token_type(selenium, browser_id, token_type)
    if invite_type:
        assert_invite_type(selenium, browser_id, invite_type)
    if invite_target:
        assert_invite_target(selenium, browser_id, invite_target, hosts, spaces)
    if usage_count:
        assert_token_usage_count_value(selenium, browser_id, usage_count)
    if usage_limit:
        usage_starter = f"0/{usage_limit}"
        assert_token_usage_count_value(selenium, browser_id, usage_starter)
    if privileges:
        tree = get_privileges_tree(selenium, browser_id)
        tree.assert_privileges(selenium, browser_id, privileges)
    if caveats:
        assert_token_caveats(
            selenium,
            browser_id,
            caveats,
            users,
            groups,
            hosts,
            tmp_memory,
            creation,
        )


def assert_token_caveats(
    selenium: SeleniumDrivers,
    browser_id: str,
    caveats: TokenCaveats,
    users: Users,
    groups: dict[str, str],
    hosts: Hosts,
    tmp_memory: TmpMemory,
    creation: bool,
) -> None:
    expiration_caveat = caveats.get("expiration")
    region_caveats = caveats.get("region")
    country_caveats = caveats.get("country")
    asn_caveats = caveats.get("ASN")
    ip_caveats = caveats.get("IP")
    consumer_caveats = caveats.get("consumer")
    service_caveats = caveats.get("service")
    interface_caveat = caveats.get("interface")
    readonly_caveat = caveats.get("read only")
    path_caveats = caveats.get("path")
    object_id_caveats = caveats.get("object ID")

    if expiration_caveat:
        caveat = get_caveat_by_name(selenium, browser_id, "expiration")
        caveat.assert_expiration_caveat(expiration_caveat, tmp_memory)
    if region_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, "region")
        caveat.assert_region_caveats(region_caveats)
    if country_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, "country")
        caveat.assert_country_caveats(country_caveats)
    if asn_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, "asn")
        caveat.assert_asn_caveats(asn_caveats)
    if ip_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, "ip")
        caveat.assert_ip_caveats(ip_caveats)
    if consumer_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, "consumer")
        caveat.assert_consumer_caveats(consumer_caveats, users, groups, hosts, creation)
    if service_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, "service")
        caveat.assert_service_caveats(service_caveats)
    if interface_caveat:
        caveat = get_caveat_by_name(selenium, browser_id, "interface")
        caveat.assert_interface_caveat(interface_caveat)
    if readonly_caveat:
        caveat = get_caveat_by_name(selenium, browser_id, "readonly")
        caveat.assert_readonly_caveat()
    if path_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, "path")
        caveat.assert_path_caveats(path_caveats)
    if object_id_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, "object_id")
        caveat.assert_object_id_caveats(object_id_caveats)


@wt(parsers.parse('user of {browser_id} revokes token named "{token_name}"'))
def revoke_token(selenium: SeleniumDrivers, browser_id: str, token_name: str) -> None:
    option = "Modify"
    action = "revoke"

    click_on_token_on_tokens_list(selenium, browser_id, token_name)
    click_menu_button_of_tokens_page(selenium, browser_id)
    click_option_in_token_page_menu(selenium, browser_id, option)
    switch_toggle_to_change_token(selenium, browser_id, action)
    click_save_button_on_tokens_page(selenium, browser_id)


@wt(parsers.parse('user of {browser_id} removes token named "{token_name}"'))
def remove_token(selenium: SeleniumDrivers, browser_id: str, token_name: str) -> None:
    btn = "remove"
    button = "Remove"
    modal = "Remove token"

    wt_click_on_btn_for_oz_token(selenium, browser_id, btn, token_name)
    click_modal_button(selenium, browser_id, button, modal)


@wt(parsers.parse("user of {browser_id} removes all tokens"))
def remove_all_tokens(selenium: SeleniumDrivers, browser_id: str) -> None:
    btn = "remove"
    button = "Remove"
    modal = "Remove token"

    driver = selenium[browser_id]
    oz_page = OZLoggedIn(driver)
    oz_page.open_panel(TokensPage)
    tokens = oz_page.tokens.sidebar.tokens
    if len(tokens):
        tokens[0].click()

        for token in OZLoggedIn(driver).tokens.sidebar.tokens:
            token.menu_button.click()
            click_option_for_token_row_menu(driver, btn)
            click_modal_button(selenium, browser_id, button, modal)


@wt(
    parsers.parse(
        "user of {browser_id} creates and checks token with "
        "following configuration:\n{config}"
    )
)
def create_and_check_token(
    browser_id: str,
    config: str,
    selenium: SeleniumDrivers,
    users: Users,
    groups: dict[str, str],
    hosts: Hosts,
    tmp_memory: TmpMemory,
    spaces: dict[str, str],
) -> None:
    _create_token_with_config(
        selenium,
        browser_id,
        config,
        users,
        groups,
        hosts,
        tmp_memory,
    )
    _assert_token_configuration(
        selenium,
        browser_id,
        config,
        users,
        groups,
        hosts,
        tmp_memory,
        spaces,
        creation=True,
    )


def choose_and_revoke_token_in_oz_gui(
    selenium: SeleniumDrivers, browser_id: str, token_name: str
) -> None:
    option = "Tokens"

    click_on_option_in_the_sidebar(selenium, browser_id, option)
    revoke_token(selenium, browser_id, token_name)


@wt(
    parsers.parse(
        'user of {browser_id} creates new token named "{name}" with '
        "basic {template} template"
    )
)
def create_token_with_basic_template(
    selenium: SeleniumDrivers, browser_id: str, name: str, template: str
) -> None:
    button = "Create new token"

    click_on_button_in_tokens_sidebar(selenium, browser_id, button)
    choose_token_template(selenium, browser_id, template)
    type_new_token_name(selenium, browser_id, name)
    click_create_token_button_in_create_token_page(selenium, browser_id)
    close_alert_popup_if_present(selenium[browser_id], AlertPopup.TOKEN_CREATED)


@wt(
    parsers.parse(
        "using web GUI, {user} creates access token with caveats "
        "set for object which ID was copied to clipboard"
    )
)
def create_token_with_copied_object_id(
    displays: dict[str, str],
    clipboard: Clipboard,
    user: str,
    selenium: SeleniumDrivers,
    users: Users,
    groups: dict[str, str],
    hosts: Hosts,
    tmp_memory: TmpMemory,
) -> None:
    option = "Tokens"
    object_id = clipboard.paste(display=displays[user])
    config = (
        f"name: access_token\ntype: access\ncaveats:\n  object ID:\n    -  {object_id}"
    )
    click_on_option_in_the_sidebar(selenium, user, option)
    create_token_with_config(
        selenium,
        user,
        config,
        users,
        groups,
        hosts,
        tmp_memory,
    )


def _copy_object_id(
    displays: dict[str, str],
    clipboard: Clipboard,
    user: str,
    selenium: SeleniumDrivers,
    tmp_memory: TmpMemory,
    name: str,
    space: str,
) -> None:
    option = "Information"
    button = "File ID"
    modal = "File details"

    _click_menu_for_elem_somewhere_in_file_browser(
        selenium, user, name, space, tmp_memory
    )
    click_option_in_data_row_menu_in_browser(selenium, user, option)
    click_modal_button(selenium, user, button, modal)
    close_modal(selenium, user, modal)

    tmp_memory["object_id"] = clipboard.paste(display=displays[user])


@given(
    parsers.parse(
        "using web GUI, {user} creates access token with caveats "
        'set for object ID for "{name}" in '
        r'space "{space}" in {host}'
    )
)
def create_token_with_object_id(
    displays: dict[str, str],
    clipboard: Clipboard,
    user: str,
    selenium: SeleniumDrivers,
    users: Users,
    groups: dict[str, str],
    hosts: Hosts,
    tmp_memory: TmpMemory,
    name: str,
    space: str,
) -> None:

    option = "Tokens"

    _copy_object_id(
        displays,
        clipboard,
        user,
        selenium,
        tmp_memory,
        name,
        space,
    )

    object_id = tmp_memory["object_id"]
    config = (
        f"name: access_token\ntype: access\ncaveats:\n  object ID:\n    -  {object_id}"
    )

    click_on_option_in_the_sidebar(selenium, user, option)
    create_token_with_config(
        selenium,
        user,
        config,
        users,
        groups,
        hosts,
        tmp_memory,
    )
    click_copy_button_in_token_view(selenium, user)
    tmp_memory[user]["token"] = clipboard.paste(display=displays[user])


@wt(parsers.parse('user of {browser_id} copies token "{token_name}" from tokens page'))
def copy_token_and_store_value(
    selenium: SeleniumDrivers,
    browser_id: str,
    token_name: str,
    clipboard: Clipboard,
    displays: dict[str, str],
    tmp_memory: TmpMemory,
) -> None:
    option = "Tokens"
    click_on_option_in_the_sidebar(selenium, browser_id, option)
    click_on_token_containing_name(selenium, browser_id, token_name)
    click_copy_button_in_token_view(selenium, browser_id)
    copied_token = clipboard.paste(display=displays[browser_id])
    tmp_memory["copied_token"] = copied_token
