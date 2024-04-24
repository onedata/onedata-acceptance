"""This module contains meta steps for operations on members page in Onezone
using web GUI
"""

__author__ = "Katarzyna Such"
__copyright__ = "Copyright (C) 2021 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.steps.onezone.members import (
    set_privileges_in_members_subpage, click_element_in_members_list,
    assert_privileges_in_members_subpage, click_on_option_in_members_list_menu,
    assert_member_is_in_parent_members_list)
from tests.gui.steps.onezone.spaces import (
    click_on_option_of_space_on_left_sidebar_menu)
from tests.gui.steps.modals.modal import (
    assert_error_modal_with_text_appeared, assert_element_text_in_modal)


def fail_to_set_privileges_using_op_gui(user, space_name, member_name,
                                        member_type, config, selenium, onepanel,
                                        oz_page):
    button = 'Members'
    option = 'sets'
    list_type = 'users'
    where = 'space'
    text = 'insufficient privileges'
    click_on_option_of_space_on_left_sidebar_menu(
        selenium, user, space_name, button, oz_page)
    click_element_in_members_list(selenium, user, member_name,
                                  oz_page, where, list_type, onepanel)
    set_privileges_in_members_subpage(selenium, user, member_name,
                                      member_type, where, config, onepanel,
                                      oz_page, option)
    assert_error_modal_with_text_appeared(selenium, user, text)


def assert_privileges_in_space_using_op_gui(user, space_name, member_name,
                                            member_type, config, selenium,
                                            onepanel, oz_page):
    option = 'Members'
    list_type = 'users'
    where = 'space'
    click_on_option_of_space_on_left_sidebar_menu(selenium, user,
                                                  space_name, option,
                                                  oz_page)
    click_element_in_members_list(selenium, user, member_name,
                                  oz_page, where, list_type, onepanel)
    assert_privileges_in_members_subpage(selenium, user, member_name,
                                         member_type, where, config,
                                         onepanel, oz_page, True)


def fail_to_create_invitation_in_space_using_op_gui(user, space_name, popups,
                                                    modals, selenium, onepanel,
                                                    oz_page):
    option = 'Members'
    button = 'Invite user using token'
    where = 'space'
    member = 'users'
    modal = 'Invite using token'
    text = 'This resource could not be loaded'
    element = 'alert'
    click_on_option_of_space_on_left_sidebar_menu(selenium, user,
                                                  space_name, option,
                                                  oz_page)
    click_on_option_in_members_list_menu(selenium, user, button,
                                         where, member, oz_page, onepanel,
                                         popups)
    assert_element_text_in_modal(selenium, user, modals, modal, text, element)


def assert_not_user_in_space_using_op_gui(user, space_name, member_name,
                                          selenium, onepanel, oz_page):
    option = 'does not see'
    member_type = 'user'
    parent_type = 'space'
    assert_member_is_in_parent_members_list(selenium, user, option,
                                            member_name, member_type,
                                            space_name, parent_type,
                                            oz_page, onepanel)


def assert_group_in_space_using_op_gui(selenium, user, space_name, oz_page,
                                       group_name, onepanel):
    option1 = 'Members'
    option2 = 'sees'
    member_type = 'group'
    parent_type = 'space'
    click_on_option_of_space_on_left_sidebar_menu(selenium, user,
                                                  space_name, option1,
                                                  oz_page)
    assert_member_is_in_parent_members_list(selenium, user, option2,
                                            group_name, member_type,
                                            space_name, parent_type,
                                            oz_page, onepanel)
