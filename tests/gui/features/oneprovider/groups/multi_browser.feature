Feature: Groups operations using multiple browsers in Oneprovider GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
    And initial spaces configuration in "onezone" Onezone service:
          space1:
              owner: user1
              users:
                  - user2
              providers:
                  - oneprovider-1:
                      storage: posix
                      size: 1000000

    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [onezone, onezone] page
    And users of [browser1, browser2] logged as [user1, user2] to Onezone service
    And opened oneprovider-1 Oneprovider view in web GUI by users of [browser1, browser2]
    And users of [browser1, browser2] clicked on the "groups" tab in main menu sidebar


# todo rewrite test for new gui in onezone
  Scenario: User fails to view group, to which he does not belong to, using its ID in URL
    When user of browser1 selects "group1" from groups sidebar list
    And user of browser1 copies a first resource ID from URL
    And user of browser1 sends copied group's ID to user of browser2
    And user of browser2 changes webapp path to /#/onedata/groups concatenated with received group's ID
    Then user of browser2 sees an error notify with text matching to: .*?[Cc]annot load requested resource.*?
    And user of browser2 does not see "group1" in groups list


# todo rewrite test for new gui in onezone
  Scenario: User successfully invites other user to join his group (presses ENTER after entering token)
    # user1 generate group invitation token
    When user of browser1 clicks on settings icon displayed for "group1" item on the groups sidebar list
    And user of browser1 clicks on the "INVITE USER" item in settings dropdown for group named "group1"
    And user of browser1 sees that "Invite user to the group" modal has appeared
    And user of browser1 sees non-empty token in active modal
    And user of browser1 clicks on copy button in active modal
    And user of browser1 sends copied token to user of browser2
    And user of browser1 clicks "OK" confirmation button in displayed modal
    And user of browser1 sees that the modal has disappeared

    # user2 joins group1
    And user of browser2 clicks on the Join button in groups sidebar header
    And user of browser2 sees that "Join a group" modal has appeared
    And user of browser2 clicks on input box in active modal
    And user of browser2 types received token on keyboard
    And user of browser2 presses enter on keyboard
    And user of browser2 sees that the modal has disappeared
    Then user of browser2 sees that group named "group1" has appeared in the groups list

    # users checks group1 permission table
    And user of browser2 selects "group1" from groups sidebar list
    And user of browser2 sees that "user2" item has appeared on current USERS permissions table in Groups tab
    And user of browser1 selects "group1" from groups sidebar list
    And user of browser1 sees that "user2" item has appeared on current USERS permissions table in Groups tab


# todo rewrite test for new gui in onezone
  Scenario: User successfully invites other user to join his group (clicks JOIN confirmation button after entering token)
    # user1 generate group invitation token
    When user of browser1 clicks on settings icon displayed for "group1" item on the groups sidebar list
    And user of browser1 clicks on the "INVITE USER" item in settings dropdown for group named "group1"
    And user of browser1 sees that "Invite user to the group" modal has appeared
    And user of browser1 sees non-empty token in active modal
    And user of browser1 clicks on copy button in active modal
    And user of browser1 sends copied token to user of browser2
    And user of browser1 clicks "OK" confirmation button in displayed modal
    And user of browser1 sees that the modal has disappeared

    # user2 joins group1
    And user of browser2 clicks on the Join button in groups sidebar header
    And user of browser2 sees that "Join a group" modal has appeared
    And user of browser2 clicks on input box in active modal
    And user of browser2 types received token on keyboard
    And user of browser2 clicks "Join" confirmation button in displayed modal
    And user of browser2 sees that the modal has disappeared
    Then user of browser2 sees that group named "group1" has appeared in the groups list

    # users checks group1 permission table
    And user of browser2 selects "group1" from groups sidebar list
    And user of browser2 sees that "user2" item has appeared on current USERS permissions table in Groups tab
    And user of browser1 selects "group1" from groups sidebar list
    And user of browser1 sees that "user2" item has appeared on current USERS permissions table in Groups tab
