Feature: Basic operations on shares directory using REST API, oneclient

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


  Scenario Outline: User fails to remove shares directory
    When using REST, user1 gets ID of the shares directory as the parent of the space "space1" in oneprovider-1
    Then using <client1>, user1 fails to remove shares directory in oneprovider-1

    Examples:
    | client1    |
    | REST       |
    | oneclient1 |


  Scenario Outline: User fails to move shares directory
    When using REST, user1 gets ID of the shares directory as the parent of the space "space1" in oneprovider-1
    Then using <client1>, user1 fails to move shares directory in oneprovider-1

    Examples:
    | client1    |
    | REST       |
    | oneclient1 |


  Scenario Outline: User fails to create file in shares directory
    When using REST, user1 gets ID of the shares directory as the parent of the space "space1" in oneprovider-1
    Then using <client1>, user1 fails to create file "some_name.txt" in shares directory in oneprovider-1

    Examples:
    | client1    |
    | REST       |
    | oneclient1 |


  Scenario: User fails to add QoS requirement to shares directory
    When using REST, user1 gets ID of the shares directory as the parent of the space "space1" in oneprovider-1
    Then using REST, user1 fails to add qos requirement "geo=PL" to shares directory in oneprovider-1


  Scenario: User fails to add metadata to shares directory
    When using REST, user1 gets ID of the shares directory as the parent of the space "space1" in oneprovider-1
    Then using REST, user1 fails to add JSON metadata '{"id": 1}' to shares directory in oneprovider-1


  Scenario: User fails to establish dataset on shares directory
    When using REST, user1 gets ID of the shares directory as the parent of the space "space1" in oneprovider-1
    Then using REST, user1 fails to establish dataset on shares directory in oneprovider-1