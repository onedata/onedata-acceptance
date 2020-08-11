Feature: Basic management of groups with multiple users in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
          group2:
            owner: user2
          group3:
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


  Scenario: Single user adds subgroup
    When user of browser1 clicks on Groups in the main menu
    And user of browser1 clicks "group3" on the groups list in the sidebar
    And user of browser1 clicks on "Invite group using token" button in groups list menu in "group3" group members view
    And user of browser1 copies invitation token from modal
    And user of browser1 closes "Invite using token" modal

    And user of browser1 adds group "group1" as subgroup using copied token

    Then user of browser1 sees "group1" as "group3" child


  Scenario: User adds subgroup
    When user of browser1 copies "group1" group invitation token
    And user of browser1 sends copied token to user of browser2
    And user of browser2 adds group "group2" as subgroup using copied token

    Then users of [browser1, browser2] sees group "group1" on groups list
    And user of browser2 sees group "group2" on groups list
