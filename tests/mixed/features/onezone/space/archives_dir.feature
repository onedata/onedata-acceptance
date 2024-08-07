Feature: Basic operations on archives directory using REST API, oneclient

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


  Scenario Outline: User fails to remove archives directory
    When using REST, user1 gets ID of the archives directory as the parent of the space "space1" in oneprovider-1
    Then using <client1>, user1 fails to remove archives directory in oneprovider-1

    Examples:
    | client1    |
    | REST       |
    | oneclient1 |


  Scenario Outline: User fails to move archives directory
    When using REST, user1 gets ID of the archives directory as the parent of the space "space1" in oneprovider-1
    Then using <client1>, user1 fails to move archives directory in oneprovider-1

    Examples:
    | client1    |
    | REST       |
    | oneclient1 |


  Scenario Outline: User fails to create file in archives directory
    When using REST, user1 gets ID of the archives directory as the parent of the space "space1" in oneprovider-1
    Then using <client1>, user1 fails to create file "some_name.txt" in archives directory in oneprovider-1

    Examples:
    | client1    |
    | REST       |
    | oneclient1 |


  Scenario: User fails to add QoS requirement to archives directory
    When using REST, user1 gets ID of the archives directory as the parent of the space "space1" in oneprovider-1
    Then using REST, user1 fails to add qos requirement "geo=PL" to archives directory in oneprovider-1


  Scenario: User fails to add metadata to archives directory
    When using REST, user1 gets ID of the archives directory as the parent of the space "space1" in oneprovider-1
    Then using REST, user1 fails to add JSON metadata '{"id": 1}' to archives directory in oneprovider-1


  Scenario: User fails to establish dataset on archives directory
    When using REST, user1 gets ID of the archives directory as the parent of the space "space1" in oneprovider-1
    Then using REST, user1 fails to establish dataset on archives directory in oneprovider-1