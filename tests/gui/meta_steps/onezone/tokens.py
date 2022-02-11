"""This module contains meta steps for operations on tokens in Onezone
using web GUI.
"""

__author__ = "Agnieszka Warchol, Natalia Organek"
__copyright__ = "Copyright (C) 2020 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

import yaml

from tests.gui.meta_steps.oneprovider.data import (
    _click_menu_for_elem_somewhere_in_file_browser)
from tests.gui.steps.common.notifies import notify_visible_with_text
from tests.gui.steps.modal import (
    assert_error_modal_with_text_appeared, click_modal_button, close_modal)
from tests.gui.steps.oneprovider.file_browser import (
    click_option_in_data_row_menu_in_file_browser)
from tests.gui.steps.onezone.spaces import click_on_option_in_the_sidebar
from tests.gui.steps.onezone.tokens import *
from tests.gui.steps.onezone.tokens import click_option_for_token_row_menu
from tests.utils.bdd_utils import wt, parsers, given
from tests.utils.utils import repeat_failed


def _paste_token_into_text_field(selenium, browser_id, oz_page, token):
    page = oz_page(selenium[browser_id])['tokens']
    page.input_name = token


@wt(parsers.parse('user of {browser_id} pastes copied token '
                  'into token text field'))
@repeat_failed(timeout=WAIT_BACKEND)
def paste_copied_token_into_text_field(selenium, browser_id, oz_page, clipboard,
                                       displays):
    token = clipboard.paste(display=displays[browser_id])
    _paste_token_into_text_field(selenium, browser_id, oz_page, token)


@wt(parsers.parse('user of {browser_id} pastes received token '
                  'into token text field'))
def paste_received_token_into_text_field(selenium, browser_id,
                                         oz_page, tmp_memory):
    token = tmp_memory[browser_id]['mailbox']['token']
    _paste_token_into_text_field(selenium, browser_id, oz_page, token)


@wt(parsers.re('user of (?P<browser_id>.*) joins (?P<option>group|space) using '
               'received token'))
def consume_received_token(selenium, browser_id, oz_page, tmp_memory):
    option = 'Tokens'
    button = 'Consume token'

    click_on_option_in_the_sidebar(selenium, browser_id, option, oz_page)
    click_on_button_in_tokens_sidebar(selenium, browser_id, oz_page, button)
    paste_received_token_into_text_field(selenium, browser_id, oz_page,
                                         tmp_memory)
    click_on_join_button_on_tokens_page(selenium, browser_id, oz_page)


@wt(parsers.parse('user of {browser_id} joins group using copied token'))
@wt(parsers.parse('user of {browser_id} joins to harvester in Onezone page'))
def consume_token_from_copied_token(selenium, browser_id, oz_page, clipboard,
                                    displays):
    option = 'Tokens'
    button = 'Consume token'

    click_on_option_in_the_sidebar(selenium, browser_id, option, oz_page)
    click_on_button_in_tokens_sidebar(selenium, browser_id, oz_page, button)
    paste_copied_token_into_text_field(selenium, browser_id, oz_page, clipboard,
                                       displays)
    click_on_join_button_on_tokens_page(selenium, browser_id, oz_page)


@wt(parsers.parse('user of {browser_id} adds group "{elem_name}" as subgroup '
                  'using copied token'))
@wt(parsers.re('user of (?P<browser_id>.*) adds '
               '(space|harvester|group) "(?P<elem_name>.*)" '
               'to (harvester|space) using copied token'))
@repeat_failed(timeout=WAIT_FRONTEND)
def add_element_with_copied_token(selenium, browser_id, elem_name, oz_page,
                                  clipboard, displays, modals):
    option = 'Tokens'
    button = 'Consume token'

    click_on_option_in_the_sidebar(selenium, browser_id, option, oz_page)
    click_on_button_in_tokens_sidebar(selenium, browser_id, oz_page, button)
    paste_copied_token_into_text_field(selenium, browser_id, oz_page, clipboard,
                                       displays)
    select_member_from_dropdown(selenium, browser_id, elem_name, modals,
                                oz_page)
    click_on_join_button_on_tokens_page(selenium, browser_id, oz_page)


