Feature: Basic operations on the special share root directory,
  which is the parent of a share. Using REST API and oneclient.

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


  Scenario Outline: User fails to remove the shares directory
    When using REST, user1 gets ID of the shares directory from the share details in the space "space1" in oneprovider-1
    Then using <client1>, user1 fails to remove the shares directory in oneprovider-1

    Examples:
    | client1    |
    | REST       |
    | oneclient1 |


  Scenario Outline: User fails to move the shares directory
    When using REST, user1 gets ID of the shares directory from the share details in the space "space1" in oneprovider-1
    Then using <client1>, user1 fails to move the shares directory in oneprovider-1

    Examples:
    | client1    |
    | REST       |
    | oneclient1 |


  Scenario Outline: User fails to create file in the shares directory
    When using REST, user1 gets ID of the shares directory from the share details in the space "space1" in oneprovider-1
    Then using <client1>, user1 fails to create file "some_name.txt" in the shares directory in oneprovider-1

    Examples:
    | client1    |
    | REST       |
    | oneclient1 |


  Scenario: User fails to add QoS requirement to the shares directory
    When using REST, user1 gets ID of the shares directory from the share details in the space "space1" in oneprovider-1
    Then using REST, user1 fails to add QoS requirement "geo=PL" to the shares directory in oneprovider-1


  Scenario: User fails to add metadata to the shares directory
    When using REST, user1 gets ID of the shares directory from the share details in the space "space1" in oneprovider-1
    Then using REST, user1 fails to add JSON metadata '{"id": 1}' to the shares directory in oneprovider-1


  Scenario: User fails to establish dataset on the shares directory
    When using REST, user1 gets ID of the shares directory from the share details in the space "space1" in oneprovider-1
    Then using REST, user1 fails to establish dataset on the shares directory in oneprovider-1