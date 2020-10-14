Feature: Access tokens tests

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


  Scenario Outline: User can create a file in a space using <client1> authenticating themselves with an access token created by <client2>
    When using <client2>, user1 creates token with following configuration:
           name: access_token
           type: access
           caveats:
             read only: False
    And if <client2> is web gui, user1 copies created token
    And user1 sends token to user2
    Then using <client1>, user2 succeeds to create file named "file1" using received token in "space1" in oneprovider-1

    Examples:
    | client1     | client2 |
    | REST        | web gui |
    | oneclient2  | REST    |
    | oneclient1  | web gui |


  Scenario Outline: User cannot use an access token created with <client1> and revoked with <client2> when using <client3>
    When using <client1>, user1 creates token with following configuration:
           name: access_token
           type: access
           caveats:
             read only: False
    And if <client1> is web gui, user1 copies created token
    And user1 sends token to user2
    And using <client2>, user1 revokes token named "access_token"
    Then using <client3>, user2 fails to create file named "file1" using received token in "space1" in oneprovider-1

    Examples:
    | client1 | client2 | client3    |
    | REST    | web gui | oneclient1 |
    | web gui | REST    | REST       |
    | REST    | web gui | REST       |
    | web gui | REST    | oneclient1 |


  Scenario Outline: User sees all token caveats in token configuration using <client1> after setting them in new access token with <client2>
    When using <client1>, user1 creates token with following configuration:
        name: access_token
        type: access
        caveats:
          expiration:
            after: 10
          region:
            allow: True
            region codes:
              - Europe
          country:
            allow: False
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
    Then using <client2>, user1 sees that created token configuration is as following:
          name: access_token
          type: Access
          caveats:
            expiration:
              set: True
            region:
              allow: True
              region codes:
                - Europe
            country:
              allow: False
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

    Examples:
    | client1    | client2 |
    | REST       | web gui |
    | web gui    | REST    |


  Scenario: User creates a file with Oneclient but not with REST using token with caveat set for Oneclient interface
    When using web gui, user1 creates token with following configuration:
           name: access_token
           type: access
           caveats:
             read only: False
             interface: Oneclient
    And using web gui, user1 copies created token
    And user1 sends token to user2
    And user2 mounts oneclient in /home/user2/onedata using received token
    Then using REST, user2 fails to create file named "file1" using received token in "space1" in oneprovider-1
    And using oneclient1, user2 succeeds to create file named "file1" using received token in "space1" in oneprovider-1


  Scenario: User creates a file with REST but not with Oneclient using token with caveat set for REST interface
    When using web gui, user1 creates token with following configuration:
           name: access_token
           type: access
           caveats:
             read only: False
             interface: REST
    And using web gui, user1 copies created token
    And user1 sends token to user2
    Then using oneclient1, user2 fails to create file named "file1" using received token in "space1" in oneprovider-1
    And using REST, user2 succeeds to create file named "file1" using received token in "space1" in oneprovider-1
