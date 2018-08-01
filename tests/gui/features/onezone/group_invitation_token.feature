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
    And users of [browser1, browser2] opened [onezone, onezone] page
    And users of [browser1, browser2] logged as [user1, user2] to Onezone service

  Scenario: Join a space with group invitation token
    When user of browser1 clicks "space1" on spaces on left menu
    And user of browser1 clicks Members of "space1" on left menu
    And user of browser1 clicks Invite group on Menu of Members
    And user of browser1 sends invitation token to "browser2"
    And user of browser2 clicks "group2" on groups on left menu
    And user of browser2 clicks Join space on groups menu on left menu
    And user of browser2 pastes Space invitation token to input
    And user of browser2 clicks Join the space button on Join to a space page
    Then user of browser2 sees "space1" has appeared on spaces

  Scenario: Fail to join a space with invalid group invitation token
    When user of browser2 clicks "group2" on groups on left menu
    And user of browser2 clicks Join space on groups menu on left menu
    And user of browser2 types "invalid token" to input
    And user of browser2 clicks Join the space button on Join to a space page
    Then user of browser2 sees error popup has appeared