@wt(parsers.parse('user of {browser_id} {result} to consume token for '
                  '"{elem_name}" {elem}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def result_to_consume_token_for_elem(selenium, browser_id, oz_page, elem_name,
                                     result, clipboard, displays, modals):
    add_element_with_copied_token(selenium, browser_id, elem_name, oz_page,
                                  clipboard, displays, modals)
    _result_to_consume_token(selenium, browser_id, result, modals)


@wt(parsers.parse('user of {browser_id} {result} to consume token'))
@repeat_failed(timeout=WAIT_FRONTEND)
def result_to_consume_token(selenium, browser_id, oz_page, result, clipboard,
                            displays, modals):
    consume_token_from_copied_token(selenium, browser_id, oz_page, clipboard,
                                    displays)
    _result_to_consume_token(selenium, browser_id, result, modals)


def _result_to_consume_token(selenium, browser_id, result, modals):
    if result == 'succeeds':
        notify_type = 'success'
        text_regexp = '.*joined.*'

        notify_visible_with_text(selenium, browser_id, notify_type, text_regexp)
    else:
        text = 'Consuming token failed'
        button = 'Close'
        modal = 'Error'

        assert_error_modal_with_text_appeared(selenium, browser_id, text)
        click_modal_button(selenium, browser_id, button, modal, modals)


def _create_token_of_type(selenium, browser_id, token_type, oz_page, popups,
                          iteration=None):
    button = 'Create new token'
    token_name = f'{token_type}_token'
    if iteration:
        token_name = token_name + str(iteration)

    click_on_button_in_tokens_sidebar(selenium, browser_id, oz_page, button)
    click_create_custom_token(selenium, browser_id, oz_page)
    type_new_token_name(selenium, browser_id, oz_page, token_name)
    choose_token_type_to_create(selenium, browser_id, oz_page, token_type)
    if token_type == 'invite':
        invite_type = 'Register Oneprovider'
        choose_invite_type_in_oz_token_page(selenium, browser_id, oz_page,
                                            invite_type, popups)
    click_create_token_button_in_create_token_page(selenium, browser_id,
                                                   oz_page)


@wt(parsers.re(r'user of (?P<browser_id>.*?) creates (?P<number>\d*?) '
               r'(?P<token_type>.*?) tokens?'))
def create_number_of_typed_token(selenium, browser_id, number: int, token_type,
                                 oz_page, popups):
    for i in range(number):
        _create_token_of_type(selenium, browser_id, token_type, oz_page,
                              popups, i)


@wt(parsers.parse('user of {browser_id} creates token with following '
                  'configuration:\n{config}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def create_token_with_config(selenium, browser_id, config, oz_page,
                             popups, users, groups, hosts, tmp_memory):
    """Create invite token according to given config.

    Config format given in yaml is as follow:

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
    _create_token_with_config(selenium, browser_id, config, oz_page,
                              popups, users, groups, hosts, tmp_memory)


def _create_token_with_config(selenium, browser_id, config, oz_page,
                              popups, users, groups, hosts, tmp_memory):
    button = 'Create new token'
    click_on_button_in_tokens_sidebar(selenium, browser_id, oz_page, button)
    click_create_custom_token(selenium, browser_id, oz_page)

    data = yaml.load(config)
    name = data.get('name', False)
    token_type = data['type']
    invite_type = data.get('invite type', False)
    invite_target = data.get('invite target', False)
    usage_limit = data.get('usage limit', False)
    caveats = data.get('caveats', False)
    privileges = data.get('privileges', False)

    if name:
        type_new_token_name(selenium, browser_id, oz_page, name)
    choose_token_type_to_create(selenium, browser_id, oz_page, token_type)
    if invite_type:
        choose_invite_type_in_oz_token_page(selenium, browser_id, oz_page,
                                            invite_type, popups)
    if invite_target:
        choose_invite_select(selenium, browser_id, oz_page, invite_target,
                             hosts, popups)
    if usage_limit:
        select_token_usage_limit(selenium, browser_id, str(usage_limit),
                                 oz_page)
    if privileges:
        tree = get_privileges_tree(selenium, browser_id, oz_page)
        tree.set_privileges(privileges)
    if caveats:
        show_inactive_caveats(selenium, browser_id, oz_page)
        _set_tokens_caveats(selenium, browser_id, oz_page, caveats, popups,
                            users, groups, hosts, tmp_memory)
    click_create_token_button_in_create_token_page(selenium, browser_id,
                                                   oz_page)


def _set_tokens_caveats(selenium, browser_id, oz_page, caveats, popups, users,
                        groups, hosts, tmp_memory):
    expiration_caveat = caveats.get('expiration')
    region_caveats = caveats.get('region', False)
    country_caveats = caveats.get('country', False)
    asn_caveats = caveats.get('ASN', False)
    ip_caveats = caveats.get('IP', False)
    consumer_caveats = caveats.get('consumer', False)
    service_caveats = caveats.get('service', False)
    interface_caveat = caveats.get('interface', False)
    readonly_caveat = caveats.get('read only', False)
    path_caveats = caveats.get('path', False)
    object_id_caveats = caveats.get('object ID', False)

    if expiration_caveat:
        caveat = get_caveat_by_name(selenium, browser_id, oz_page, 'expiration')
        caveat.set_expiration_caveat(expiration_caveat, tmp_memory)
    if region_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, oz_page, 'region')
        caveat.set_region_caveats(selenium, browser_id, region_caveats, popups)
    if country_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, oz_page, 'country')
        caveat.set_country_caveats(selenium, browser_id, country_caveats,
                                   popups)
    if asn_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, oz_page, 'asn')
        caveat.set_asn_caveats(selenium, browser_id, asn_caveats)
    if ip_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, oz_page, 'ip')
        caveat.set_ip_caveats(selenium, browser_id, ip_caveats)
    if consumer_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, oz_page, 'consumer')
        caveat.set_consumer_caveats(selenium, browser_id, popups,
                                    consumer_caveats, users, groups, hosts)
    if service_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, oz_page, 'service')
        caveat.set_service_caveats(selenium, browser_id, service_caveats,
                                   popups)
    if interface_caveat:
        caveat = get_caveat_by_name(selenium, browser_id, oz_page, 'interface')
        caveat.set_interface_caveat(interface_caveat)
    if readonly_caveat:
        caveat = get_caveat_by_name(selenium, browser_id, oz_page, 'readonly')
        caveat.set_readonly_caveat()
    if path_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, oz_page, 'path')
        caveat.set_path_caveats(path_caveats)
    if object_id_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, oz_page, 'object_id')
        caveat.set_object_id_caveats(object_id_caveats)


@wt(parsers.parse('user of {browser_id} sees that created token configuration '
                  'is as following:\n{config}'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_token_configuration(selenium, browser_id, config, oz_page, users,
                               groups, hosts, tmp_memory):
    """Assert token is corresponding to given config.

        Config format given in yaml is as follow:

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
    _assert_token_configuration(selenium, browser_id, config, oz_page, users,
                                groups, hosts, tmp_memory)


@repeat_failed(timeout=WAIT_FRONTEND)
def assert_token_configuration_gui(selenium, browser_id, config, oz_page, users,
                                   groups, hosts, tmp_memory):
    token_name = yaml.load(config)['name']
    click_on_token_on_tokens_list(selenium, browser_id, token_name, oz_page)
    _assert_token_configuration(selenium, browser_id, config, oz_page, users,
                                groups, hosts, tmp_memory)


def _assert_token_configuration(selenium, browser_id, config, oz_page, users,
                                groups, hosts, tmp_memory, creation=False):
    data = yaml.load(config)
    token_name = data.get('name', False)
    revoked = data.get('revoked', False)
    token_type = data.get('type', False)
    invite_type = data.get('invite type', False)
    invite_target = data.get('invite target', False)
    usage_count = data.get('usage count', False)
    usage_limit = data.get('usage limit', False)
    privileges = data.get('privileges', False)
    caveats = data.get('caveats', False)

    if token_name:
        assert_token_name(selenium, browser_id, oz_page, token_name)
    assert_token_revoked(selenium, browser_id, oz_page, revoked)
    if token_type:
        assert_token_type(selenium, browser_id, oz_page, token_type)
    if invite_type:
        assert_invite_type(selenium, browser_id, oz_page, invite_type)
    if invite_target:
        assert_invite_target(selenium, browser_id, oz_page, invite_target,
                             hosts)
    if usage_count:
        assert_token_usage_count_value(selenium, browser_id, usage_count,
                                       oz_page)
    if usage_limit:
        usage_starter = f'0/{usage_limit}'
        assert_token_usage_count_value(selenium, browser_id, usage_starter,
                                       oz_page)
    if privileges:
        tree = get_privileges_tree(selenium, browser_id, oz_page)
        tree.assert_privileges(privileges)
    if caveats:
        assert_token_caveats(selenium, browser_id, oz_page, caveats, users,
                             groups, hosts, tmp_memory, creation)


def assert_token_caveats(selenium, browser_id, oz_page, caveats, users,
                         groups, hosts, tmp_memory, creation):
    expiration_caveat = caveats.get('expiration', False)
    region_caveats = caveats.get('region', False)
    country_caveats = caveats.get('country', False)
    asn_caveats = caveats.get('ASN', False)
    ip_caveats = caveats.get('IP', False)
    consumer_caveats = caveats.get('consumer', False)
    service_caveats = caveats.get('service', False)
    interface_caveat = caveats.get('interface', False)
    readonly_caveat = caveats.get('read only', False)
    path_caveats = caveats.get('path', False)
    object_id_caveats = caveats.get('object ID', False)

    if expiration_caveat:
        caveat = get_caveat_by_name(selenium, browser_id, oz_page, 'expiration')
        caveat.assert_expiration_caveat(expiration_caveat, tmp_memory)
    if region_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, oz_page, 'region')
        caveat.assert_region_caveats(region_caveats)
    if country_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, oz_page, 'country')
        caveat.assert_country_caveats(country_caveats)
    if asn_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, oz_page, 'asn')
        caveat.assert_asn_caveats(asn_caveats)
    if ip_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, oz_page, 'ip')
        caveat.assert_ip_caveats(ip_caveats)
    if consumer_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, oz_page, 'consumer')
        caveat.assert_consumer_caveats(consumer_caveats, users, groups,
                                       hosts, creation)
    if service_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, oz_page, 'service')
        caveat.assert_service_caveats(service_caveats)
    if interface_caveat:
        caveat = get_caveat_by_name(selenium, browser_id, oz_page, 'interface')
        caveat.assert_interface_caveat(interface_caveat)
    if readonly_caveat:
        caveat = get_caveat_by_name(selenium, browser_id, oz_page, 'readonly')
        caveat.assert_readonly_caveat()
    if path_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, oz_page, 'path')
        caveat.assert_path_caveats(path_caveats)
    if object_id_caveats:
        caveat = get_caveat_by_name(selenium, browser_id, oz_page, 'object_id')
        caveat.assert_object_id_caveats(object_id_caveats)


