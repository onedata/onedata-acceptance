Feature: Basic operations on trash directory using REST API, oneclient

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
    And oneclient mounted using token by user1


  Scenario Outline: User fails to remove trash directory
    When using REST, user1 gets ID of the trash directory as the parent of the space "space1" in oneprovider-1
    Then using <client1>, user1 fails to remove trash directory in oneprovider-1

    Examples:
    | client1    |
    | REST       |
    | oneclient1 |


  Scenario Outline: User fails to move trash directory
    When using REST, user1 gets ID of the trash directory as the parent of the space "space1" in oneprovider-1
    Then using <client1>, user1 fails to move trash directory in oneprovider-1

    Examples:
    | client1    |
    | REST       |
    | oneclient1 |


  Scenario Outline: User fails to create file in trash directory
    When using REST, user1 gets ID of the trash directory as the parent of the space "space1" in oneprovider-1
    Then using <client1>, user1 fails to create file "some_name.txt" in trash directory in oneprovider-1

    Examples:
    | client1    |
    | REST       |
    | oneclient1 |


  Scenario: User fails to add QoS requirement to trash directory
    When using REST, user1 gets ID of the trash directory as the parent of the space "space1" in oneprovider-1
    Then using REST, user1 fails to add qos requirement "geo=PL" to trash directory in oneprovider-1


  Scenario: User fails to add metadata to trash directory
    When using REST, user1 gets ID of the trash directory as the parent of the space "space1" in oneprovider-1
    Then using REST, user1 fails to add JSON metadata '{"id": 1}' to trash directory in oneprovider-1


  Scenario: User fails to establish dataset on trash directory
    When using REST, user1 gets ID of the trash directory as the parent of the space "space1" in oneprovider-1
    Then using REST, user1 fails to establish dataset on trash directory in oneprovider-1
