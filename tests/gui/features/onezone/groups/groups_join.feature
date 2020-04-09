Feature: Joining a group in Onezone GUI


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
    And user of [browser1, browser2] logged as [user1, user2] to [Onezone, Onezone] service


  Scenario: User joins group using invitation token
    When user of browser1 clicks on Groups in the main menu
    And user of browser1 clicks "group1" on the groups list in the sidebar
    And user of browser1 clicks on "Invite user using token" button in users list menu in "group1" group members view
    And user of browser1 copies invitation token from modal
    And user of browser1 clicks on "Cancel" button in modal "Invite using token"
    And user of browser1 sends copied token to user of browser2

    And user of browser2 joins group using received token

    Then user of browser1 sees "user2" user on "group1" group members list
    And user of browser2 sees group "group1" on groups list


  Scenario: User fails to join group he already belongs to
    When user of browser1 clicks on Groups in the main menu
    And user of browser1 clicks "group1" on the groups list in the sidebar
    And user of browser1 clicks on "Invite user using token" button in users list menu in "group1" group members view
    And user of browser1 copies invitation token from modal
    And user of browser1 clicks on "Cancel" button in modal "Invite using token"

    And user of browser1 joins group using copied token

    Then user of browser1 sees that error modal with text "Consuming token failed" appeared


  Scenario: User fails to view group he does not belong to
    When user of browser1 clicks on Groups in the main menu
    And user of browser1 goes to group "group1" main subpage
    And user of browser1 copies a first resource ID from URL
    And user of browser1 sends copied ID to user of browser2
    And user of browser2 changes webapp path to "/i#/onedata/groups" concatenated with received ID
    And user of browser2 refreshes site
    Then user of browser2 sees "DON’T HAVE ACCESS" in error details on groups page

