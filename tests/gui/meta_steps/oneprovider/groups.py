"""Meta steps for basic operations on groups in Oneprovider web GUI
"""

__author__ = "Michal Stanisz"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")

from tests.gui.steps.common.miscellaneous import *
from tests.gui.steps.oneprovider.groups import *
from tests.gui.steps.oneprovider_common import *
from tests.gui.steps.common.copy_paste import *
from tests.gui.steps.modal import *
from tests.gui.steps.common.notifies import notify_visible_with_text
from tests.gui.conftest import WAIT_FRONTEND


def _create_invite_group_token(selenium, user, op_page, parent, tmp_memory,
                               displays, clipboard):
    wt_click_on_the_given_main_menu_tab(selenium, user, 'groups')
    modal_name = "Invite group to the group"
    click_settings_icon_for_group(selenium, user, parent, op_page)
    click_on_item_in_group_settings_dropdown(selenium, user, 'INVITE '
                                             'GROUP', parent, op_page)
    wt_wait_for_modal_to_appear(selenium, user, modal_name, tmp_memory)
    get_token_from_modal(selenium, user, tmp_memory)
    click_on_copy_btn_in_modal(selenium, user, tmp_memory)
    send_copied_item_to_other_users(user, 'token', user, tmp_memory, 
                                    displays, clipboard)


@repeat_failed(timeout=WAIT_FRONTEND)    
def _try_to_join_group_to_group(selenium, user, child, op_page, tmp_memory, 
                                regexp, notify_type):
    modal_name = "Join a group to group"
    click_settings_icon_for_group(selenium, user, child, op_page)
    click_on_item_in_group_settings_dropdown(selenium, user, 'JOIN AS SUBGROUP',
                                             child, op_page)
    wt_wait_for_modal_to_appear(selenium, user, modal_name, tmp_memory)
    activate_input_box_in_modal(user, '', tmp_memory)
    type_item_into_active_element(selenium, user, 'token', tmp_memory)
    press_enter_on_active_element(selenium, user)
    notify_visible_with_text(selenium, user, notify_type, regexp)
    wt_wait_for_modal_to_disappear(selenium, user, tmp_memory)


def fail_to_add_subgroups_using_op_gui(selenium, user, op_page, parent, group_list,
                                       tmp_memory, displays, clipboard):
    _create_invite_group_token(selenium, user, op_page, parent, tmp_memory, 
                               displays, clipboard)
    for child in parse_seq(group_list):
        regexp = 'Failed to join.*{}.*'.format(child)
        _try_to_join_group_to_group(selenium, user, child, op_page, tmp_memory,
                                    regexp, 'error')


