Feature: Management of tokens basic features in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user:
                generate_token: false
    And initial spaces configuration in "onezone" Onezone service:
            space1:
                owner: space-owner-user
    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario Outline: User successfully removes token
    When user of browser clicks on Tokens in the main menu
    And user of browser creates 1 <token type> token
    And user of browser sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser clicks on remove button for token named "<token name>" on tokens list
    And user of browser clicks on "Remove" button in modal "Remove token"
    Then user of browser sees exactly 0 item(s) on tokens list in tokens sidebar

    Examples:
    | token type| token name    |
    | access    | access_token   |
    | identity  | identity_token |
    | invite    | invite_token   |


  Scenario Outline: User successfully revokes and then activates created token
    When user of browser clicks on Tokens in the main menu
    And user of browser creates 1 <token type> token
    And user of browser sees that token named "<token name>" is marked as active
    And user of browser clicks on tokens view menu button
    And user of browser clicks "Modify" option in tokens view menu

    And user of browser clicks "Revoke" toggle to revoke token
    And user of browser clicks "Save" button on tokens view
    Then user of browser sees that token named "<token name>" is marked as revoked

    And user of browser clicks on tokens view menu button
    And user of browser clicks "Modify" option in tokens view menu
    And user of browser clicks "Revoke" toggle to activate token
    And user of browser clicks "Save" button on tokens view
    Then user of browser sees that token named "<token name>" is marked as active

    Examples:
    | token type| token name     |
    | access    | access_token   |
    | identity  | identity_token |
    | invite    | invite_token   |


  Scenario Outline: User successfully deletes selected obsolete token

    # create obsolete tokens
    When user of browser creates token with following configuration:
        name: identity_token_1
        type: identity
        caveats:
          expiration:
            after: -10

    And user of browser creates token with following configuration:
        name: identity_token_2
        type: identity
        caveats:
          expiration:
            after: -10

    And user of browser creates token with following configuration:
        name: access_token_1
        type: access
        caveats:
          expiration:
            after: -10

    And user of browser creates token with following configuration:
        name: access_token_2
        type: access
        caveats:
          expiration:
            after: -10

    And user of browser creates token with following configuration:
        name: invite_token_1
        type: invite
        invite type: Invite user to space
        invite target: space1
        caveats:
          expiration:
            after: -10

    And user of browser creates token with following configuration:
        name: invite_token_2
        type: invite
        invite type: Invite user to space
        invite target: space1
        caveats:
          expiration:
            after: -10

    And user of browser clicks on "Clean up obsolete tokens" button in tokens sidebar
    And user of browser sees that "Clean up obsolete tokens" modal has appeared

    And user of browser deselects "<token_to_save>" in modal "Clean up obsolete tokens"
    And user of browser clicks on "Remove" button in modal "Clean up obsolete tokens"

    Then user of browser sees "<token_to_save>" in token list on tokens page sidebar
    And user of browser does not see "<token_to_delete>" in token list on tokens page sidebar

    Examples:
    | token_to_save     | token_to_delete   |
    | invite_token_1    | invite_token_2    |
    | access_token_1    | access_token_2    |
    | identity_token_1  | identity_token_2  |


  Scenario: User successfully deletes obsolete tokens of selected type

    # create obsolete tokens
    When user of browser creates token with following configuration:
        name: access_token_1
        type: access
        caveats:
          expiration:
            after: -10

    And user of browser creates token with following configuration:
        name: invite_token_1
        type: invite
        invite type: Invite user to space
        invite target: space1
        caveats:
          expiration:
            after: -10

    And user of browser clicks on "Clean up obsolete tokens" button in tokens sidebar
    And user of browser sees that "Clean up obsolete tokens" modal has appeared

    And user of browser deselects "Invitation tokens" type in modal "Clean up obsolete tokens"
    And user of browser clicks on "Remove" button in modal "Clean up obsolete tokens"

    Then user of browser sees "invite_token_1" in token list on tokens page sidebar
    And user of browser does not see "access_token_1" in token list on tokens page sidebar