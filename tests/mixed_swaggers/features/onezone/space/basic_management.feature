Feature: Basic management
  Basic management of space in Onezone using GUI and REST API

  Background:
    Given initial users configuration in "z1" Onezone service:
            - user1
    And initial spaces configuration in "z1" Onezone service:
        space1:
            owner: user1
            providers:
                - p1:
                    storage: NFS
                    size: 1000000
    And opened browser with user1 logged to "z1 onezone" service


  Scenario Outline: User leaves space using <client1> and using <client2> he sees that it has been left
    When using <client1>, user1 leaves space named "space1" in "z1" Onezone service
    Then using <client2>, user1 sees that space named "space1" has disappeared from "z1" Onezone service

  Examples:
  | client1 | client2   |
  | web GUI | REST      |
  | REST    | web GUI   |


  Scenario Outline: User renames space using <client1> and using <client2> he sees that it has been renamed
    When using <client1>, user1 renames space named "space1" to "NewNameSpace" in "z1" Onezone service
    Then using <client2>, user1 sees that space named "space1" has been renamed to "NewNameSpace" in "z1" Onezone service

  Examples:
  | client1 | client2   |
  | web GUI | REST      |
  | REST    | web GUI   |


  Scenario Outline: User set space as home using <client1> and using <client2> he sees that it has been set as home space
    When using <client1>, user1 set space named "space1" as home space in "z1" Onezone service
    Then using <client2>, user1 sees that space named "space1" has been set as home in "z1" Onezone service

  Examples:
  | client1 | client2   |
  | web GUI | REST      |
  | REST    | web GUI   |


  Scenario Outline: User unsupport space using <client1> and using <client2> he sees that it has been unsupported
    When using <client1>, user1 removes support from provider "p1" for space named "space1" in "z1" Onezone service
    Then using <client2>, user1 sees that there is no supporting provider named "p1" for space named "space1" in "z1" Onezone service

  Examples:
  | client1 | client2   |
  | web GUI | REST      |
  | REST    | web GUI   |


  Scenario: User removes space using <client1> and using <client2> he sees that it has been removed
    When using REST, user1 removes space named "space1" in "z1" Onezone service
    Then using web GUI, user1 sees that space named "space1" has disappeared from "z1" Onezone service

