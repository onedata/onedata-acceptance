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
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User creates group using button to confirm group name
    When user of browser clicks on the create button in "groups" Onezone panel
    And user of browser writes "group1" into group name text field
    And user of browser clicks on confirmation button

    And user of browser refreshes site

    Then user of browser sees group "group1" on groups list


  Scenario: User creates group using enter to confirm group name
    When user of browser clicks on the create button in "groups" Onezone panel
    And user of browser writes "group1" into group name text field
    And user of browser presses enter on keyboard

    And user of browser refreshes site

    Then user of browser sees group "group1" on groups list


  Scenario: User tries to create unnamed group using button to confirm group name
    When user of browser clicks on the create button in "groups" Onezone panel

    Then user of browser sees that create group button is inactive 


  Scenario: User tries to create unnamed group using enter to confirm group name
    When user of browser clicks on the create button in "groups" Onezone panel
    And user of browser presses enter on keyboard

    Then user of browser sees that error modal with text "creating group failed" appeared

