"""Steps implementation for permissions GUI tests. 
"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = "This software is released under the MIT license cited in " \
              "LICENSE.txt"

import re
import random
import string

import pytest
from selenium.common.exceptions import InvalidElementStateException

from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.utils.generic import parse_seq
from tests.utils.utils import repeat_failed
from tests.utils.bdd_utils import wt, parsers


def _get_index(selenium, browser_id, num, modals, numerals):
    n = numerals[num]
    if n < 0:
        perm = modals(selenium[browser_id]
                      ).details_modal.edit_permissions.acl.permissions
        n += len(perm)
    return n


@wt(parsers.parse('user of {browser_id} selects "{permission_type}" '
                  'permission type in edit permissions panel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def select_permission_type(selenium, browser_id, permission_type, modals):
    driver = selenium[browser_id]
    button_name = f'{permission_type.lower()}_button'
    getattr(modals(driver).details_modal.edit_permissions, button_name).click()


@wt(parsers.parse('user of {browser_id} sees that current permission is '
                  '"{perm}"'))
def check_permission(selenium, browser_id, perm, modals):
    perm_value = modals(selenium[browser_id]
                        ).details_modal.edit_permissions.posix.value
    assert perm_value == perm, ('POSIX permission value {} instead of'
                                ' expected {}'.format(perm_value, perm))


@wt(parsers.parse('user of {browser_id} sets "{perm}" permission code in '
                  'edit permissions panel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def set_posix_permission(selenium, browser_id, perm, modals):
    modals(selenium[browser_id]
           ).details_modal.edit_permissions.posix.value = perm


@wt(parsers.parse('user of {browser_id} fails to set "{perm}" permission code '
                  'in edit permissions panel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def fail_to_set_posix_permission(selenium, browser_id, perm, modals):
    try:
        modals(selenium[browser_id]
               ).details_modal.edit_permissions.posix.value = perm
        raise Exception(f'Fail in setting permission code was expected, but it '
                        f'succeeded')
    except InvalidElementStateException:
        pass


def _change_acl_options(option_list, subject, change):
    for option in parse_seq(option_list):
        if option in ['allow', 'deny']:
            button_name = f'{option}_option'
            getattr(subject, button_name).click()
        else:
            permissions = option.split(':')
            parent_permission_name = (permissions[0].capitalize()
                                      .replace('Acl', 'ACL'))
            parent_permission = subject.acl_permission_group[
                parent_permission_name]

            if len(permissions) == 1:
                getattr(parent_permission.toggle, change)()
            else:
                child_permission = (permissions[1].capitalize()
                                    .replace('acl', 'ACL'))
                parent_permission.expand()
                subject.scroll_to_elem_on_acl_permission_group(
                    parent_permission)
                getattr(parent_permission.permissions[
                            child_permission].toggle, change)()


@wt(parsers.re('user of (?P<browser_id>.*) sets (?P<option_list>.*) options? '
               'in ACL record in edit permissions modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def select_acl_options(selenium, browser_id, option_list, modals, subject):
    # argument 'option_list' is one of the following patterns:
    # [<parent_permission>|<parent_permission>:<child_permission>, ...]
    # all except [<parent_permission>|<parent_permission>:<child_permission>, ...]
    # [allow|deny, <parent_permission>|<parent_permission>:<child_permission>, ...]

    driver = selenium[browser_id]
    change = 'check'
    subject = (modals(driver).details_modal.
               edit_permissions.acl.member_permission_list[subject])

    re_options = re.match("[Aa]ll( except )?(.*)", option_list)
    if re_options:
        option_list = re_options.group(2)

        for parent_permission in subject.acl_permission_group:
            parent_permission.toggle.check()

        change = f'un{change}'

    _change_acl_options(option_list, subject, change)


def assert_fail_to_select_acl_option(selenium, browser_id, option_list,
                                     modals, subject):
    driver = selenium[browser_id]
    subject = (modals(driver).details_modal.
               edit_permissions.acl.member_permission_list[subject])
    option = parse_seq(option_list)[0]
    permissions = option.split(':')
    parent_permission_name = (permissions[0].capitalize().replace('Acl', 'ACL'))
    parent_permission = subject.acl_permission_group[parent_permission_name]
    child_permission = (permissions[1].capitalize().replace('acl', 'ACL'))
    parent_permission.expand()
    subject.scroll_to_elem_on_acl_permission_group(parent_permission)
    child_permission_class = parent_permission.permissions[
        child_permission].name_web_elem.get_attribute('class')
    if 'disabled' not in child_permission_class:
        raise Exception(f'{child_permission} is not disabled and user can '
                        f'change ACL option which is not expected')


@wt(parsers.parse('user of {browser_id} expands select list for {num} ACL '
                  'record in edit permissions modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def expand_acl_modal(selenium, browser_id, num, numerals, modals):
    n = _get_index(selenium, browser_id, num, modals, numerals)

    modals(selenium[browser_id]
           ).details_modal.edit_permissions.acl.permissions[n].expand()


@wt(parsers.parse('user of {browser_id} selects {subject} from subject list '
                  'in ACL record in edit permissions modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def select_acl_subject(selenium, browser_id, subject, modals, popups):
    driver = selenium[browser_id]
    modals(driver).details_modal.edit_permissions.acl.expand_dropdown()
    popups(driver).dropdown.options[subject].click()


@wt(parsers.re('user of (?P<browser_id>.*) sees exactly (?P<val>\d+) ACL '
               'records? in edit permissions panel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_amount_of_acls(selenium, browser_id, modals, val: int):
    driver = selenium[browser_id]
    perm = modals(driver
                  ).details_modal.edit_permissions.acl.member_permission_list
    assert val == len(perm), (f'There are {len(perm)} '
                              f'instead of {val} ACL records')


@wt(parsers.re('user of (?P<browser_id>\w+) sees that (?P<num>\w+) ACL record '
               'has (?P<subject_type>group|user) subject type '
               'in edit permissions modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_subject_type(selenium, browser_id, modals, subject_type, num,
                        numerals):
    n = _get_index(selenium, browser_id, num, modals, numerals)

    assert subject_type == (modals(selenium[browser_id]
                                   ).details_modal.edit_permissions
                            .acl.permissions[n].subject_type()), (
        f'{subject_type} is not subject type in {num} ACL record')


@wt(parsers.re('user of (?P<browser_id>\w+) sees that there is no subject in '
               '(?P<num>\w+) ACL record in edit permissions modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_lack_of_subject(selenium, browser_id, modals, num, numerals):
    n = _get_index(selenium, browser_id, num, modals, numerals)

    perm = modals(selenium[browser_id]
                  ).details_modal.edit_permissions.acl.permissions[n]
    assert re.match('Select a (user|group)', perm.subject_name), (
        f'There is subject named {perm.subject_name}')


@wt(parsers.re('user of (?P<browser_id>\w+) sees that subject (?P<name>name|'
               'type) is editable in (?P<num>\w+) ACL record in edit '
               'permissions modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_acl_record_editable(selenium, browser_id, modals, num, numerals,
                               name):
    n = _get_index(selenium, browser_id, num, modals, numerals)

    perm = modals(selenium[browser_id]
                  ).details_modal.edit_permissions.acl.permissions[n]
    try:
        _ = getattr(perm, '_{}_select'.format(name))
    except RuntimeError:
        raise RuntimeError("Subject {} is not editable in {} ACL record".
                           format(name, num))


@wt(parsers.re('user of (?P<browser_id>\w+) sees that subject (?P<name>name|'
               'type) is not editable in (?P<num>\w+) ACL record in edit '
               'permissions modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_acl_record_not_editable(selenium, browser_id, modals, num, numerals,
                                   name):
    n = _get_index(selenium, browser_id, num, modals, numerals)

    perm = modals(selenium[browser_id]
                  ).details_modal.edit_permissions.acl.permissions[n]
    with pytest.raises(RuntimeError, message="Subject {} is editable in {} ACL"
                                             " record".format(name, num)):
        _ = getattr(perm, '_{}_select'.format(name))


@wt(parsers.re(r'user of (?P<browser_id>\w+) sees that only (?P<option_list>.*)'
               r' privileges? (are|is) set in (?P<num>\w+) ACL record in edit '
               'permissions panel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_set_acl_privileges(selenium, browser_id, modals, num, numerals,
                              option_list):
    driver = selenium[browser_id]
    n = _get_index(selenium, browser_id, num, modals, numerals)

    perm = modals(driver
                  ).details_modal.edit_permissions.acl.member_permission_list[n]
    perm.click()

    options = [x.lower() for x in parse_seq(option_list)]
    is_allow_checked = perm.is_allow_option_checked()
    if options[0] in ['allow', 'deny']:
        if 'deny' in options and is_allow_checked:
            assert False, 'Checked permissions type should be "deny" not "allow"'
        elif 'allow' in options and not is_allow_checked:
            assert False, 'Checked permissions type should be "allow" not "deny"'
        options.pop(0)

    for option in options:
        permissions = option.split(':')
        parent_permission_name = permissions[0].capitalize().replace('Acl',
                                                                     'ACL')
        parent_permission = perm.acl_permission_group[parent_permission_name]
        if len(permissions) == 1:
            assert parent_permission.toggle.is_checked(), (
                f'{parent_permission_name} should be checked')
        else:
            parent_permission.expand()
            child_permission_name = permissions[1].capitalize().replace('acl',
                                                                        'ACL')
            assert (parent_permission.permissions[child_permission_name]
                    .toggle.is_checked()), (f'{child_permission_name} '
                                            f'should be checked')


@wt(parsers.re(r'user of (?P<browser_id>\w+) sees that (?P<num>\w+) ACL record'
               ' in edit permissions panel is set for (?P<type>.*?) '
               '(?P<name>.*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_acl_subject(selenium, browser_id, modals, num, numerals, type, name):
    driver = selenium[browser_id]
    n = _get_index(selenium, browser_id, num, modals, numerals)

    perm = modals(driver
                  ).details_modal.edit_permissions.acl.member_permission_list[n]
    name = name.strip('\"')

    assert perm.subject_type() == type, (f'Subject type is not {type} '
                                         f'in {num} ACL record')
    assert perm.name == name, 'Subject name is not {name} in {num} ACL record'


@wt(parsers.re(r'user of (?P<browser_id>\w+) clicks "(?P<btn>.*)" button in '
               r'(?P<num>.*) ACL record in permissions panel'))
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_btn_in_acl_record(selenium, browser_id, modals, btn, num,
                               numerals, popups):
    driver = selenium[browser_id]
    n = _get_index(selenium, browser_id, num, modals, numerals)

    btn = btn.strip('\"')
    perm = modals(driver
                  ).details_modal.edit_permissions.acl.member_permission_list[n]
    perm.menu_button()
    popups(driver).menu_in_edit_permissions.menu[btn.capitalize()]()


@wt(parsers.re('user of (?P<browser_id>\w+) sees that (?P<subjects>.*) '
               '(is|are) in subject list in ACL record'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_subject_in_list_in_acl_record(selenium, browser_id, subjects, modals,
                                         tmp_memory, popups):
    driver = selenium[browser_id]
    modals(driver).details_modal.edit_permissions.acl.expand_dropdown()
    subject_list = popups(driver).dropdown.options
    for subject in parse_seq(subjects):
        assert subject in subject_list, f'{subject} not found in subjects list'


@wt(parsers.re('user of (?P<browser_id>\w+) does not see (?P<subjects>.*) '
               'in subject list in (?P<num>.*) ACL record'))
def assert_subject_not_in_list_in_acl_record(selenium, browser_id, subjects,
                                             modals, num, numerals):
    n = _get_index(selenium, browser_id, num, modals, numerals)

    perm = modals(selenium[browser_id]
                  ).details_modal.edit_permissions.acl.permissions[n]
    perm.expand()
    subjects_list = [x.text.lower() for x in perm.subjects_list]
    for subject in parse_seq(subjects):
        assert subject.lower() not in subjects_list, ("{} in subjects list in "
                                                      "{} ACL record".format(
            subject, num))
    perm.expand()


def expand_subject_record_in_edit_permissions_modal(selenium, browser_id,
                                                    modals, subject):
    driver = selenium[browser_id]
    modals(driver).details_modal.edit_permissions.acl.member_permission_list[
        subject].click()


def click_on_record_header_in_edit_permissions_modal(selenium, browser_id,
                                                     modals, subject):
    driver = selenium[browser_id]
    modals(driver).details_modal.edit_permissions.acl.member_permission_list[
        subject].header.click()


def check_permission_denied_alert_in_edit_permissions_modal(selenium,
                                                            browser_id, modals):
    edit_permissions_modal = modals(selenium[browser_id]
                                    ).details_modal.edit_permissions
    assert edit_permissions_modal.permission_denied_alert


def check_permissions_list_in_edit_permissions_modal(selenium, browser_id,
                                                     modals):
    driver = selenium[browser_id]
    edit_permissions_modal = modals(driver).details_modal.edit_permissions
    assert len(edit_permissions_modal.acl.member_permission_list) > 0


@wt(parsers.re('user of (?P<browser_id>\w+) sees "no access" tag on '
               '(?P<item_name>.*)'))
def assert_no_access_tag_on_file(browser_id, item_name, tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    err_msg = f'"No access" tag for {item_name} in file browser not visible'
    assert browser.data[item_name].tag_label == "No access", err_msg


@wt(parsers.re('user of (?P<browser_id>\w+) does not see "no access" tag on '
               '(?P<item_name>.*)'))
def assert_not_no_access_tag_on_file(browser_id, item_name, tmp_memory):
    browser = tmp_memory[browser_id]['file_browser']
    err_msg = f'"No access" tag for {item_name} in file browser visible'
    assert not browser.data[item_name].is_tag_visible('no_access'), err_msg


@repeat_failed(timeout=WAIT_FRONTEND)
def get_unknown_user_id_from_acl_entry(selenium, browser_id, modals,
                                       num, numerals):
    driver = selenium[browser_id]
    n = _get_index(selenium, browser_id, num, modals, numerals)
    perm = modals(driver
                  ).details_modal.edit_permissions.acl.member_permission_list[n]
    return perm.subject_id
