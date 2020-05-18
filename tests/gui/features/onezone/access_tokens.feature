Feature: Management of access tokens in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1:
                generate_token: false
    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


#  Scenario Outline: User successfully creates token
#    When user of browser clicks on Tokens in the main menu
#    And user of browser sees exactly 0 item(s) on tokens list in tokens sidebar
#    And user of browser clicks on create new token button in tokens sidebar
#    And user of browser chooses <token type> token type in "Create new token" view
#    And user of browser clicks on "Create token" button in "Create new token" view
#    Then user of browser sees exactly 1 item(s) on tokens list in tokens sidebar
#
#  Examples:
#  | token type|
#  | access    |
#  | identity  |

  Scenario: User successfully creates invite token
    When user of browser clicks on Tokens in the main menu
    And user of browser sees exactly 0 item(s) on tokens list in tokens sidebar
    And user of browser clicks on create new token button in tokens sidebar
    And user of browser chooses invite token type in "Create new token" view
    And user of browser chooses "Register Oneprovider" invite type
    And user of browser clicks on "Create token" button in "Create new token" view
    Then user of browser sees exactly 1 item(s) on tokens list in tokens sidebar
    #TODO to nie działa
    And user of browser sees that 1st token type is invite
#
#  Scenario Outline: User successfully removes token
#    When user of browser clicks on Tokens in the main menu
#    And user of browser clicks on create new token button in tokens sidebar
#    And user of browser chooses <token type> token type in "Create new token" view
#    And user of browser clicks on "Create token" button in "Create new token" view
#    And user of browser sees exactly 1 item(s) on tokens list in tokens sidebar
#    And user of browser clicks on remove button for 1st item on tokens list in tokens page
#    And user of browser clicks on "Remove" button in modal "Remove token"
#    And user of browser sees exactly 0 item(s) on tokens list in tokens sidebar
#
#  Examples:
#  | token type|
#  | access    |
#  | identity  |
#
#
#  Scenario: User successfully copies access token
#    When user of browser clicks on Tokens in the main menu
#    And user of browser clicks on create new token button in tokens sidebar
#    And user of browser clicks on "Create token" button in "Create new token" view
#    And user of browser sees exactly 1 item(s) on tokens list in tokens sidebar
#    And user of browser clicks on 1st item on tokens list in tokens sidebar
#    And user of browser clicks on copy button in token view
#    And user of browser sees that token has been copied correctly
