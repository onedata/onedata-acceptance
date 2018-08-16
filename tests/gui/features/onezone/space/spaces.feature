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


  Scenario: Rename space (click on confirmation button)
    When user of browser clicks "space1" on spaces on left sidebar menu
    And user of browser types "space2" on rename input on overview page
    And user of browser clicks on confirmation button on overview page
    Then user of browser sees "space2" has appeared on spaces
    And user of browser sees "space1" has disappeared on spaces

  Scenario: Rename space (press Enter to confirm)
    When user of browser clicks "space1" on spaces on left sidebar menu
    And user of browser types "space2" on rename input on overview page
    And user of browser presses enter on keyboard
    Then user of browser sees "space2" has appeared on spaces
    And user of browser sees "space1" has disappeared on spaces

  Scenario: Cancel rename space
    When user of browser clicks "space1" on spaces on left sidebar menu
    And user of browser types "space2" on rename input on overview page
    And user of browser clicks on cancel button on overview page
    Then user of browser sees "space1" has appeared on spaces
    And user of browser sees "space2" has disappeared on spaces

  Scenario: Leave space
    # create new space
    When user of browser clicks create new space on spaces on left sidebar menu
    And user of browser types "space2" on input on create new space page
    And user of browser clicks on create new space button
    # leave space
    And user of browser clicks "space2" on spaces on left sidebar menu
    And user of browser clicks on leave space button
    And user of browser clicks on "Yes, leave" button
    Then user of browser sees "space2" has disappeared on spaces

  Scenario: Cancel leave space
    # create new space
    When user of browser clicks create new space on spaces on left sidebar menu
    And user of browser types "space2" on input on create new space page
    And user of browser clicks on create new space button
    # leave space
    And user of browser clicks "space2" on spaces on left sidebar menu
    And user of browser clicks on leave space button
    And user of browser clicks on "No, stay here" button
    Then user of browser sees "space2" has appeared on spaces

  Scenario: Set space as home space for user
    When user of browser clicks "space1" on spaces on left sidebar menu
    And user of browser clicks on toggle default space
    Then user of browser sees home space on spaces on left sidebar menu

  Scenario: Unset space as home space for user
    When user of browser clicks "space1" on spaces on left sidebar menu
    And user of browser clicks on toggle default space
    And user of browser sees home space on spaces on left sidebar menu
    And user of browser clicks on toggle default space
    Then user of browser sees home space has disappeared on spaces on left sidebar menu

  Scenario: Number of supporting providers after create new space
    # create new space
    When user of browser clicks create new space on spaces on left sidebar menu
    And user of browser types "space2" on input on create new space page
    And user of browser clicks on create new space button
    Then user of browser sees 0 number of supporting providers of "space2"

  Scenario: Size of the space after create new space
    # create new space
    When user of browser clicks create new space on spaces on left sidebar menu
    And user of browser types "space2" on input on create new space page
    And user of browser clicks on create new space button
    Then user of browser sees 0 B size of the "space2"

  Scenario: Fail to join a space with invalid user invitation token
    When user of browser clicks Join some space using a space invitation token button
    And user of browser types "invalid token" to input on Join to a space page
    And user of browser clicks Join the space button on Join to a space page
    Then user of browser sees error popup has appeared

  Scenario: Check list o providers on space
    When user of browser clicks "space1" on spaces on left sidebar menu
    And user of browser clicks Providers of "space1" on left sidebar menu
    Then user of browser sees "oneprovider-1" is on the providers list
    And user of browser sees length of providers list is equal number of supporting providers of "space1"

  Scenario: Generate different support tokens (space has arleady supported by one provider)
    When user of browser clicks "space1" on spaces on left sidebar menu
    And user of browser clicks Providers of "space1" on left sidebar menu
    And user of browser clicks Get support button on providers page
    And user of browser clicks Copy button on Get support page
    And user of browser clicks Generate another token on Get support page
    Then user of browser sees another token is different than first one

  Scenario: Generate different deploy provider tokens (space has arleady supported by one provider)
    When user of browser clicks "space1" on spaces on left sidebar menu
    And user of browser clicks Providers of "space1" on left sidebar menu
    And user of browser clicks Get support button on providers page
    And user of browser clicks Deploy your own provider tab on get support page
    And user of browser clicks Copy button on Get support page
    And user of browser clicks Generate another token on Get support page
    Then user of browser sees another token is different than first one

  Scenario: Successfully copy support token (space has arleady supported by one provider)
    When user of browser clicks "space1" on spaces on left sidebar menu
    And user of browser clicks Providers of "space1" on left sidebar menu
    And user of browser clicks Get support button on providers page
    And user of browser clicks Copy button on Get support page
    Then user of browser sees copy token and token in input are the same
    And user of browser sees non-empty copy token