"""This module contains gherkin steps to run acceptance tests featuring
basic operations on spaces in Onezone using REST API mixed with web GUI.
"""

__author__ = "Michal Cwiertnia"
__copyright__ = "Copyright (C) 2017 ACK CYFRONET AGH"
__license__ = ("This software is released under the MIT license cited in "
               "LICENSE.txt")


from pytest_bdd import when, then, parsers

from tests.mixed.utils.common import NoSuchClientException


@when(parsers.re('using (?P<client>.*), (?P<user>.+?) creates '
                 'spaces? (?P<space_list>.+?) in "(?P<host>.+?)" '
                 'Onezone service'))
@then(parsers.re('using (?P<client>.*), (?P<user>.+?) creates '
                 'spaces? (?P<space_list>.+?) in "(?P<host>.+?)" '
                 'Onezone service'))
def create_spaces_in_oz(client, user, space_list, host, hosts, users, selenium,
                        oz_page, request):

    if client.lower() == 'rest':
        from tests.mixed.steps.rest.onezone.space_management import \
                                                create_spaces_in_oz_using_rest
        create_spaces_in_oz_using_rest(user, users, hosts, host, space_list)
    elif client.lower() == 'web gui':
        from tests.gui.meta_steps.onezone.spaces import \
                                                create_spaces_in_oz_using_gui
        create_spaces_in_oz_using_gui(selenium, user, oz_page, space_list)
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>.+?) leaves spaces? '
                 'named (?P<space_list>.+?) in "(?P<host>.+?)" Onezone '
                 'service'))
def leave_spaces_in_oz(client, request, user, space_list, host,
                       selenium, oz_page, users, hosts, spaces, popups):

    if client.lower() == 'rest':
        from tests.mixed.steps.rest.onezone.space_management import \
                                                leave_spaces_in_oz_using_rest
        leave_spaces_in_oz_using_rest(user, users, host, hosts, space_list,
                                      spaces)
    elif client.lower() == 'web gui':
        from tests.gui.meta_steps.onezone.spaces import \
                                                leave_spaces_in_oz_using_gui
        leave_spaces_in_oz_using_gui(selenium, user, space_list, oz_page, popups)
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>.+?) renames spaces? '
                 'named (?P<space_list>.+?) to (?P<new_names_list>.+?) '
                 'in "(?P<host>.+?)" Onezone service'))
def rename_spaces_in_oz(client, request, user, space_list, new_names_list,
                        host, selenium, oz_page, users, hosts, spaces):

    if client.lower() == 'rest':
        from tests.mixed.steps.rest.onezone.space_management import \
                                                rename_spaces_in_oz_using_rest
        rename_spaces_in_oz_using_rest(user, users, host, hosts,
                                       space_list, new_names_list, spaces)
    elif client.lower() == 'web gui':
        from tests.gui.meta_steps.onezone.spaces import \
                                            rename_spaces_in_oz_using_gui
        rename_spaces_in_oz_using_gui(selenium, user, oz_page, space_list,
                                      new_names_list)
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>.+?) set space named '
                 '"(?P<space_name>.+?)" as home space in "(?P<host>.+?)" '
                 'Onezone service'))
def set_space_as_home_in_oz(client, request, user, space_name, host, selenium,
                            oz_page, users, hosts, spaces, popups):

    if client.lower() == 'rest':
        from tests.mixed.steps.rest.onezone.space_management import \
                                            set_space_as_home_in_oz_using_rest
        set_space_as_home_in_oz_using_rest(user, users, host, hosts, space_name,
                                           spaces)
    elif client.lower() == 'web gui':
        from tests.gui.meta_steps.onezone.spaces import \
                                            set_space_as_home_in_oz_using_gui
        set_space_as_home_in_oz_using_gui(selenium, user, oz_page,
                                          space_name, popups)
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>.+?) removes spaces? '
                 'named (?P<space_list>.+?) in "(?P<host>.+?)" Onezone '
                 'service'))
@then(parsers.re('using (?P<client>.*), (?P<user>.+?) removes spaces? '
                 'named (?P<space_list>.+?) in "(?P<host>.+?)" Onezone '
                 'service'))
