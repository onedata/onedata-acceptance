"""This module contains meta steps for operations on clusters in Onezone
using web GUI
"""

__author__ = "Agnieszka Warchol"
__copyright__ = "Copyright (C) 2019 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from tests.gui.steps.onezone.members import *
from tests.utils.utils import repeat_failed
from tests.gui.steps.onezone.spaces import click_on_option_in_the_sidebar
from tests.gui.steps.onezone.clusters import (click_on_record_in_clusters_menu,
                                              input_join_cluster_token_into_token_input_field)
from tests.gui.steps.onepanel.common import wt_click_on_subitem_for_item
from tests.gui.steps.common.miscellaneous import close_modal
from tests.gui.steps.common.copy_paste import send_copied_item_to_other_users


@wt(parsers.parse('user of {browser_id} invites user of {browser} '
                  'to "{cluster}" cluster'))
@repeat_failed(timeout=WAIT_FRONTEND)
def invite_user_to_cluster(selenium, browser_id, browser, cluster, oz_page,
                           hosts, onepanel, tmp_memory, displays, clipboard):
    option = 'Clusters'
    sub_item = 'Members'
    button = 'Invite user using token'
    where = option.lower()[:-1]
    member = 'users'
    modal = 'Invite using token'
    item_type = 'token'

    click_on_option_in_the_sidebar(selenium, browser_id, option, oz_page)
    click_on_record_in_clusters_menu(selenium, browser_id, oz_page, cluster,
                                     hosts)
    wt_click_on_subitem_for_item(selenium, browser_id, option,
                                 sub_item, cluster, onepanel, hosts)
    click_on_option_in_members_list_menu(selenium, browser_id, button, cluster,
                                         where, member, oz_page, onepanel)
    copy_token_from_modal(selenium, browser_id)
    close_modal(selenium, browser_id, modal, modals)
    send_copied_item_to_other_users(browser_id, item_type, browser,
                                    tmp_memory, displays, clipboard)


@wt(parsers.parse('user of {browser_id} joins to cluster'))
@repeat_failed(timeout=WAIT_FRONTEND)
def join_to_cluster(selenium, browser_id, oz_page, displays, clipboard):
    option = 'Clusters'
    button = 'join cluster'
    button2 = 'join the cluster'

    click_on_option_in_the_sidebar(selenium, browser_id, option, oz_page)
    click_button_in_cluster_menu(selenium, browser_id, oz_page, button)
    input_join_cluster_token_into_token_input_field(selenium, browser_id,
                                                    oz_page, displays,
                                                    clipboard)
    click_button_in_cluster_menu(selenium, browser_id, oz_page, button2)

