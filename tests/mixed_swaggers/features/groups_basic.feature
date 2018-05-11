Feature: Basic operations on groups

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
    And opened p1 Oneprovider view in web GUI by user1


  Scenario Outline: User creates groups
    When using <client1>, user1 creates groups [group1, group2, group3] in "z1" Onezone service
    Then using <client2>, user1 sees that groups named [group1, group2, group3] has appeared in "z1" Onezone service

  Examples:
  | client1 | client2   |
  | REST    | web GUI   |
  | web GUI | REST      | 


  Scenario Outline: User renames group
    When using <client2>, user1 creates group "group1" in "z1" Onezone service
    And using <client1>, user1 sees that group named "group1" has appeared in "z1" Onezone service
    And using <client1>, user1 renames group "group1" to "new_name1" in "z1" Onezone service
    Then using <client2>, user1 sees that group named "new_name1" has appeared in "z1" Onezone service
    And using <client2>, user1 does not see group named "group1" in "z1" Onezone service

  Examples:
  | client1 | client2   |
  | REST    | web GUI   |
  | web GUI | REST      | 


  Scenario: User removes group
    When using web GUI, user1 creates group "group1" in "z1" Onezone service
    And using REST, user1 sees that group named "group1" has appeared in "z1" Onezone service
    And using REST, user1 removes group "group1" in "z1" Onezone service
    Then using web GUI, user1 does not see group named "group1" in "z1" Onezone service

    
  Scenario Outline: User leaves group
    When using <client1>, user1 creates group "group1" in "z1" Onezone service
    And using <client2>, user1 sees that group named "group1" has appeared in "z1" Onezone service
    And using <client2>, user1 leaves group "group1" in "z1" Onezone service
    Then using <client1>, user1 does not see group named "group1" in "z1" Onezone service

  Examples:
  | client1 | client2   |
  | REST    | web GUI   |
  | web GUI | REST      | 


  Scenario Outline: User joins a group to parent group
    When using <client1>, user1 creates groups [child, parent] in "z1" Onezone service
    And using <client2>, user1 sees that groups named [parent, child] have appeared in "z1" Onezone service
    And using <client2>, user1 adds group "child" as subgroup to group "parent" in "z1" Onezone service
    Then using <client1>, user1 sees group "child" as subgroup to group "parent" in "z1" Onezone service

  Examples:
  | client1 | client2   |
  | REST    | web GUI   |
  | web GUI | REST      | 


  Scenario Outline: User removes group from parent group
    When using <client1>, user1 creates groups [parent, child] in "z1" Onezone service
    And using <client1>, user1 sees that groups named [parent, child] have appeared in "z1" Onezone service
    And using <client1>, user1 adds group "child" as subgroup to group "parent" in "z1" Onezone service
    And using <client2>, user1 sees that group named parent has appeared in "z1" Onezone service
    And using <client2>, user1 sees group "child" as subgroup to group "parent" in "z1" Onezone service
    And using <client2>, user1 removes subgroup "child" from group "parent" in "z1" Onezone service
    Then using <client1>, user1 does not see group "child" as subgroup to group "parent" in "z1" Onezone service

  Examples:
  | client1 | client2   |
  | REST    | web GUI   |
  | web GUI | REST      | 