def remove_spaces_in_oz(client, request, user, space_list, host, users, hosts,
                        spaces):

    if client.lower() == 'rest':
        from tests.mixed.steps.rest.onezone.space_management import \
                                                remove_spaces_in_oz_using_rest
        remove_spaces_in_oz_using_rest(user, users, host, hosts, space_list,
                                       spaces)
    elif client.lower() == 'web gui':
        from tests.gui.meta_steps.onezone.spaces import \
                                                remove_space_in_oz_using_gui
        remove_space_in_oz_using_gui()
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>.+?) removes '
                 '(?P<user_list>.+?) from space "(?P<space_name>.+?)" in '
                 '"(?P<host>.+?)" Onezone service'))
def delete_users_from_space_in_oz(client, request, user_list, space_name, host,
                                  users, hosts, spaces, user):

    if client.lower() == 'rest':
        from tests.mixed.steps.rest.onezone.space_management import \
                                    delete_users_from_space_in_oz_using_rest
        delete_users_from_space_in_oz_using_rest(user_list, users, host,
                                                 hosts, space_name, spaces,
                                                 user)
    elif client.lower() == 'web gui':
        from tests.gui.meta_steps.onezone.spaces import \
                                    delete_users_from_space_in_oz_using_gui
        delete_users_from_space_in_oz_using_gui()
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>.+?) adds '
                 '(?P<user_list>.+?) to "(?P<space_name>.+?)" in '
                 '"(?P<host>.+?)" Onezone service'))
def add_users_to_space_in_oz(client, request, user_list, space_name, host,
                             users, hosts, spaces, user):

    if client.lower() == 'rest':
        from tests.mixed.steps.rest.onezone.space_management import \
                                            add_users_to_space_in_oz_using_rest
        add_users_to_space_in_oz_using_rest(user_list, users, host, hosts,
                                            space_name, spaces, user)
    elif client.lower() == 'web gui':
        from tests.gui.meta_steps.onezone.spaces import \
                                            add_users_to_space_in_oz_using_gui
        add_users_to_space_in_oz_using_gui()
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>.+?) removes support '
                 'from provider "(?P<provider_name>.+?)" for space named '
                 '"(?P<space_name>.+?)" in "(?P<host>.+?)" Onezone service'))
def remove_provider_support_for_space_in_oz(client, request, user,
                                            provider_name, space_name, host,
                                            selenium, users, hosts, spaces,
                                            admin_credentials, onepanel,
                                            popups):

    if client.lower() == 'rest':
        from tests.mixed.steps.rest.onezone.space_management import \
                            remove_provider_support_for_space_in_oz_using_rest
        remove_provider_support_for_space_in_oz_using_rest(user, users, host,
                                                           hosts, provider_name,
                                                           space_name, spaces,
                                                           admin_credentials)
    elif client.lower() == 'web gui':
        from tests.gui.meta_steps.onezone.spaces import \
                            remove_provider_support_for_space_in_oz_using_gui
        remove_provider_support_for_space_in_oz_using_gui(selenium, user,
                                                          space_name, onepanel,
                                                          popups, hosts)
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>.+?) invites '
                 '(?P<user_list>.+?) to space named "(?P<space_name>.+?)" in '
                 '"(?P<host>.+?)" Onezone service'))
def invite_other_users_to_space(client, request, user, user_list, space_name,
                                host, selenium, tmp_memory, users,
                                hosts, spaces, displays, clipboard, oz_page,
                                onepanel, popups):

    if client.lower() == 'rest':
        from tests.mixed.steps.rest.onezone.space_management import \
                                        invite_otehr_users_to_space_using_rest
        invite_otehr_users_to_space_using_rest(user, users, host, hosts,
                                               space_name, spaces, tmp_memory,
                                               user_list)

    elif client.lower() == 'web gui':
        from tests.gui.meta_steps.onezone.spaces import \
                                        invite_other_users_to_space_using_gui
        invite_other_users_to_space_using_gui(selenium, user, space_name,
                                              user_list, oz_page, tmp_memory,
                                              displays, clipboard,
                                              onepanel, popups)
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user_list>.+?) joins to '
                 'space using received (?P<item_name>.+?) in "(?P<host>.+?)" '
                 'Onezone service'))
