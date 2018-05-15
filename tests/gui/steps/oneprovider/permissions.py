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
from pytest_bdd import parsers, when, then
from tests.gui.conftest import WAIT_FRONTEND
from tests.gui.utils.generic import repeat_failed, parse_seq


def _get_index(selenium, browser_id, num, modals, numerals):
    n = numerals[num]
    if n < 0:
        perm = modals(selenium[browser_id]).edit_permissions.acl.permissions
        n += len(perm)
    return n


@when(parsers.parse('user of {browser_id} selects "{permission_type}" '
                    'permission type in active modal'))
@then(parsers.parse('user of {browser_id} selects "{permission_type}" '
                    'permission type in active modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def select_permission_type(selenium, browser_id, permission_type, modals):
    modals(selenium[browser_id]).edit_permissions.select(permission_type)
   

@when(parsers.parse('user of {browser_id} sees that current permission is '
                    '"{perm}"'))
@then(parsers.parse('user of {browser_id} sees that current permission is '
                    '"{perm}"'))
@repeat_failed(timeout=WAIT_FRONTEND)
def check_permission(selenium, browser_id, perm, modals):
    perm_value = modals(selenium[browser_id]).edit_permissions.posix.value 
    assert perm_value == perm, "POSIX permission value {} instead of'\
                               ' expected {}".format(perm_value, perm)


@when(parsers.parse('user of {browser_id} sets "{perm}" permission code in '
                    'active modal'))
@then(parsers.parse('user of {browser_id} sets "{perm}" permission code in '
                    'active modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def set_permission(selenium, browser_id, perm, modals):
    modals(selenium[browser_id]).edit_permissions.posix.value = perm


@when(parsers.parse('user of {browser_id} sets incorrect {num:d} char '
                    'permission code in active modal'))
@then(parsers.parse('user of {browser_id} sets incorrect {num:d} char '
                    'permission code in active modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def set_incorect_permission(selenium, browser_id, num, numerals, modals):
    random.seed()
    val = random.choice('89')
    for _ in range(num-1):
        val += random.choice(string.digits)
    modals(selenium[browser_id]).edit_permissions.posix.value = val


@when(parsers.parse('user of {browser_id} clicks "Add" in ACL edit '
                    'permissions modal'))
@then(parsers.parse('user of {browser_id} clicks "Add" in ACL edit '
                    'permissions modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def add_acl(selenium, browser_id, modals):
    modals(selenium[browser_id]).edit_permissions.acl.add()


@when(parsers.re('user of (?P<browser_id>.*) sets (?P<option_list>.*) options? '
                 'in (?P<num>\w+) ACL record in edit permissions modal'))
@then(parsers.re('user of (?P<browser_id>.*) sets (?P<option_list>.*) options? '
                 'in (?P<num>\w+) ACL record in edit permissions modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def select_acl_options(selenium, browser_id, option_list, modals, num, numerals):
    n = _get_index(selenium, browser_id, num, modals, numerals)
    perm = modals(selenium[browser_id]).edit_permissions.acl.permissions[n]
    option_list = option_list.strip('\"')
    select_all = False
    re_options = re.match("[Aa]ll( except )?(.*)", option_list)
    if re_options:
        select_all = True
        option_list = re_options.group(2)
    options = [x.lower() for x in parse_seq(option_list)]
    for o in perm.options:
        if o.name.lower() == 'deny' and not 'deny' in options:
            continue
        if select_all ^ o.is_checked():
            o.click()
        if o.name.lower() in options:
            o.click()


@when(parsers.re('user of (?P<browser_id>\w+) selects (?P<subject_type>user|group)'
                 ' as subject type in (?P<num>\w+) ACL record in edit '
                 'permissions modal'))
@then(parsers.re('user of (?P<browser_id>\w+) selects (?P<subject_type>user|group)'
                 ' as subject type in (?P<num>\w+) ACL record in edit '
                 'permissions modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def select_acl_subject_type(selenium, browser_id, subject_type, num, numerals, 
                            modals):
    n = _get_index(selenium, browser_id, num, modals, numerals)
    
    perm = modals(selenium[browser_id]).edit_permissions.acl.permissions[n]
    getattr(perm, 'select_{}'.format(subject_type))()


@when(parsers.parse('user of {browser_id} expands select list for {num} ACL '
                    'record in edit permissions modal'))
@then(parsers.parse('user of {browser_id} expands select list for {num} ACL '
                    'record in edit permissions modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def expand_acl_modal(selenium, browser_id, num, numerals, modals):
    n = _get_index(selenium, browser_id, num, modals, numerals)
    
    modals(selenium[browser_id]).edit_permissions.acl.permissions[n].expand()


@when(parsers.parse('user of {browser_id} selects {subject} from subject list'
                    ' in {num} ACL record in edit permissions modal'))
@then(parsers.parse('user of {browser_id} selects {subject} from subject list'
                    ' in {num} ACL record in edit permissions modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def select_acl_subject(selenium, browser_id, subject, num, numerals, modals):
    n = _get_index(selenium, browser_id, num, modals, numerals)
    perm = modals(selenium[browser_id]).edit_permissions.acl.permissions[n]
    perm.expand()
    for s in perm.subjects_list:
        if s.text == subject:
            s.click()
            break
    else:
        raise RuntimeError("No {} subject in subject list in {} ACL record".
                           format(subject, num))


@when(parsers.re('user of (?P<browser_id>.*) sees exactly (?P<val>\d+) ACL '
                 'records? in edit permissions modal'), 
                 converters=dict(val=int))
@then(parsers.re('user of (?P<browser_id>.*) sees exactly (?P<val>\d+) ACL '
                 'records? in edit permissions modal'), 
                 converters=dict(val=int))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_amount_of_acls(selenium, browser_id, modals, val):        
    perm = modals(selenium[browser_id]).edit_permissions.acl.permissions
    assert val == len(perm), "There are {} instead of {} ACL records".format(
                                len(perm), val)
    

@when(parsers.re('user of (?P<browser_id>\w+) sees that (?P<num>\w+) ACL record'
                 ' has (?P<subject_type>group|user) subject type in edit '
                 'permissions modal'))
@then(parsers.re('user of (?P<browser_id>\w+) sees that (?P<num>\w+) ACL record'
                 ' has (?P<subject_type>group|user) subject type in edit '
                 'permissions modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_subject_type(selenium, browser_id, modals, subject_type, num, numerals):
    n = _get_index(selenium, browser_id, num, modals, numerals)
    
    assert subject_type == (modals(selenium[browser_id]).
                                edit_permissions.
                                acl.
                                permissions[n].
                                subject_type()), ("{} is not subject type in {}"
                                        " ACL record".format(subject_type, num))


@when(parsers.re('user of (?P<browser_id>\w+) sees that there is no subject in '
                 '(?P<num>\w+) ACL record in edit permissions modal'))
@then(parsers.re('user of (?P<browser_id>\w+) sees that there is no subject in '
                 '(?P<num>\w+) ACL record in edit permissions modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_lack_of_subject(selenium, browser_id, modals, num, numerals):
    n = _get_index(selenium, browser_id, num, modals, numerals)
    
    perm = modals(selenium[browser_id]).edit_permissions.acl.permissions[n]
    assert re.match('Select a (user|group)', perm.subject_name), ("There is "
                                "subject named {}".format(perm.subject_name))


@when(parsers.re('user of (?P<browser_id>\w+) sees that subject (?P<name>name|'
                 'type) is editable in (?P<num>\w+) ACL record in edit '
                 'permissions modal'))
@then(parsers.re('user of (?P<browser_id>\w+) sees that subject (?P<name>name|'
                 'type) is editable in (?P<num>\w+) ACL record in edit '
                 'permissions modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_acl_record_editable(selenium, browser_id, modals, num, numerals, 
                               name):
    n = _get_index(selenium, browser_id, num, modals, numerals)
    
    perm = modals(selenium[browser_id]).edit_permissions.acl.permissions[n]
    try:
        _ = getattr(perm, '_{}_select'.format(name))
    except RuntimeError:
        raise RuntimeError("Subject {} is not editable in {} ACL record".
                            format(name, num))


@when(parsers.re('user of (?P<browser_id>\w+) sees that subject (?P<name>name|'
                 'type) is not editable in (?P<num>\w+) ACL record in edit '
                 'permissions modal'))
@then(parsers.re('user of (?P<browser_id>\w+) sees that subject (?P<name>name|'
                 'type) is not editable in (?P<num>\w+) ACL record in edit '
                 'permissions modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_acl_record_not_editable(selenium, browser_id, modals, num, numerals, 
                                   name):
    n = _get_index(selenium, browser_id, num, modals, numerals)
    
    perm = modals(selenium[browser_id]).edit_permissions.acl.permissions[n]
    with pytest.raises(RuntimeError, message="Subject {} is editable in {} ACL"
                                             " record".format(name, num)):
        _ = getattr(perm, '_{}_select'.format(name))
        

@when(parsers.re('user of (?P<browser_id>\w+) sees that only (?P<option_list>.*) '
                 'privileges? (are|is) set in (?P<num>\w+) ACL record in edit '
                 'permissions modal'))
@then(parsers.re('user of (?P<browser_id>\w+) sees that only (?P<option_list>.*) '
                 'privileges? (are|is) set in (?P<num>\w+) ACL record in edit '
                 'permissions modal'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_set_acl_privileges(selenium, browser_id, modals, num, numerals, 
                              option_list):
    n = _get_index(selenium, browser_id, num, modals, numerals)
    
    perm = modals(selenium[browser_id]).edit_permissions.acl.permissions[n]
    
    options = [x.lower() for x in parse_seq(option_list)]
    if not 'deny' in options:
        options.append('allow')
    for o in perm.options:
        if o.is_checked():
            assert o.name.lower() in options, ("{} privilege is set in {} ACL "
                                        "record".format(o.name.lower(), num))
        else:
            assert o.name.lower() not in options, ("{} privilege is not set "
                                "in {} ACL record".format(o.name.lower(), num))


@when(parsers.re('user of (?P<browser_id>\w+) sees that (?P<num>\w+) ACL record'
                 ' in edit permissions modal is set for (?P<type>.*?) '
                 '(?P<name>.*)'))
@then(parsers.re('user of (?P<browser_id>\w+) sees that (?P<num>\w+) ACL record'
                 ' in edit permissions modal is set for (?P<type>.*?) '
                 '(?P<name>.*)'))
@repeat_failed(timeout=WAIT_FRONTEND)
def assert_acl_subject(selenium, browser_id, modals, num, numerals, type, name):
    n = _get_index(selenium, browser_id, num, modals, numerals)
    
    perm = modals(selenium[browser_id]).edit_permissions.acl.permissions[n]
    name = name.strip('\"')

        
    assert perm.subject_type() == type, ("Subject type is not {} in {}"
                                        " ACL record".format(type, num))
    assert perm.subject_name == name, ("Subject name is not {} in {} "
                                        "ACL record".format(name, num))


@when(parsers.re('user of (?P<browser_id>\w+) clicks on (?P<btn>.*) button '
                 'in (?P<num>.*) ACL record in edit permissions modal'))    
@then(parsers.re('user of (?P<browser_id>\w+) clicks on "(?P<btn>.*)" button '
                 'in (?P<num>.*) ACL record in edit permissions modal'))    
@repeat_failed(timeout=WAIT_FRONTEND)
def click_on_btn_in_acl_record(selenium, browser_id, modals, btn, num, numerals):
    n = _get_index(selenium, browser_id, num, modals, numerals)
    
    btn = btn.strip('\"').replace(' ', '_')
    perm = modals(selenium[browser_id]).edit_permissions.acl.permissions[n]
    getattr(perm, btn.lower())()


@when(parsers.re('user of (?P<browser_id>\w+) sees that (?P<subjects>.*) '
                  '(is|are) in subject list in (?P<num>.*) ACL record'))
@then(parsers.re('user of (?P<browser_id>\w+) sees that (?P<subjects>.*) '
                  '(is|are) in subject list in (?P<num>.*) ACL record'))
def assert_subject_in_list_in_acl_record(selenium, browser_id, subjects, modals,
                                         num, numerals):
    n = _get_index(selenium, browser_id, num, modals, numerals)
    
    perm = modals(selenium[browser_id]).edit_permissions.acl.permissions[n]
    perm.expand()
    subjects_list = [x.text.lower() for x in perm.subjects_list]
    for subject in parse_seq(subjects):
        assert subject.lower() in subjects_list,( "{} not in subjects list in "
                                           "{} ACL record".format(subject, num))
    perm.expand()


@when(parsers.re('user of (?P<browser_id>\w+) does not see (?P<subjects>.*) '
                  'in subject list in (?P<num>.*) ACL record'))
@then(parsers.re('user of (?P<browser_id>\w+) does not see (?P<subjects>.*) '
                  'in subject list in (?P<num>.*) ACL record'))
def assert_subject_not_in_list_in_acl_record(selenium, browser_id, subjects, 
                                             modals, num, numerals):
    n = _get_index(selenium, browser_id, num, modals, numerals)
    
    perm = modals(selenium[browser_id]).edit_permissions.acl.permissions[n]
    perm.expand()
    subjects_list = [x.text.lower() for x in perm.subjects_list]
    for subject in parse_seq(subjects):
        assert subject.lower() not in subjects_list,( "{} in subjects list in "
                                           "{} ACL record".format(subject, num))
    perm.expand()

