Feature: Basic management of spaces


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000


    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: Create new space
    When user of browser clicks create new space on spaces on left menu
    And user of browser types "space" on input
    And user of browser clicks on create new space button
    Then user of browser sees "space" has appeared on spaces

  Scenario: Rename space
    When user of browser clicks "space1" on spaces on left menu
    And user of browser types "space2" on rename input
    And user of browser clicks on confirmation button
    Then user of browser sees "space2" has appeared on spaces

    Scenario: Cancel rename space
    When user of browser clicks "space1" on spaces on left menu
    And user of browser types "space2" on rename input
    And user of browser clicks on cancel button
    Then user of browser sees "space1" has appeared on spaces

  Scenario: Leave space
#    create new space
    When user of browser clicks create new space on spaces on left menu
    And user of browser types "space" on input
    And user of browser clicks on create new space button
#    leave space
    And user of browser clicks "space" on spaces on left menu
    And user of browser clicks on leave space button
    And user of browser clicks on yes leave button
    Then user of browser sees "space" has disappeared on spaces

  Scenario: Set space as home space for user
    When user of browser clicks "space1" on spaces on left menu
    And user of browser clicks on toggle default space
    Then user of browser sees home space on spaces on left menu

  Scenario: Unset space as home space for user
    When user of browser clicks "space1" on spaces on left menu
    And user of browser clicks on toggle default space
    And user of browser sees home space on spaces on left menu
    And user of browser clicks on toggle default space
    Then user of browser sees home space has disappeared on spaces on left menu

  Scenario: Number of supporting providers after create new space
#    create new space
    When user of browser clicks create new space on spaces on left menu
    And user of browser types "space" on input
    And user of browser clicks on create new space button
    Then user of browser sees 0 number of supporting providers of "space"

  Scenario: Size of the space after create new space
#    create new space
    When user of browser clicks create new space on spaces on left menu
    And user of browser types "space" on input
    And user of browser clicks on create new space button
    Then user of browser sees 0 B size of the "space"



