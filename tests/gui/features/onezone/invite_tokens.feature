Feature: Management of invite tokens in Onezone GUI

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1:
                generate_token: false
    And initial spaces configuration in "onezone" Onezone service:
          space1:
              owner: admin
    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, Onezone] page
    And user of [browser1, browser2] logged as [admin, user1] to [Onezone, Onezone] service


  Scenario: User can consume invite token with consumer caveat
    When user of browser1 clicks on Tokens in the main menu
    And user of browser1 creates invite token with following configuration:
          invite type: Invite user to space
          invite target: space1
          usage limit: infinity
          caveats:
            consumer:
              - type: user
                by: id
                value: user1

