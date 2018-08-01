Feature: Create new space


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: Create new space (with new space button on left menu)
    When user of browser clicks create new space on spaces on left menu
    And user of browser types "space" on input
    And user of browser clicks on create new space button
    Then user of browser sees "space" has appeared on spaces

  Scenario: Create new space (with Get started button)
    When user of browser clicks Get started on spaces on left menu
    And user of browser clicks Create a space on No spaces page
    And user of browser types "space" on input
    And user of browser clicks on create new space button
    Then user of browser sees "space" has appeared on spaces