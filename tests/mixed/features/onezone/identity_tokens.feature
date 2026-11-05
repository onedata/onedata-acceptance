Feature: Identity tokens tests

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: user1
            providers:
              - oneprovider-1:
                  storage: posix
                  size: 1000000
    And opened [browser1, browser2] with [user1, user2] signed in to ["onezone", "onezone"] service


  Scenario: User set in access token caveat succeeds to use that token only with their identity token
    When using web gui, user1 creates token with following configuration:
           name: access_token_for_user2
           type: access
           caveats:
             read only: False
             consumer:
               - type: user
                 by: id
                 consumer name: user2
    And using web gui, user1 copies created token named "access_token_for_user2"
    And user1 sends token to user2
    And using REST, user2 fails to create file named "file1" using received token in "space1" in oneprovider-1
    And using web gui, user2 creates token with following configuration:
           name: identity_token_of_user2
           type: identity
    And using web gui, user2 copies created token named "identity_token_of_user2"
    Then using REST with identity token, user2 succeeds to create file named "file1" using received token in "space1" in oneprovider-1
    And using web gui, user1 succeeds to see item named "file1" in "space1" in oneprovider-1



  Scenario: User not set in access token caveat fails to use that token
    When using web gui, user1 creates token with following configuration:
           name: access_token_for_user1
           type: access
           caveats:
             read only: False
             consumer:
               - type: user
                 by: id
                 consumer name: user1
    And using web gui, user1 copies created token named "access_token_for_user2"
    And user1 sends token to user2
    And using REST, user2 fails to create file named "file1" using received token in "space1" in oneprovider-1
    And using web gui, user2 creates token with following configuration:
           name: identity_token_of_user2
           type: identity
    And using web gui, user2 copies created token named "identity_token_of_user2"
    Then using REST with identity token, user2 fails to create file named "file1" using received token in "space1" in oneprovider-1
    And using web gui, user1 fails to see item named "file1" in "space1" in oneprovider-1
