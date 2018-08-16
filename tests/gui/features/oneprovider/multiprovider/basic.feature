Feature: Oneprovider functionality using multiple providers

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
    And initial spaces configuration in "onezone" Onezone service:
          space1:
              owner: user1
              providers:
                  - oneprovider-1:
                      storage: posix
                      size: 1000000
                  - oneprovider-2:
                      storage: posix
                      size: 1000000
#          space2:
#              owner: user1
#              providers:
#                  - oneprovider-1:
#                      storage: posix
#                      size: 1000000
#                  - oneprovider-2:
#                      storage: posix
#                      size: 1000000
    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service

  Scenario: User creates space in one provider and sees that it was created also in other provider
    # create space
    When user of browser clicks create new space on spaces on left sidebar menu
    And user of browser types "multiprov" on input on create new space page
    And user of browser clicks on create new space button
    And user of browser sees "multiprov" has appeared on spaces
    # check space in first provider
    And user of browser clicks "space1" on spaces on left sidebar menu
    And user of browser clicks Providers of "space1" on left sidebar menu
    And user of browser sees "oneprovider-1" is on the providers list
    And user of browser clicks on "oneprovider-1" provider on left sidebar menu
    And user of browser sees that Oneprovider session has started
    And user of browser sees "multiprov" is in spaces list on onepanel page
    # check space in second provider
    And user of browser clicks on the "providers" tab in main menu sidebar
    And user of browser clicks on "oneprovider-2" provider on left sidebar menu
    Then user of browser sees "multiprov" is in spaces list on onepanel page

  Scenario: User changes name of space in one provider and sees that it was changed also in other provider
    # rename space
    When user of browser clicks "space1" on spaces on left sidebar menu
    And user of browser types "NewNameSpace" on rename input on overview page
    And user of browser presses enter on keyboard
    And user of browser sees "NewNameSpace" has appeared on spaces
    And user of browser sees "space1" has disappeared on spaces

    # check space in first provider
    And user of browser clicks "NewNameSpace" on spaces on left sidebar menu
    And user of browser clicks Providers of "NewNameSpace" on left sidebar menu
    And user of browser sees "oneprovider-1" is on the providers list
    And user of browser clicks on "oneprovider-1" provider on left sidebar menu
    And user of browser sees that Oneprovider session has started
    And user of browser sees "NewNameSpace" is in spaces list on onepanel page
    And user of browser sees "space1" is not in spaces list on onepanel page
    # check space in second provider
    And user of browser clicks on the "providers" tab in main menu sidebar
    And user of browser clicks on "oneprovider-2" provider on left sidebar menu
    Then user of browser sees "NewNameSpace" is in spaces list on onepanel page
    Then user of browser sees "space1" is not in spaces list on onepanel page

