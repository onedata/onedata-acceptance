Feature: Basic groups management in Oneprovider GUI


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

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service
    And opened oneprovider-1 Oneprovider view in web GUI by user of browser
    And user of browser clicked on the "groups" tab in main menu sidebar


  # todo rewrite test for new gui in onezone
  Scenario: User receives group invitation token
    When user of browser clicks on settings icon displayed for "group1" item on the groups sidebar list
    And user of browser clicks on the "INVITE GROUP" item in settings dropdown for group named "group1"
    And user of browser sees that "Invite group to the group" modal has appeared
    Then user of browser sees non-empty token in active modal


  # todo rewrite test for new gui in onezone
  Scenario: User fails to join group to space because of using invalid token (presses ENTER after entering token)
    When user of browser clicks on settings icon displayed for "group1" item on the groups sidebar list
    And user of browser clicks on the "JOIN SPACE" item in settings dropdown for group named "group1"
    And user of browser sees that "Join a space" modal has appeared
    And user of browser clicks on input box in active modal
    And user of browser types "helloworld" on keyboard
    And user of browser presses enter on keyboard
    Then user of browser sees an error notify with text matching to: .*join.*group1.*space.*
    And user of browser sees that the modal has disappeared


  # todo rewrite test for new gui in onezone
  Scenario: User fails to join group to space because of using invalid token (clicks Join confirmation button after entering token)
    When user of browser clicks on settings icon displayed for "group1" item on the groups sidebar list
    And user of browser clicks on the "JOIN SPACE" item in settings dropdown for group named "group1"
    And user of browser sees that "Join a space" modal has appeared
    And user of browser clicks on input box in active modal
    And user of browser types "helloworld" on keyboard
    And user of browser clicks "Join" confirmation button in displayed modal
    Then user of browser sees an error notify with text matching to: .*join.*group1.*space.*
    And user of browser sees that the modal has disappeared


  # todo rewrite test for new gui in onezone
  Scenario: User fails to join group as subgroup because of using invalid token (presses ENTER after entering token)
    When user of browser clicks on settings icon displayed for "group1" item on the groups sidebar list
    And user of browser clicks on the "JOIN AS SUBGROUP" item in settings dropdown for group named "group1"
    And user of browser sees that "Join a group to group" modal has appeared
    And user of browser clicks on input box in active modal
    And user of browser types "helloworld" on keyboard
    And user of browser presses enter on keyboard
    Then user of browser sees an error notify with text matching to: .*join.*group1.*subgroup.*
    And user of browser sees that the modal has disappeared


  # todo rewrite test for new gui in onezone
  Scenario: User fails to join group as subgroup because of using invalid token (clicks Join confirmation button after entering token)
    When user of browser clicks on settings icon displayed for "group1" item on the groups sidebar list
    And user of browser clicks on the "JOIN AS SUBGROUP" item in settings dropdown for group named "group1"
    And user of browser sees that "Join a group to group" modal has appeared
    And user of browser clicks on input box in active modal
    And user of browser types "helloworld" on keyboard
    And user of browser clicks "Join" confirmation button in displayed modal
    Then user of browser sees an error notify with text matching to: .*join.*group1.*subgroup.*
    And user of browser sees that the modal has disappeared


  # todo rewrite test for new gui in onezone
  Scenario: User fails to join to group because of using invalid token (presses ENTER after entering token)
    When user of browser clicks on the Join button in groups sidebar header
    And user of browser sees that "Join a group" modal has appeared
    And user of browser clicks on input box in active modal
    And user of browser types "helloworld" on keyboard
    And user of browser presses enter on keyboard
    Then user of browser sees an error notify with text matching to: .*[Ff]ailed.*join.*group.*
    And user of browser sees that the modal has disappeared


  # todo rewrite test for new gui in onezone
  Scenario: User fails to join to group because of using invalid token (clicks Join confirmation button after entering token)
    When user of browser clicks on the Join button in groups sidebar header
    And user of browser sees that "Join a group" modal has appeared
    And user of browser clicks on input box in active modal
    And user of browser types "helloworld" on keyboard
    And user of browser clicks "Join" confirmation button in displayed modal
    Then user of browser sees an error notify with text matching to: .*[Ff]ailed.*join.*group.*
    And user of browser sees that the modal has disappeared


  # todo rewrite test for new gui in onezone
  Scenario: User successfully renames group (presses ENTER after entering group name)
    When user of browser clicks on settings icon displayed for "group1" item on the groups sidebar list
    And user of browser clicks on the "RENAME" item in settings dropdown for group named "group1"
    And user of browser sees that "Rename a group" modal has appeared
    And user of browser clicks on input box in active modal
    And user of browser types "NewNameGroup" on keyboard
    And user of browser presses enter on keyboard
    And user of browser sees an info notify with text matching to: .*group1.*renamed.*NewNameGroup.*
    And user of browser sees that the modal has disappeared
    And user of browser refreshes site
    Then user of browser sees that group named "group1" has disappeared from the groups list
    And user of browser sees that group named "NewNameGroup" has appeared in the groups list


  # todo rewrite test for new gui in onezone
  Scenario: User successfully renames group (clicks OK after entering group name)
    When user of browser clicks on settings icon displayed for "group1" item on the groups sidebar list
    And user of browser clicks on the "RENAME" item in settings dropdown for group named "group1"
    And user of browser sees that "Rename a group" modal has appeared
    And user of browser clicks on input box in active modal
    And user of browser types "NewNameGroup" on keyboard
    And user of browser clicks "OK" confirmation button in displayed modal
    And user of browser sees an info notify with text matching to: .*group1.*renamed.*NewNameGroup.*
    And user of browser sees that the modal has disappeared
    And user of browser refreshes site
    Then user of browser sees that group named "group1" has disappeared from the groups list
    And user of browser sees that group named "NewNameGroup" has appeared in the groups list


  # todo rewrite test for new gui in onezone
  Scenario: User can leave existing group
    When user of browser clicks on settings icon displayed for "group1" item on the groups sidebar list
    And user of browser clicks on the "LEAVE THIS GROUP" item in settings dropdown for group named "group1"
    And user of browser sees that "Leave the group" modal has appeared
    And user of browser clicks "Yes" confirmation button in displayed modal
    And user of browser sees that the modal has disappeared
    Then user of browser sees an info notify with text matching to: .*group1.*left
    And user of browser refreshes site
    And user of browser sees that group named "group1" has disappeared from the groups list


  # todo rewrite test for new gui in onezone
  Scenario: User fails to view group after leaving it
    When user of browser selects "group1" from groups sidebar list
    And user of browser copies a first resource ID from URL
    And user of browser clicks on settings icon displayed for "group1" item on the groups sidebar list
    And user of browser clicks on the "LEAVE THIS GROUP" item in settings dropdown for group named "group1"
    And user of browser sees that "Leave the group" modal has appeared
    And user of browser clicks "Yes" confirmation button in displayed modal
    And user of browser sees that the modal has disappeared
    And user of browser sees an info notify with text matching to: .*group1.*left
    And user of browser refreshes site
    And user of browser sees that group named "group1" has disappeared from the groups list
    And user of browser changes webapp path to /#/onedata/groups concatenated with copied item
    Then user of browser sees an error notify with text matching to: .*?[Cc]annot load requested resource.*?
    And user of browser does not see "group1" in groups list
