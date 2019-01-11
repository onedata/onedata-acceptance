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
    And user of browser opened Onezone page
    And user of browser logged as user1 to Onezone service


  Scenario Outline: User successfully renames space
    When user of browser clicks on Spaces in the main menu
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser writes "space2" into rename space text field
    And user of browser confirms rename the space using <confirmation_method>
    Then user of browser sees that "space2" has appeared on the spaces list in the sidebar
    And user of browser sees that "space1" has disappeared on the spaces list in the sidebar

    Examples:
      | confirmation_method |
      | enter               |
      | button              |


  Scenario: User successfully cancels rename space
    When user of browser clicks on Spaces in the main menu
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser writes "space2" into rename space text field
    And user of browser clicks on cancel button on overview page
    Then user of browser sees that "space1" has appeared on the spaces list in the sidebar
    And user of browser sees that "space2" has disappeared on the spaces list in the sidebar


  Scenario: User successfully leaves space
    # create new space
    When user of browser clicks on Spaces in the main menu
    And user of browser clicks on Create space button in spaces sidebar
    And user of browser writes "space2" into space name text field
    And user of browser clicks on Create new space button

    # leave space
    And user of browser clicks "space2" on the spaces list in the sidebar
    And user of browser clicks on "Leave space" button in space menu
    And user of browser clicks on yes button
    Then user of browser sees that "space2" has disappeared on the spaces list in the sidebar


  Scenario: User successfully cancels leave space
    # create new space
    When user of browser clicks on Spaces in the main menu
    And user of browser clicks on Create space button in spaces sidebar
    And user of browser writes "space2" into space name text field
    And user of browser clicks on Create new space button

    # leave space
    And user of browser clicks "space2" on the spaces list in the sidebar
    And user of browser clicks on "Leave space" button in space menu
    And user of browser clicks on no button
    Then user of browser sees that "space2" has appeared on the spaces list in the sidebar


  Scenario: User successfully sets space as home space
    When user of browser clicks on Spaces in the main menu
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks on "Toggle default space" button in space menu
    Then user of browser sees that home of "space1" has appeared in the sidebar


  Scenario: User successfully unsets space as home space
    When user of browser clicks on Spaces in the main menu
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks on "Toggle default space" button in space menu
    And user of browser sees that home of "space1" has appeared in the sidebar
    And user of browser clicks on "Toggle default space" button in space menu
    Then user of browser sees that home of "space1" has disappeared in the sidebar


  Scenario: User sees no supporting providers after create new space
    # create new space
    When user of browser clicks on Spaces in the main menu
    And user of browser clicks on Create space button in spaces sidebar
    And user of browser writes "space2" into space name text field
    And user of browser clicks on Create new space button

    Then user of browser sees 0 number of supporting providers of "space2"


  Scenario: User sees that space size is zero right after creating
    # create new space
    When user of browser clicks on Spaces in the main menu
    And user of browser clicks on Create space button in spaces sidebar
    And user of browser writes "space2" into space name text field
    And user of browser clicks on Create new space button

    Then user of browser sees 0 B size of the "space2"


  Scenario: User fails to join to space because of using invalid token
    When user of browser clicks on Spaces in the main menu
    And user of browser clicks Join some space using a space invitation token button
    And user of browser writes "invalid token" into space token text field
    And user of browser clicks Join the space button on Join to a space page
    Then user of browser sees that error popup has appeared


  Scenario: User sees that provider is added to supporters list after supporting space
    When user of browser clicks on Spaces in the main menu
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Providers of "space1" in the sidebar
    Then user of browser sees "oneprovider-1" is on the providers list
    And user of browser sees that length of providers list equals number of supporting providers of "space1"


  Scenario: User generates different support tokens (space has already supported by one provider)
    When user of browser clicks on Spaces in the main menu
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Providers of "space1" in the sidebar
    And user of browser clicks Get support button on providers page
    And user of browser clicks Copy button on Get support page
    And user of browser clicks Generate another token on Get support page
    Then user of browser sees that another token is different than first one


  Scenario: User generates different deploy provider tokens (space has already supported by one provider)
    When user of browser clicks on Spaces in the main menu
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Providers of "space1" in the sidebar
    And user of browser clicks Get support button on providers page
    And user of browser clicks Deploy your own provider tab on get support page
    And user of browser clicks Copy button on Get support page
    And user of browser clicks Generate another token on Get support page
    Then user of browser sees that another token is different than first one


  Scenario: User successfully copies support token (space has already supported by one provider)
    When user of browser clicks on Spaces in the main menu
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Providers of "space1" in the sidebar
    And user of browser clicks Get support button on providers page
    And user of browser clicks Copy button on Get support page
    Then user of browser sees copy token and token in support token text field are the same
    And user of browser sees non-empty copy token