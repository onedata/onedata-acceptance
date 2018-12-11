Feature: Management of access tokens in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1:
                generate_token: false
    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User successfully creates access token
    When user of browser clicks on Tokens in the sidebar
    And user of browser sees exactly 0 item(s) on tokens list in tokens sidebar
    And user of browser clicks on "Create new token" button in tokens sidebar
    Then user of browser sees exactly 1 item(s) on tokens list in tokens sidebar


  Scenario: User successfully removes access token
    When user of browser clicks on Tokens in the sidebar
    And user of browser clicks on "Create new token" button in tokens sidebar
    And user of browser sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser clicks on remove button for 1st item on tokens list in tokens page
    And user of browser sees exactly 0 item(s) on tokens list in tokens sidebar


  Scenario: User successfully copies access token
    When user of browser clicks on Tokens in the sidebar
    And user of browser clicks on "Create new token" button in tokens sidebar
    And user of browser sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser clicks on copy button for 1st item on tokens list in tokens page
    And user of browser sees that token for 1st item on tokens list in tokens sidebar has been copied correctly
