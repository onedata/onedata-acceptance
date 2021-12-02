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
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - file1
                    - dir1:
                        - dir2:
                          - file2: 11111
                        - dir3
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
    And opened [browser1, browser2] with [user1, user2] signed in to ["onezone", "onezone"] service


  Scenario Outline: User can create a file in a space using <client1> authenticating themselves with an access token created by <client2>
    When using <client2>, user1 creates token with following configuration:
           name: access_token
           type: access
           caveats:
             read only: False
    And if <client2> is web GUI, user1 copies created token
    And user1 sends token to user2
    Then using <client1>, user2 succeeds to create file named "file3" using received token in "space1" in oneprovider-1

    Examples:
    | client1     | client2 |
    | REST        | web GUI |
    | oneclient1  | REST    |
    | oneclient1  | web GUI |


  Scenario Outline: User cannot use an access token created with <client1> and revoked with <client2> when using <client3>
    When using <client1>, user1 creates token with following configuration:
           name: access_token
           type: access
           caveats:
             read only: False
    And if <client1> is web GUI, user1 copies created token
    And user1 sends token to user2
    And using <client2>, user1 revokes token named "access_token"
    Then using <client3>, user2 fails to create file named "file3" using received token in "space1" in oneprovider-1

    Examples:
    | client1 | client2 | client3    |
    | REST    | web GUI | oneclient1 |
    | web GUI | REST    | REST       |
    | REST    | web GUI | REST       |
    | web GUI | REST    | oneclient1 |


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
    | REST       | web GUI |
    | web GUI    | REST    |


  Scenario: User creates a file with Oneclient but not with REST using token with caveat set for Oneclient interface
    When using web GUI, user1 creates token with following configuration:
           name: access_token
           type: access
           caveats:
             read only: False
             interface: Oneclient
    And using web GUI, user1 copies created token
    And user1 sends token to user2
    And user2 mounts oneclient using received token
    Then using REST, user2 fails to create file named "file3" using received token in "space1" in oneprovider-1
    And using oneclient1, user2 succeeds to create file named "file3" using received token in "space1" in oneprovider-1


  Scenario: User creates a file with REST but not with Oneclient using token with caveat set for REST interface
    When using web GUI, user1 creates token with following configuration:
           name: access_token
           type: access
           caveats:
             read only: False
             interface: REST
    And using web GUI, user1 copies created token
    And user1 sends token to user2
    Then using oneclient1, user2 fails to create file named "file3" using received token in "space1" in oneprovider-1
    And using REST, user2 succeeds to create file named "file3" using received token in "space1" in oneprovider-1


  Scenario: Using REST, user can create a group in a space after getting token with caveat set for onezone service, created by web GUI
    When using web GUI, user1 creates token with following configuration:
        name: access_token
        type: access
        caveats:
          service:
            Service:
              - dev-onezone
    And using web GUI, user1 copies created token
    And user1 sends token to user2

    Then user2 creates group "group4" using REST using received token in "onezone" Onezone service
    And using web GUI, user1 sees that group named "group1" has appeared in "onezone" Onezone service


  Scenario Outline: Using <client1>, user cannot create file after getting token with caveat set only for onezone service, created by web GUI
    When using web GUI, user1 creates token with following configuration:
        name: access_token
        type: access
        caveats:
          service:
            Service:
              - dev-onezone
    And using web GUI, user1 copies created token
    And user1 sends token to user2

    Then using <client1>, user2 fails to create file named "file3" using received token in "space1" in oneprovider-1
    And using web GUI, user1 fails to see item named "file3" in "space1" in oneprovider-1

    Examples:
    | client1     |
    | REST        |
    | oneclient1  |


  Scenario Outline: Using <client1>, user can create file after getting token with caveat set for oneprovider service, created by web GUI
    When using web GUI, user1 creates token with following configuration:
        name: access_token
        type: access
        caveats:
          service:
            Service:
              - Any Oneprovider
    And using web GUI, user1 copies created token
    And user1 sends token to user2

    Then using <client1>, user2 succeeds to create file named "file3" using received token in "space1" in oneprovider-1
    And using web GUI, user1 succeeds to see item named "file3" in "space1" in oneprovider-1

    Examples:
    | client1     |
    | REST        |
    | oneclient1  |


  Scenario: Using REST, user cannot create a group in a space after getting token with caveat set only for oneprovider service, created by web GUI
    When using web GUI, user1 creates token with following configuration:
        name: access_token
        type: access
        caveats:
          service:
            Service:
              - Any Oneprovider
    And using web GUI, user1 copies created token
    And user1 sends token to user2

    Then user2 fails to create group "group1" using REST using received token in "onezone" Onezone service
    And using web GUI, user1 does not see group named group1 in "onezone" Onezone service


  Scenario Outline: Using <client1>, user fails to create file after getting token with caveat set only for "read only", created by web GUI
    When using web GUI, user1 creates token with following configuration:
           name: access_token
           type: access
           caveats:
              read only: True
    And using web GUI, user1 copies created token
    And user1 sends token to user2

    Then using <client1>, user2 fails to create file named "file3" using received token in "space1" in oneprovider-1
    And using web GUI, user1 fails to see item named "file3" in "space1" in oneprovider-1

    Examples:
    | client1     |
    | REST        |
    | oneclient1  |


  Scenario Outline: Using <client1>, user can see file after getting token with caveat set for "read only", created by web GUI
    When using web GUI, user1 creates token with following configuration:
           name: access_token
           type: access
           caveats:
              read only: True
    And using web GUI, user1 copies created token
    And user1 sends token to user2
    And user2 mounts oneclient using received token
    Then using <client1>, user2 succeeds to see item named "file1" using received access token in "space1" in oneprovider-1

    Examples:
    | client1     |
    | REST        |
    | oneclient1  |


  Scenario Outline: Using <client1>, user can create file after getting token with expiration time set in caveat, created by web GUI
    When using web GUI, user1 creates token with following configuration:
        name: access_token
        type: access
        caveats:
          expiration:
            after: 10
    And using web GUI, user1 copies created token
    And user1 sends token to user2

    Then using <client1>, user2 succeeds to create file named "file3" using received token in "space1" in oneprovider-1
    And using web GUI, user1 succeeds to see item named "file3" in "space1" in oneprovider-1

    Examples:
    | client1     |
    | REST        |
    | oneclient1  |


  Scenario Outline: Using <client1>, user cannot create file after getting token with expiration time set in caveat, created by web GUI
    When using web GUI, user1 creates token with following configuration:
        name: access_token
        type: access
        caveats:
          expiration:
            after: 1
    And using web GUI, user1 copies created token
    And user1 sends token to user2
    And user2 is idle for 70 seconds
    Then using <client1>, user2 fails to create file named "file3" using received token in "space1" in oneprovider-1
    And using web GUI, user1 fails to see item named "file3" in "space1" in oneprovider-1

    Examples:
    | client1     |
    | REST        |
    | oneclient1  |

