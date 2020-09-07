Feature: Multi Browser invitation group to spaces


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And initial groups configuration in "onezone" Onezone service:
          group2:
            owner: user2
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000


    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, Onezone] page
    And users of [browser1, browser2] logged as [user1, user2] to [Onezone, Onezone] service


  Scenario: User joins a space with group invitation token
    When user of browser1 clicks on Data in the main menu
    And user of browser1 clicks "space1" on the spaces list in the sidebar
    And user of browser1 clicks Members of "space1" in the sidebar
    And user of browser1 clicks on "Invite group using token" button in groups list menu in "space1" space members view
    And user of browser1 copies invitation token from modal
    And user of browser1 closes "Invite using token" modal
    And user of browser1 sends copied token to user of browser2

    And user of browser2 adds group "group2" to space using copied token

    Then user of browser2 sees that "space1" has appeared on the spaces list in the sidebar


  Scenario: User joins a space with group invitation token and see space was renamed
    # user1 invites user2 via group invitation
    When user of browser1 clicks on Data in the main menu
    And user of browser1 clicks "space1" on the spaces list in the sidebar
    And user of browser1 clicks Members of "space1" in the sidebar
    And user of browser1 clicks on "Invite group using token" button in groups list menu in "space1" space members view
    And user of browser1 copies invitation token from modal
    And user of browser1 closes "Invite using token" modal
    And user of browser1 sends copied token to user of browser2

    And user of browser2 adds group "group2" to space using copied token

    # user1 renames space
    And user of browser1 clicks "space1" on the spaces list in the sidebar
    And user of browser1 writes "space2" into rename space text field
    And user of browser1 clicks on confirmation button on overview page

    # user2 sees space has different name
    And user of browser1 is idle for 4 seconds
    Then user of browser2 sees that "space1" has disappeared on the spaces list in the sidebar
    And user of browser2 sees that "space2" has appeared on the spaces list in the sidebar
