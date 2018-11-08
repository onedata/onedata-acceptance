Feature: Multiuser operations on groups using REST API and web GUI

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2   
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
            users:
                - user2
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000

    And opened browser with [user1, user2] logged to [onezone onezone, onezone onezone] service
    And opened oneprovider-1 Oneprovider view in web GUI by [user1, user2]


  Scenario Outline: User joins group
    When using <client1>, user1 creates group "group1" in "onezone" Onezone service
    And using <client2>, user1 sees that group named "group1" has appeared in "onezone" Onezone service
    And using <client2>, user1 invites user2 to group "group1" in "onezone" Onezone service
    And using <client2>, user2 joins group he was invited to in "onezone" Onezone service
    Then using <client1>, user2 sees that group named "group1" has appeared in "onezone" Onezone service

  Examples:
  | client1 | client2   |
  | REST    | web GUI   |
  | web GUI | REST      | 


  Scenario Outline: Group is not renamed because of lack in privileges
    When using <client1>, user1 creates group "group1" in "onezone" Onezone service
    And using <client2>, user1 sees that group named "group1" has appeared in "onezone" Onezone service
    And using <client2>, user1 invites user2 to group "group1" in "onezone" Onezone service
    And using <client1>, user2 joins group he was invited to in "onezone" Onezone service
    And using <client2>, user2 sees that group named "group1" has appeared in "onezone" Onezone service
    And using <client2>, user2 fails to rename group "group1" to "new_name" in "onezone" Onezone service
    Then using <client1>, user2 sees group named "group1" in "onezone" Onezone service
    And using <client1>, user2 does not see group named "new_name" in "onezone" Onezone service

  Examples:
  | client1 | client2   |
  | REST    | web GUI   |
  | web GUI | REST      | 


  Scenario: Group is not removed because of lack in privileges
    When using web GUI, user1 creates group "group1" in "onezone" Onezone service
    And using REST, user1 sees that group named "group1" has appeared in "onezone" Onezone service
    And using REST, user1 invites user2 to group "group1" in "onezone" Onezone service
    And using web GUI, user2 joins group he was invited to in "onezone" Onezone service
    And using REST, user2 sees that group named "group1" has appeared in "onezone" Onezone service
    And using REST, user2 fails to remove group "group1" in "onezone" Onezone service
    Then using web GUI, user2 sees group named "group1" in "onezone" Onezone service


  Scenario Outline: Group is not joined to group because of lack in privileges
    When using <client1>, user1 creates group [child] in "onezone" Onezone service
    And using <client2>, user1 sees that group named [child] has appeared in "onezone" Onezone service
    And using <client2>, user1 invites user2 to group "child" in "onezone" Onezone service
    And using <client1>, user2 joins group he was invited to in "onezone" Onezone service
    And using <client1>, user2 creates group [parent] in "onezone" Onezone service
    And using <client2>, user2 sees that groups named [child, parent] has appeared in "onezone" Onezone service
    And using <client2>, user2 fails to join group "child" as subgroup to group "parent" in "onezone" Onezone service
    Then using <client1>, user2 does not see group "child" as subgroup to group "parent" in "onezone" Onezone service

  Examples:
  | client1 | client2   |
  | REST    | web GUI   |
  | web GUI | REST      | 

