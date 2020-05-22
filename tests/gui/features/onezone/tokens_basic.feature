Feature: Management of tokens basic features in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1:
                generate_token: false
    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario Outline: User successfully creates token
    When user of browser clicks on Tokens in the main menu
    And user of browser sees exactly 0 item(s) on tokens list in tokens sidebar
    And user of browser clicks on create new token button in tokens sidebar
    And user of browser chooses <token type> token type in "Create new token" view
    And user of browser clicks on "Create token" button in "Create new token" view
    Then user of browser sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser sees that 1st token's type is <token type>

  Examples:
  | token type|
  | access    |
  | identity  |

  Scenario: User successfully creates invite token
    When user of browser clicks on Tokens in the main menu
    And user of browser sees exactly 0 item(s) on tokens list in tokens sidebar
    And user of browser clicks on create new token button in tokens sidebar
    And user of browser chooses invite token type in "Create new token" view
    And user of browser chooses "Register Oneprovider" invite type
    And user of browser clicks on "Create token" button in "Create new token" view
    Then user of browser sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser sees that 1st token's type is invite

    
  Scenario Outline: User successfully removes token
    When user of browser clicks on Tokens in the main menu
    And user of browser creates 1 <token type> token
    And user of browser sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser clicks on remove button for 1st item on tokens list in tokens page
    And user of browser clicks on "Remove" button in modal "Remove token"
    Then user of browser sees exactly 0 item(s) on tokens list in tokens sidebar

  Examples:
  | token type|
  | access    |
  | identity  |
  | invite    |


  Scenario Outline: User successfully renames token
    When user of browser clicks on Tokens in the main menu
    And user of browser creates 1 <token type> token
    And user of browser sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser clicks on rename button for 1st item on tokens list in tokens page
    And user of browser appends 1st token's name with "-renamed"
    And user of browser confirms changes in 1st token
    Then user of browser sees that 1st token's name includes "renamed"

  Examples:
  | token type|
  | access    |
  | identity  |
  | invite    |


  Scenario Outline: User does not sees name changes after discarding them in tokens sidebar
    When user of browser clicks on Tokens in the main menu
    And user of browser creates 1 <token type> token
    And user of browser sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser clicks on rename button for 1st item on tokens list in tokens page
    And user of browser appends 1st token's name with "-renamed"
    And user of browser discards changes in 1st token
    Then user of browser sees that 1st token's name does not include "renamed"

  Examples:
  | token type|
  | access    |
  | identity  |
  | invite    |


  Scenario: User successfully copies access token
    When user of browser clicks on Tokens in the main menu
    And user of browser clicks on create new token button in tokens sidebar
    And user of browser clicks on "Create token" button in "Create new token" view
    And user of browser sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser clicks on 1st item on tokens list in tokens sidebar
    And user of browser clicks on copy button in token view
    Then user of browser sees that token has been copied correctly


  Scenario: User sees right tokens after filtering them
    When user of browser clicks on Tokens in the main menu
    And user of browser creates 2 access tokens
    And user of browser is idle for 5 seconds
    And user of browser creates 2 identity tokens
    And user of browser creates 2 invite tokens
    And user of browser sees exactly 6 item(s) on tokens list in tokens sidebar

    And user of browser chooses "Access" filter in tokens sidebar
    Then user of browser sees exactly 2 item(s) on tokens list in tokens sidebar
    And user of browser sees that all tokens in tokens sidebar are type of access

    And user of browser chooses "Identity" filter in tokens sidebar
    Then user of browser sees exactly 2 item(s) on tokens list in tokens sidebar
    And user of browser sees that all tokens in tokens sidebar are type of identity

    And user of browser chooses "Invite" filter in tokens sidebar
    Then user of browser sees exactly 2 item(s) on tokens list in tokens sidebar
    And user of browser sees that all tokens in tokens sidebar are type of invite

    And user of browser chooses "All" filter in tokens sidebar
    Then user of browser sees exactly 6 item(s) on tokens list in tokens sidebar


  Scenario Outline: User can revoke and then activate created token
    When user of browser clicks on Tokens in the main menu
    And user of browser creates 1 <token type> token
    And user of browser sees that 1st token is marked as active
    And user of browser clicks on tokens view menu button
    And user of browser clicks "Modify" option in tokens view menu

    And user of browser clicks "Revoke" toggle to revoke token
    And user of browser clicks "Save" button on tokens view
    Then user of browser sees that 1st token is marked as revoked

    And user of browser clicks on tokens view menu button
    And user of browser clicks "Modify" option in tokens view menu
    And user of browser clicks "Revoke" toggle to activate token
    And user of browser clicks "Save" button on tokens view
    Then user of browser sees that 1st token is marked as active

    Examples:
  | token type|
  | access    |
  | identity  |
  | invite    |