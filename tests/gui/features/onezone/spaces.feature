Feature: Basic management of spaces


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
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
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: Create new space
    When user of browser clicks create new space on spaces on left menu
    And user of browser types "space" on input
    And user of browser clicks on create new space button
    Then user of browser sees new "space" appeared

