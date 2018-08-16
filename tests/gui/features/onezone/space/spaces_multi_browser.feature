Feature: Multi Browser basic management of spaces


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
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

  Scenario: Join a space with user invitation token
    When user of browser1 clicks "space1" on spaces on left sidebar menu
    And user of browser1 clicks Members of "space1" on left sidebar menu
    And user of browser1 clicks Invite user on Menu of Members
    And user of browser1 sends invitation token to "browser2"
    And user of browser2 clicks Join some space using a space invitation token button
    And user of browser2 pastes Space invitation token to input on Join to a space page
    And user of browser2 clicks Join the space button on Join to a space page
    Then user of browser2 sees "space1" has appeared on spaces

  Scenario: Join a space with user invitation token (with Get started button)
    When user of browser1 clicks "space1" on spaces on left sidebar menu
    And user of browser1 clicks Members of "space1" on left sidebar menu
    And user of browser1 clicks Invite user on Menu of Members
    And user of browser1 sends invitation token to "browser2"
    And user of browser2 clicks Get started on spaces on left sidebar menu
    And user of browser2 clicks join an existing space on Welcome page
    And user of browser2 pastes Space invitation token to input on Join to a space page
    And user of browser2 clicks Join the space button on Join to a space page
    Then user of browser2 sees "space1" has appeared on spaces

  Scenario: Join a space with user invitation token (with press ENTER)
    When user of browser1 clicks "space1" on spaces on left sidebar menu
    And user of browser1 clicks Members of "space1" on left sidebar menu
    And user of browser1 clicks Invite user on Menu of Members
    And user of browser1 sends invitation token to "browser2"
    And user of browser2 clicks Join some space using a space invitation token button
    And user of browser2 pastes Space invitation token to input on Join to a space page
    And user of browser2 presses enter on keyboard
    Then user of browser2 sees "space1" has appeared on spaces