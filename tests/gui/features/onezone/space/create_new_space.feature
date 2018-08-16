Feature: Create new space


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: Create new space (with new space button on left sidebar menu)
    When user of browser clicks create new space on spaces on left sidebar menu
    And user of browser types "space1" on input on create new space page
    And user of browser clicks on create new space button
    Then user of browser sees "space1" has appeared on spaces

  Scenario: Create new space (with Get started button)
    When user of browser clicks Get started on spaces on left sidebar menu
    And user of browser clicks Create a space on Welcome page
    And user of browser types "space1" on input on create new space page
    And user of browser clicks on create new space button
    Then user of browser sees "space1" has appeared on spaces

  Scenario: Create new space (with new space button on left sidebar menu and pressing ENTER)
    When user of browser clicks create new space on spaces on left sidebar menu
    And user of browser types "space1" on input on create new space page
    And user of browser presses enter on keyboard
    Then user of browser sees "space1" has appeared on spaces

  Scenario: Create new space (with Get started button and pressing ENTER)
    When user of browser clicks Get started on spaces on left sidebar menu
    And user of browser clicks Create a space on Welcome page
    And user of browser types "space1" on input on create new space page
    And user of browser presses enter on keyboard
    Then user of browser sees "space1" has appeared on spaces