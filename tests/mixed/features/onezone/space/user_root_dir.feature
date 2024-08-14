Feature: Basic operations on the special user root directory which is
  user`s home onedata directory, parent directory of all user`s spaces.
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


  Scenario Outline: User fails to remove the user root directory
    When using REST, user1 gets ID of the user root directory from the space "space1" details in oneprovider-1
    Then using <client1>, user1 fails to remove the user root directory in oneprovider-1

    Examples:
    | client1    |
    | REST       |
    | oneclient1 |


  Scenario: User fails to remove the user root directory using file path
    When using REST, user1 gets ID of the user root directory from the space "space1" details in oneprovider-1
    Then using oneclient1, user1 fails to remove the user root directory using file path in oneprovider-1


  Scenario Outline: User fails to move the user root directory
    When using REST, user1 gets ID of the user root directory from the space "space1" details in oneprovider-1
    Then using <client1>, user1 fails to move the user root directory in oneprovider-1

    Examples:
    | client1    |
    | REST       |
    | oneclient1 |


  Scenario: User fails to move the user root directory using file path
    When using REST, user1 gets ID of the user root directory from the space "space1" details in oneprovider-1
    Then using oneclient1, user1 fails to move the user root directory using file path in oneprovider-1


  Scenario Outline: User fails to create file in the user root directory
    When using REST, user1 gets ID of the user root directory from the space "space1" details in oneprovider-1
    Then using <client1>, user1 fails to create file "some_name.txt" in the user root directory in oneprovider-1

    Examples:
    | client1    |
    | REST       |
    | oneclient1 |


  Scenario: User fails to create file in the user root directory using file path
    When using REST, user1 gets ID of the user root directory from the space "space1" details in oneprovider-1
    Then using oneclient1, user1 fails to create file "some_name.txt" in the user root directory using file path in oneprovider-1


  Scenario: User fails to add QoS requirement to the user root directory
    When using REST, user1 gets ID of the user root directory from the space "space1" details in oneprovider-1
    Then using REST, user1 fails to add QoS requirement "geo=PL" to the user root directory in oneprovider-1


  Scenario: User fails to add metadata to the user root directory
    When using REST, user1 gets ID of the user root directory from the space "space1" details in oneprovider-1
    Then using REST, user1 fails to add JSON metadata '{"id": 1}' to the user root directory in oneprovider-1


  Scenario: User fails to establish dataset on the user root directory
    When using REST, user1 gets ID of the user root directory from the space "space1" details in oneprovider-1
    Then using REST, user1 fails to establish dataset on the user root directory in oneprovider-1