@wt(parsers.parse('user of {browser_id} revokes token named "{token_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def revoke_token(selenium, browser_id, token_name, oz_page, popups):
    option = 'Modify'
    action = 'revoke'

    click_on_token_on_tokens_list(selenium, browser_id, token_name, oz_page)
    click_menu_button_of_tokens_page(selenium, browser_id, oz_page)
    click_option_in_token_page_menu(selenium, browser_id, option, popups)
    switch_toggle_to_change_token(selenium, browser_id, action, oz_page)
    click_save_button_on_tokens_page(selenium, browser_id, oz_page)


@wt(parsers.parse('user of {browser_id} removes token named "{token_name}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_token(selenium, browser_id, token_name, oz_page, popups, modals):
    btn = 'remove'
    button = 'Remove'
    modal = 'Remove token'

    wt_click_on_btn_for_oz_token(selenium, browser_id, btn, token_name, oz_page,
                                 popups)
    click_modal_button(selenium, browser_id, button, modal, modals)


@wt(parsers.parse('user of {browser_id} removes all tokens'))
@repeat_failed(timeout=WAIT_FRONTEND)
def remove_all_tokens(selenium, browser_id, oz_page, popups, modals):
    btn = 'remove'
    button = 'Remove'
    modal = 'Remove token'

    driver = selenium[browser_id]
    tokens = oz_page(driver)['tokens'].sidebar.tokens
    if len(tokens):
        tokens[0].click()

        for token in oz_page(driver)['tokens'].sidebar.tokens:
            token.menu_button.click()
            click_option_for_token_row_menu(driver, btn, popups)
            click_modal_button(selenium, browser_id, button, modal, modals)


@wt(parsers.parse('user of {browser_id} creates and checks token with '
                  'following configuration:\n{config}'))
def create_and_check_token(browser_id, config, selenium, oz_page, popups,
                           users, groups, hosts, tmp_memory):
    _create_token_with_config(selenium, browser_id, config, oz_page, popups,
                              users, groups, hosts, tmp_memory)
    _assert_token_configuration(selenium, browser_id, config, oz_page, users,
                                groups, hosts, tmp_memory, creation=True)


def choose_and_revoke_token_in_oz_gui(selenium, browser_id, token_name,
                                      oz_page, popups):
    option = 'Tokens'

    click_on_option_in_the_sidebar(selenium, browser_id, option, oz_page)
    revoke_token(selenium, browser_id, token_name, oz_page, popups)


@wt(parsers.parse('user of {browser_id} creates new token named "{name}" with '
                  'basic {template} template'))
def create_token_with_basic_template(selenium, browser_id, name, template,
                                     oz_page):
    button = 'Create new token'

    click_on_button_in_tokens_sidebar(selenium, browser_id, oz_page, button)
    choose_token_template(selenium, browser_id, template, oz_page)
    type_new_token_name(selenium, browser_id, oz_page, name)
    click_create_token_button_in_create_token_page(selenium, browser_id,
                                                   oz_page)


def _create_token_using_id(user, selenium, oz_page, popups, users, groups,
                           hosts, tmp_memory, object_id):
    option = 'Tokens'
    config = (f'name: access_token\ntype: access\ncaveats:\n  '
              f'object ID:\n    -  {object_id}')
    click_on_option_in_the_sidebar(selenium, user, option, oz_page)
    create_token_with_config(selenium, user, config, oz_page, popups,
                             users, groups, hosts, tmp_memory)


@wt(parsers.parse('using web GUI, {user} creates access token with caveats '
                  'set for object which ID was copied to clipboard'))
def create_token_using_copied_object_id(displays, clipboard, user, selenium,
                                        oz_page, popups, users, groups, hosts,
                                        tmp_memory):
    object_id = clipboard.paste(display=displays[user])
    _create_token_using_id(user, selenium, oz_page, popups, users, groups,
                           hosts, tmp_memory, object_id)



def _copy_object_id(displays, clipboard, user, selenium, oz_page, tmp_memory,
                    modals, name, space, op_container):
    option = 'Information'
    button = 'File ID'
    modal = 'File details'

    _click_menu_for_elem_somewhere_in_file_browser(selenium, user, name,
                                                   space, tmp_memory, oz_page,
                                                   op_container)
    click_option_in_data_row_menu_in_file_browser(selenium, user, option,
                                                  modals)
    click_modal_button(selenium, user, button, modal, modals)
    close_modal(selenium, user, modal, modals)

    tmp_memory["object_id"] = clipboard.paste(display=displays[user])


@given(parsers.parse('using web GUI, {user} creates access token with caveats '
                     'set for object ID for "{name}" in space '
                     r'"{space}" in {host}'))
def create_token_with_object_id(displays, clipboard, user, selenium, oz_page,
                                popups, users, groups, hosts, tmp_memory,
                                modals, name, space, op_container):

    _copy_object_id(displays, clipboard, user, selenium, oz_page, tmp_memory,
                    modals, name, space, op_container)

    object_id = tmp_memory["object_id"]
    _create_token_using_id(user, selenium, oz_page, popups, users, groups,
                           hosts, tmp_memory, object_id)
    click_copy_button_in_token_view(selenium, user, oz_page)
    tmp_memory[user]['token'] = clipboard.paste(display=displays[user])


@given(parsers.parse('using web GUI, {user} creates token with '
                     'following configuration:\n{config}'))
def given_create_token(user, config, selenium, oz_page, popups, users,
                       groups, hosts, tmp_memory, clipboard, displays):
    create_token_with_config(selenium, user, config, oz_page, popups,
                             users, groups, hosts, tmp_memory)

    click_copy_button_in_token_view(selenium, user, oz_page)
    tmp_memory[user]['token'] = clipboard.paste(display=displays[user])