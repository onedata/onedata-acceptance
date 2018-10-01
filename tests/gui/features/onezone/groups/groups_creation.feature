Feature: Basic creation/joining of groups with one user in Onezone GUI


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
    And user of browser opened Onezone page
    And user of browser logged as user1 to Onezone service


  Scenario Outline: User creates group
    When user of browser clicks on Create group button in groups sidebar
    And user of browser writes "group1" into group name text field
    And user of browser confirms using <confirmation_method>
    Then user of browser sees group "group1" on groups list

    Examples:
      | confirmation_method |
      | enter               |
      | button              |

  Scenario: User fails to create unnamed group using button to confirm group name
    When user of browser clicks on Create group button in groups sidebar
    Then user of browser sees that create group button is inactive


  Scenario: User fails to create unnamed group using enter to confirm group name
    When user of browser clicks on Create group button in groups sidebar
    And user of browser presses enter on keyboard
    Then user of browser sees that error modal with text "creating group failed" appeared

