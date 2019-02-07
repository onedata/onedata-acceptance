Feature: Basic management
  Basic management of space in Onezone using GUI and REST API

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
    And opened browsers with [admin, user1] logged to [oneprovider-1 provider panel, onezone] service


  Scenario Outline: User leaves space using <client1> and using <client2> he sees that it has been left
    When using <client1>, user1 leaves space named "space1" in "onezone" Onezone service
    Then using <client2>, user1 sees that space named "space1" has disappeared from "onezone" Onezone service

  Examples:
  | client1 | client2   |
  | web GUI | REST      |
  | REST    | web GUI   |


  Scenario Outline: User renames space using <client1> and using <client2> he sees that it has been renamed
    When using <client1>, user1 renames space named "space1" to "NewNameSpace" in "onezone" Onezone service
    Then using <client2>, user1 sees that space named "space1" has been renamed to "NewNameSpace" in "onezone" Onezone service

  Examples:
  | client1 | client2   |
  | web GUI | REST      |
  | REST    | web GUI   |


  Scenario Outline: User set space as home using <client1> and using <client2> he sees that it has been set as home space
    When using <client1>, user1 set space named "space1" as home space in "onezone" Onezone service
    Then using <client2>, user1 sees that space named "space1" has been set as home in "onezone" Onezone service

  Examples:
  | client1 | client2   |
  | web GUI | REST      |
  | REST    | web GUI   |


  Scenario Outline: User unsupport space using <client1> and using <client2> he sees that it has been unsupported
    When using <client1>, admin removes support from provider "oneprovider-1" for space named "space1" in "onezone" Onezone service
    Then using <client2>, user1 sees that there is no supporting provider "oneprovider-1" for space named "space1" in "onezone" Onezone service

  Examples:
  | client1 | client2   |
  | web GUI | REST      |
  | REST    | web GUI   |


  Scenario: User removes space using <client1> and using <client2> he sees that it has been removed
    When using REST, user1 removes space named "space1" in "onezone" Onezone service
    Then using web GUI, user1 sees that space named "space1" has disappeared from "onezone" Onezone service

