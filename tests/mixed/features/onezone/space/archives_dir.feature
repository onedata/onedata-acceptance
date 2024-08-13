Feature: Basic operations on the special archives root directory for a space,
  which is the root for all archives created in the space.
  Using REST API and oneclient.

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


  Scenario Outline: User fails to remove the archives directory
    When using REST, user1 gets ID of the archives directory from the space "space1" details in oneprovider-1
    Then using <client1>, user1 fails to remove the archives directory in oneprovider-1

    Examples:
    | client1    |
    | REST       |
    | oneclient1 |


  Scenario Outline: User fails to move the archives directory
    When using REST, user1 gets ID of the archives directory from the space "space1" details in oneprovider-1
    Then using <client1>, user1 fails to move the archives directory in oneprovider-1

    Examples:
    | client1    |
    | REST       |
    | oneclient1 |


  Scenario Outline: User fails to create file in the archives directory
    When using REST, user1 gets ID of the archives directory from the space "space1" details in oneprovider-1
    Then using <client1>, user1 fails to create file "some_name.txt" in the archives directory in oneprovider-1

    Examples:
    | client1    |
    | REST       |
    | oneclient1 |


  Scenario: User fails to add QoS requirement to the archives directory
    When using REST, user1 gets ID of the archives directory from the space "space1" details in oneprovider-1
    Then using REST, user1 fails to add QoS requirement "geo=PL" to the archives directory in oneprovider-1


  Scenario: User fails to add metadata to the archives directory
    When using REST, user1 gets ID of the archives directory from the space "space1" details in oneprovider-1
    Then using REST, user1 fails to add JSON metadata '{"id": 1}' to the archives directory in oneprovider-1


  Scenario: User fails to establish dataset on the archives directory
    When using REST, user1 gets ID of the archives directory from the space "space1" details in oneprovider-1
    Then using REST, user1 fails to establish dataset on the archives directory in oneprovider-1