def join_space_in_oz(client, request, user_list, item_name, host, selenium,
                     oz_page, tmp_memory, users, hosts):

    if client.lower() == 'rest':
        from tests.mixed.steps.rest.onezone.space_management import \
                                                    join_space_in_oz_using_rest
        join_space_in_oz_using_rest(user_list, users, host, hosts, item_name,
                                    tmp_memory)
    elif client.lower() == 'web gui':
        from tests.gui.meta_steps.onezone.spaces import \
                                                    join_space_in_oz_using_gui
        join_space_in_oz_using_gui(selenium, user_list, oz_page, tmp_memory,
                                   item_name)
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@when(parsers.re(r'using (?P<client>.*), (?P<user>.+?) sees that '
                 'spaces? named (?P<space_list>.+?) (has|have) appeared in '
                 '"(?P<host>.+?)" Onezone service'))
@then(parsers.re(r'using (?P<client>.*), (?P<user>.+?) sees that '
                 'spaces? named (?P<space_list>.+?) (has|have) appeared in '
                 '"(?P<host>.+?)" Onezone service'))
def assert_there_are_spaces_in_oz(client, request, user, space_list, selenium,
                                  oz_page, users, hosts, host):

    if client.lower() == 'web gui':
        from tests.gui.meta_steps.onezone.spaces import \
                                        assert_spaces_have_appeared_in_oz_gui
        assert_spaces_have_appeared_in_oz_gui(selenium, user, oz_page,
                                              space_list)
    elif client.lower() == 'rest':
        from tests.mixed.steps.rest.onezone.space_management import \
                                        assert_spaces_have_appeared_in_oz_rest
        assert_spaces_have_appeared_in_oz_rest(user, users, hosts, host,
                                               space_list)
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@then(parsers.re('using (?P<client>.*), (?P<user>.+?) sees that '
                 'spaces? named (?P<space_list>.+?) (has|have) disappeared '
                 'from "(?P<host>.+?)" Onezone service'))
def assert_there_are_no_spaces_in_oz(client, request, user, space_list, host,
                                     selenium, oz_page, users, spaces, hosts):

    if client.lower() == 'rest':
        from tests.mixed.steps.rest.onezone.space_management import \
                                        assert_there_are_no_spaces_in_oz_rest
        assert_there_are_no_spaces_in_oz_rest(user, users, host, hosts,
                                              space_list, spaces)
    elif client.lower() == 'web gui':
        from tests.gui.meta_steps.onezone.spaces import \
                                        assert_there_are_no_spaces_in_oz_gui
        assert_there_are_no_spaces_in_oz_gui(selenium, user, oz_page,
                                             space_list)
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@then(parsers.re('using (?P<client>.*), (?P<user>.+?) sees that '
                 'spaces? named (?P<space_list>.+?) (has|have) been renamed to '
                 '(?P<new_names_list>.+?) in "(?P<host>.+?)" Onezone service'))
def assert_spaces_have_been_renamed_in_oz(client, request, user, space_list,
                                          new_names_list, host, selenium,
                                          oz_page, users, hosts, spaces):

    if client.lower() == 'rest':
        from tests.mixed.steps.rest.onezone.space_management import \
                                    assert_spaces_have_been_renamed_in_oz_rest
        assert_spaces_have_been_renamed_in_oz_rest(user, users, host, hosts,
                                                   space_list, new_names_list,
                                                   spaces)
    elif client.lower() == 'web gui':
        from tests.gui.meta_steps.onezone.spaces import \
                                    assert_spaces_have_been_renamed_in_oz_gui
        assert_spaces_have_been_renamed_in_oz_gui(selenium, user, oz_page,
                                                  space_list, new_names_list)
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@then(parsers.re('using (?P<client>.*), (?P<user>.+?) sees that space '
                 'named "(?P<space_name>.+?)" has been set as home in '
                 '"(?P<host>.+?)" Onezone service'))
