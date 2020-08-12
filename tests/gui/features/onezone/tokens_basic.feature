Feature: Management of tokens basic features in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1:
                generate_token: false
    And initial spaces configuration in "onezone" Onezone service:
            space1:
                owner: user1
    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario Outline: User successfully creates token with default settings
    When user of browser clicks on Tokens in the main menu
    And user of browser sees exactly 0 item(s) on tokens list in tokens sidebar
    And user of browser clicks on "Create new token" button in tokens sidebar
    And user of browser types "Token1" to token name input box in "Create new token" view
    And user of browser chooses <token type> token type in "Create new token" view
    And user of browser clicks on "Create token" button in "Create new token" view
    Then user of browser sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser sees that there is token named "Token1" on tokens list
    And user of browser sees that "Token1" token's type is <token type>

    Examples:
    | token type|
    | access    |
    | identity  |


  Scenario: User successfully creates oneprovider invite token
    When user of browser clicks on Tokens in the main menu
    And user of browser sees exactly 0 item(s) on tokens list in tokens sidebar
    And user of browser clicks on "Create new token" button in tokens sidebar
    And user of browser types "Token1" to token name input box in "Create new token" view
    And user of browser chooses invite token type in "Create new token" view
    And user of browser chooses "Register Oneprovider" invite type
    And user of browser clicks on "Create token" button in "Create new token" view
    Then user of browser sees exactly 1 item(s) on tokens list in tokens sidebar
    And user of browser sees that there is token named "Token1" on tokens list
    And user of browser sees that "Token1" token's type is invite


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


  Scenario Outline: User successfully renames token
    When user of browser clicks on Tokens in the main menu
    And user of browser creates 1 <token type> token
    And user of browser clicks on rename button for token named "<token name>" on tokens list
    And user of browser appends "-renamed" to name of token named "<token name>"
    And user of browser confirms changes in token named "<token name>"
    And user of browser sees exactly 1 item(s) on tokens list in tokens sidebar
    Then user of browser sees that there is token named "<token name renamed>" on tokens list

    Examples:
    | token type| token name     | token name renamed     |
    | access    | access_token   | access_token-renamed   |
    | identity  | identity_token | identity_token-renamed |
    | invite    | invite_token   | invite_token-renamed   |


  Scenario: User sees right tokens after filtering them
    When user of browser clicks on Tokens in the main menu
    And user of browser creates 2 access tokens
    And user of browser is idle for 5 seconds
    And user of browser creates 2 identity tokens
    And user of browser creates 2 invite tokens
    And user of browser sees exactly 6 item(s) on tokens list in tokens sidebar

    And user of browser chooses "Access" filter in tokens sidebar
    Then user of browser sees exactly 2 item(s) on tokens list in tokens sidebar
    And user of browser sees that there is token named "access_token" on tokens list
    And user of browser sees that there is token named "access_token1" on tokens list
    And user of browser sees that all tokens in tokens sidebar are type of access

    And user of browser chooses "Identity" filter in tokens sidebar
    Then user of browser sees exactly 2 item(s) on tokens list in tokens sidebar
    And user of browser sees that there is token named "identity_token" on tokens list
    And user of browser sees that there is token named "identity_token1" on tokens list
    And user of browser sees that all tokens in tokens sidebar are type of identity

    And user of browser chooses "Invite" filter in tokens sidebar
    Then user of browser sees exactly 2 item(s) on tokens list in tokens sidebar
    And user of browser sees that there is token named "invite_token" on tokens list
    And user of browser sees that there is token named "invite_token1" on tokens list
    And user of browser sees that all tokens in tokens sidebar are type of invite

    And user of browser chooses "All" filter in tokens sidebar
    Then user of browser sees exactly 6 item(s) on tokens list in tokens sidebar


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


  Scenario: User successfully creates access token with all caveats
    When user of browser creates token with following configuration:
        type: access
        caveats:
          expiration:
            after: 10
          region:
            allow: True
            region codes:
              - Europe
          country:
            allow: True
            country codes:
              - BS
          ASN:
            - 64496
          IP:
            - 192.0.2.1
          consumer:
            - type: user
              by: id
              consumer name: user1
          service:
            Service:
              - Any Oneprovider
            Service Onepanel:
              - Any Oneprovider Onepanel
          interface: REST
          read only: True
          path:
            - space: space1
              path: /
          object ID:
            - 0000000000522CB067756964233739396665383433613330383664376465393632636539643462666561313362636835363837233166373864336661623561326166633135373739363737653532656166636231636837653434
    Then user of browser sees that created token configuration is as following:
          type: Access
          caveats:
            expiration:
              set: True
            region:
              allow: True
              region codes:
                - Europe
            country:
              allow: True
              country codes:
                - BS
            ASN:
              - 64496
            IP:
              - 192.0.2.1/32
            consumer:
              - type: user
                by: name
                consumer name: user1
            service:
              - Any Oneprovider
              - Any Oneprovider Onepanel
            interface: REST
            read only: True
            path:
              - space: space1
                path: /
            object ID:
              - 0000000000522CB067756964233739396665383433613330383664376465393632636539643462666561313362636835363837233166373864336661623561326166633135373739363737653532656166636231636837653434
