Feature: Basic management of groups with one user in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1

    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as user1 to Onezone service


  Scenario Outline: User renames group
    When user of browser clicks on "Rename" button in group "group1" menu in the sidebar
    And user of browser writes "group2" into rename group text field
    And user of browser confirms group rename using <confirmation_method>
    Then user of browser sees group "group2" on groups list
    And user of browser does not see group "group1" on groups list

    Examples:
      | confirmation_method |
      | enter               |
      | button              |


  Scenario: User removes group
    When user of browser clicks on "Remove" button in group "group1" menu in the sidebar
    And user of browser clicks on "Remove" button in modal "REMOVE GROUP"
    Then user of browser does not see group "group1" on groups list


  Scenario: User leaves group
    When user of browser clicks on "Leave" button in group "group1" menu in the sidebar
    And user of browser clicks on "Leave" button in modal "LEAVE GROUP"
    Then user of browser does not see group "group1" on groups list


  Scenario: User fails to add group as its subgroup
    When user of browser clicks on "generate an invitation token" text in group "group1" members groups list
    And user of browser copies invitation token from modal
    And user of browser closes "Invite using token" modal

    And user of browser clicks on Tokens in the main menu
    And user of browser clicks on "Consume token" button in tokens sidebar
    And user of browser pastes copied token into token text field
    And user of browser chooses "group1" group from dropdown on tokens page
    And user of browser clicks on Join button on consume token page

    Then user of browser sees that error modal with text "Consuming token failed" appeared


  Scenario: User generates group invitation token
    When user of browser clicks on Groups in the main menu
    And user of browser clicks "group1" on the groups list in the sidebar
    And user of browser clicks on "Invite group using token" button in groups list menu in "group1" group members view
    And user of browser sees that area with group invitation token has appeared

    Then user of browser sees non-empty token in token area


  Scenario: User generates user invitation token
    When user of browser clicks on Groups in the main menu
    And user of browser clicks "group1" on the groups list in the sidebar
    And user of browser clicks on "Invite user using token" button in users list menu in "group1" group members view
    And user of browser sees that area with user invitation token has appeared

    Then user of browser sees non-empty token in token area


  Scenario: User fails to view group after leaving it
    When user of browser opens group "group1" main subpage
    And user of browser copies a first resource ID from URL
    And user of browser leaves group "group1"

    And user of browser refreshes site

    And user of browser changes webapp path to "/i#/onedata/groups" concatenated with copied item
    And user of browser refreshes site

    Then user of browser sees "YOU DON’T HAVE ACCESS TO THIS RESOURCE" in error details on groups page




