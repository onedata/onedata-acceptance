Feature: Basic operations on user root directory using REST API, oneclient

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
    And opened browser with user1 signed in to "onezone" service
    And oneclient mounted using token by user1


  Scenario Outline: User fails to remove user root directory
    When using REST, user1 gets ID of the user root directory as the parent of the space "space1" in oneprovider-1
    Then using <client1>, user1 fails to remove user root directory in oneprovider-1

    Examples:
    | client1    |
    | REST       |
    | oneclient1 |


  Scenario Outline: User fails to move user root directory
    When using REST, user1 gets ID of the user root directory as the parent of the space "space1" in oneprovider-1
    Then using <client1>, user1 fails to move user root directory in oneprovider-1

    Examples:
    | client1    |
    | REST       |
    | oneclient1 |


  Scenario Outline: User fails to create file in user root directory
    When using REST, user1 gets ID of the user root directory as the parent of the space "space1" in oneprovider-1
    Then using <client1>, user1 fails to create file "some_name.txt" in user root directory in oneprovider-1

    Examples:
    | client1    |
    | REST       |
    | oneclient1 |


  Scenario: User fails to add QoS requirement to user root directory
    When using REST, user1 gets ID of the user root directory as the parent of the space "space1" in oneprovider-1
    Then using REST, user1 fails to add qos requirement "geo=PL" to user root directory in oneprovider-1


  Scenario: User fails to add metadata to user root directory
    When using REST, user1 gets ID of the user root directory as the parent of the space "space1" in oneprovider-1
    Then using REST, user1 fails to add JSON metadata '{"id": 1}' to user root directory in oneprovider-1


  Scenario: User fails to establish dataset on user root directory
    When using REST, user1 gets ID of the user root directory as the parent of the space "space1" in oneprovider-1
    Then using REST, user1 fails to establish dataset on user root directory in oneprovider-1