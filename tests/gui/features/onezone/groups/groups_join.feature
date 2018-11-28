Feature: Joining a group in Onezone GUI

  Examples:
    | confirmation_method |
    | enter               |
    | button              |

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
              home space for:
                  - user1
              providers:
                  - oneprovider-1:
                      storage: posix
                      size: 1000000

    And users opened [browser1, browser2] browsers' windows
    And user of [browser1, browser2] opened [Onezone, Onezone] page
    And user of [browser1, browser2] logged as [user1, user2] to Onezone service


  Scenario Outline: User joins group using invitation token
    When user of browser1 clicks on Groups in the sidebar
    And user of browser1 clicks "group1" on the groups list in the sidebar
    And user of browser1 clicks on "Invite user using token" button in group "group1" members menu
    And user of browser1 copies invitation token from modal
    And user of browser1 closes modal "Invite user using token"
    And user of browser1 sends copied token to user of browser2

    And user of browser2 clicks on Groups in the sidebar
    And user of browser2 clicks on Join group button in groups sidebar
    And user of browser2 pastes copied token into group token text field
    And user of browser2 confirms using <confirmation_method>

    And users of browser1 refreshes site

    Then user of browser1 sees user "user2" on group "group1" members list
    And user of browser2 sees group "group1" on groups list


  Scenario Outline: User fails to join group using group invitation token
    When user of browser1 clicks on Groups in the sidebar
    And user of browser1 clicks "group1" on the groups list in the sidebar
    And user of browser1 clicks on "Invite group using token" button in group "group1" members menu
    And user of browser1 copies invitation token from modal
    And user of browser1 closes modal "Invite group using token"
    And user of browser1 sends copied token to user of browser2

    And user of browser2 clicks on Groups in the sidebar
    And user of browser2 clicks on Join group button in groups sidebar
    And user of browser2 pastes copied token into group token text field
    And user of browser2 confirms using <confirmation_method>

    Then user of browser2 sees that error modal with text "joining the group failed" appeared


  Scenario Outline: User fails to join group using incorrect token
    When user of browser1 clicks on Groups in the sidebar
    And user of browser1 clicks on Join group button in groups sidebar
    And user of browser1 writes "aaa" into group token text field
    And user of browser1 confirms using <confirmation_method>

    Then user of browser1 sees that error modal with text "joining the group failed" appeared


  Scenario Outline: User fails to join group to space using incorrect token
    When user of browser1 clicks on Groups in the sidebar
    And user of browser1 clicks on "Join space" button in group "group1" menu
    And user of browser1 writes "aaa" into group token text field
    And user of browser1 confirms using <confirmation_method>

    Then user of browser1 sees that error modal with text "joining space failed" appeared


  Scenario Outline: User fails to join group he already belongs to
    When user of browser1 clicks on Groups in the sidebar
    And user of browser1 clicks "group1" on the groups list in the sidebar
    And user of browser1 clicks on "Invite user using token" button in group "group1" members menu
    And user of browser1 copies invitation token from modal
    And user of browser1 closes modal "Invite user using token"

    And user of browser1 clicks on Join group button in groups sidebar
    And user of browser1 pastes copied token into group token text field
    And user of browser1 confirms using <confirmation_method>

    Then user of browser1 sees that error modal with text "joining the group failed" appeared


  Scenario: User fails to view group he does not belong to
    When user of browser1 clicks on Groups in the sidebar
    And user of browser1 goes to group "group1" main subpage
    And user of browser1 copies a first resource ID from URL
    And user of browser1 sends copied ID to user of browser2
    And user of browser2 changes webapp path to "/#/onedata/groups" concatenated with received ID

    And user of browser2 refreshes site

    Then user of browser2 see that page with text "RESOURCE NOT FOUND" appeared