# add second space to given or look for text: this provider does not support any space
#  Scenario: User leaves space in one provider and sees that it was leaved from also in other provider
#    When user of browser clicks on the "spaces" tab in main menu sidebar
#
#    And user of browser clicks on settings icon displayed for "space1" item on the spaces sidebar list
#    And user of browser clicks on the "LEAVE SPACE" item in settings dropdown for space named "space1"
#    And user of browser sees that "Leave a space" modal has appeared
#    And user of browser clicks "Yes" confirmation button in displayed modal
#    And user of browser sees an info notify with text matching to: .*space1.*left
#    And user of browser sees that the modal has disappeared
#    And user of browser refreshes site
#    And user of browser sees that space named "space1" has disappeared from the spaces list
#
#    And user of browser clicks on the "providers" tab in main menu sidebar
#    And user of browser sees "space1" has appeared on spaces
#
#    And user of browser clicks on "oneprovider-2" provider on left sidebar menu
#    And user of browser clicks on the "spaces" tab in main menu sidebar
#    Then user of browser sees that space named "space1" has disappeared from the spaces list


  Scenario: User creates group in one provider and sees that it was created also in other provider
    When user of browser clicks "space1" on spaces on left sidebar menu
    And user of browser clicks Providers of "space1" on left sidebar menu
    And user of browser sees "oneprovider-1" is on the providers list
    And user of browser clicks on "oneprovider-1" provider on left sidebar menu
    And user of browser sees that Oneprovider session has started
    # create group
    And user of browser clicks on the "groups" tab in main menu sidebar
    And user of browser clicks on the Create button in groups sidebar header
    And user of browser sees that "Create a new group" modal has appeared
    And user of browser clicks on input box in active modal
    And user of browser types "multiprov" on keyboard
    And user of browser presses enter on keyboard
    And user of browser sees that the modal has disappeared
    And user of browser refreshes site
    And user of browser sees that group named "multiprov" has appeared in the groups list

    And user of browser clicks on the "providers" tab in main menu sidebar
    And user of browser sees "multiprov" is in groups on left sidebar menu
    # check group in second provider
    And user of browser clicks on "oneprovider-2" provider on left sidebar menu
    And user of browser clicks on the "groups" tab in main menu sidebar
    Then user of browser sees that group named "multiprov" has appeared in the groups list


  Scenario: User changes name of group in one provider and sees that it was changed also in other provider
    When user of browser clicks "space1" on spaces on left sidebar menu
    And user of browser clicks Providers of "space1" on left sidebar menu
    And user of browser sees "oneprovider-1" is on the providers list
    And user of browser clicks on "oneprovider-1" provider on left sidebar menu
    And user of browser sees that Oneprovider session has started
    # rename group
    When user of browser clicks on the "groups" tab in main menu sidebar
    And user of browser clicks on settings icon displayed for "group1" item on the groups sidebar list
    And user of browser clicks on the "RENAME" item in settings dropdown for group named "group1"
    And user of browser sees that "Rename a group" modal has appeared
    And user of browser clicks on input box in active modal
    And user of browser types "NewNameGroup" on keyboard
    And user of browser presses enter on keyboard
    And user of browser sees an info notify with text matching to: .*group1.*renamed.*NewNameGroup.*
    And user of browser sees that the modal has disappeared
    And user of browser refreshes site
    And user of browser sees that group named "group1" has disappeared from the groups list
    And user of browser sees that group named "NewNameGroup" has appeared in the groups list

    And user of browser clicks on the "providers" tab in main menu sidebar
    And user of browser sees "NewNameGroup" is in groups on left sidebar menu
    And user of browser sees "multiprov" is not in groups on left sidebar menu

    # check changes in second provider
    And user of browser clicks on "oneprovider-2" provider on left sidebar menu
    And user of browser clicks on the "groups" tab in main menu sidebar
    And user of browser sees that group named "group1" has disappeared from the groups list
    Then user of browser sees that group named "NewNameGroup" has appeared in the groups list

  Scenario: User leaves group in one provider and sees that it was leaved from also in other provider
    When user of browser clicks "space1" on spaces on left sidebar menu
    And user of browser clicks Providers of "space1" on left sidebar menu
    And user of browser sees "oneprovider-1" is on the providers list
    And user of browser clicks on "oneprovider-1" provider on left sidebar menu
    And user of browser sees that Oneprovider session has started
    # leave group
    When user of browser clicks on the "groups" tab in main menu sidebar
    And user of browser clicks on settings icon displayed for "group1" item on the groups sidebar list
    And user of browser clicks on the "LEAVE THIS GROUP" item in settings dropdown for group named "group1"
    And user of browser sees that "Leave the group" modal has appeared
    And user of browser clicks "Yes" confirmation button in displayed modal
    And user of browser sees that the modal has disappeared
    And user of browser sees an info notify with text matching to: .*group1.*left
    And user of browser refreshes site
    And user of browser sees that group named "group1" has disappeared from the groups list

    And user of browser clicks on the "providers" tab in main menu sidebar
    And user of browser sees "group1" is not in groups on left sidebar menu
    # check changes in second provider
    And user of browser clicks on "oneprovider-2" provider on left sidebar menu
    And user of browser clicks on the "groups" tab in main menu sidebar
    Then user of browser sees that group named "group1" has disappeared from the groups list
