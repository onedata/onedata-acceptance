Feature: Basic operations on groups

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
                
    And opened browser with user1 logged to "onezone" service


  Scenario Outline: User creates groups
    When using <client1>, user1 creates groups [group1, group2, group3] in "onezone" Onezone service
    Then using <client2>, user1 sees that groups named [group1, group2, group3] has appeared in "onezone" Onezone service

  Examples:
  | client1 | client2   |
  | REST    | web GUI   |
  | web GUI | REST      | 


  Scenario Outline: User renames group
    When using <client2>, user1 creates group "group1" in "onezone" Onezone service
    And using <client1>, user1 sees that group named "group1" has appeared in "onezone" Onezone service
    And using <client1>, user1 renames group "group1" to "new_name1" in "onezone" Onezone service
    Then using <client2>, user1 sees that group named "new_name1" has appeared in "onezone" Onezone service
    And using <client2>, user1 does not see group named "group1" in "onezone" Onezone service

  Examples:
  | client1 | client2   |
  | REST    | web GUI   |
  | web GUI | REST      | 


  Scenario: User removes group
    When using web GUI, user1 creates group "group1" in "onezone" Onezone service
    And using REST, user1 sees that group named "group1" has appeared in "onezone" Onezone service
    And using REST, user1 removes group "group1" in "onezone" Onezone service
    Then using web GUI, user1 does not see group named "group1" in "onezone" Onezone service

    
  Scenario Outline: User leaves group
    When using <client1>, user1 creates group "group1" in "onezone" Onezone service
    And using <client2>, user1 sees that group named "group1" has appeared in "onezone" Onezone service
    And using <client2>, user1 leaves group "group1" in "onezone" Onezone service
    Then using <client1>, user1 does not see group named "group1" in "onezone" Onezone service

  Examples:
  | client1 | client2   |
  | REST    | web GUI   |
  | web GUI | REST      | 


  Scenario Outline: User joins a group to parent group
    When using <client1>, user1 creates groups [child, parent] in "onezone" Onezone service
    And using <client2>, user1 sees that groups named [parent, child] have appeared in "onezone" Onezone service
    And using <client2>, user1 adds group "child" as subgroup to group "parent" in "onezone" Onezone service
    Then using <client1>, user1 sees group "child" as subgroup to group "parent" in "onezone" Onezone service

  Examples:
  | client1 | client2   |
  | REST    | web GUI   |
  | web GUI | REST      | 


  Scenario Outline: User removes group from parent group
    When using <client1>, user1 creates groups [parent, child] in "onezone" Onezone service
    And using <client1>, user1 sees that groups named [parent, child] have appeared in "onezone" Onezone service
    And using <client1>, user1 adds group "child" as subgroup to group "parent" in "onezone" Onezone service
    And using <client2>, user1 sees that group named parent has appeared in "onezone" Onezone service
    And using <client2>, user1 sees group "child" as subgroup to group "parent" in "onezone" Onezone service
    And using <client2>, user1 removes subgroup "child" from group "parent" in "onezone" Onezone service
    Then using <client1>, user1 does not see group "child" as subgroup to group "parent" in "onezone" Onezone service

  Examples:
  | client1 | client2   |
  | REST    | web GUI   |
  | web GUI | REST      | 
