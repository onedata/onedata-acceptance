Feature: Basic management of groups with one user in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
    And initial spaces configuration in "onezone" Onezone service:
          space1:
              owner: user1
              home space for:
                  - user1
              providers:
                  - oneprovider-1:
                      storage: posix
                      size: 1000000

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


  Scenario Outline: User fails to add group as its subgroup
    When user of browser clicks on "generate an invitation token" text in group "group1" members groups list
    And user of browser copies invitation token from modal
    And user of browser closes "Invite group using token" modal

    And user of browser clicks on "Join as subgroup" button in group "group1" menu in the sidebar
    And user of browser pastes copied token into group token text field
    And user of browser confirms using <confirmation_method>

    Then user of browser sees that error modal with text "joining group as subgroup failed" appeared

    Examples:
      | confirmation_method |
      | enter               |
      | button              |


  Scenario: User generates group invitation token
    When user of browser clicks on "Invite group using token" button in groups list menu in "group1" group members view
    And user of browser sees that area with group invitation token has appeared

    Then user of browser sees non-empty token in token area


  Scenario: User generates user invitation token
    When user of browser clicks on "Invite user using token" button in users list menu in "group1" group members view
    And user of browser sees that area with user invitation token has appeared

    Then user of browser sees non-empty token in token area


  Scenario: User fails to view group after leaving it
    When user of browser goes to group "group1" main subpage
    And user of browser copies a first resource ID from URL
    And user of browser leaves group "group1"

    And user of browser refreshes site

    And user of browser changes webapp path to "/i#/onedata/groups" concatenated with copied item
    And user of browser refreshes site

    And user of browser clicks Show details on groups page
    Then user of browser sees "Insufficient permissions" in error details on groups page