def assert_space_has_been_set_as_home_in_oz(client, request, user, space_name,
                                            host, selenium, oz_page, users,
                                            hosts, spaces):

    if client.lower() == 'rest':
        from tests.mixed.steps.rest.onezone.space_management import \
                                        assert_space_is_home_space_in_oz_rest
        assert_space_is_home_space_in_oz_rest(user, users, host, hosts,
                                              space_name, spaces)
    elif client.lower() == 'web gui':
        from tests.gui.meta_steps.onezone.spaces import \
                                        assert_space_is_home_space_in_oz_gui
        assert_space_is_home_space_in_oz_gui(selenium, user, oz_page,
                                             space_name)
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@then(parsers.re('using (?P<client>.*), (?P<user>.+?) sees that there '
                 '(is|are) no supporting providers? '
                 '(?P<providers_list>.+?) for space named '
                 '"(?P<space_name>.+?)" in "(?P<host>.+?)" Onezone service'))
def assert_there_is_no_provider_for_space_in_oz(client, request, user,
                                                providers_list, space_name,
                                                host, selenium, oz_page, users,
                                                hosts, spaces,
                                                admin_credentials):

    if client.lower() == 'rest':
        from tests.mixed.steps.rest.onezone.space_management import \
                            assert_there_is_no_provider_for_space_in_oz_rest
        assert_there_is_no_provider_for_space_in_oz_rest(user, users, host,
                                                         hosts, space_name,
                                                         spaces, providers_list,
                                                         admin_credentials)
    elif client.lower() == 'web gui':
        from tests.gui.meta_steps.onezone.spaces import \
                            assert_there_is_no_provider_for_space_in_oz_gui
        assert_there_is_no_provider_for_space_in_oz_gui(selenium, user, oz_page,
                                                        space_name)
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@then(parsers.re('using (?P<client>.*), (?P<user>.+?) sees that '
                 '(?P<user_list>.+?) (is|are) members? of '
                 '"(?P<space_name>.+?)" in "(?P<host>.+?)" Onezone service'))
def assert_user_is_member_of_space(client, request, user, user_list,
                                   space_name, host, spaces, users, hosts,
                                   selenium, oz_page, onepanel):

    if client.lower() == 'rest':
        from tests.mixed.steps.rest.onezone.space_management import \
                                            assert_user_is_member_of_space_rest
        assert_user_is_member_of_space_rest(space_name, spaces, user, users,
                                            user_list, host, hosts)
    elif client.lower() == 'web gui':
        from tests.gui.meta_steps.onezone.spaces import \
                                            assert_user_is_member_of_space_gui
        assert_user_is_member_of_space_gui(selenium, user, space_name, oz_page,
                                           user_list, onepanel)
    else:
        raise NoSuchClientException('Client: {} not found.'.format(client))


@when(parsers.re('using (?P<client>.*), (?P<user>.+?) sees provider '
                 '"(?P<provider_name>.+?)" with hostname matches that of '
                 '"(?P<provider>.+?)" provider in "(?P<host>.+?)" Onezone '
                 'service'))
def assert_provider_has_given_name_and_known_hostname_in_oz(client, user,
                                                            provider_name,
                                                            provider, host,
                                                            users, hosts,
                                                            selenium, oz_page,
                                                            modals):

        provider_name = hosts[provider_name]['name']

        if client.lower() == 'rest':
            from tests.mixed.steps.rest.onezone.provider import \
                                assert_provider_has_name_and_hostname_in_oz_rest
            assert_provider_has_name_and_hostname_in_oz_rest(
                user, users, host, hosts, provider_name,
                hosts[provider]['hostname'])
        elif client.lower() == 'web gui':
            from tests.gui.meta_steps.onezone.provider import \
                                assert_provider_has_name_and_hostname_in_oz_gui
            assert_provider_has_name_and_hostname_in_oz_gui(
                selenium, user, oz_page, provider_name, provider, hosts, modals)
        else:
            raise NoSuchClientException('Client: {} not found.'.format(client))
