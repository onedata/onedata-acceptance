Feature: Groups effective privileges

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
            - user3
    And initial groups configuration in "onezone" Onezone service:
          grandparent_group:
            owner: user1
            users:
              - user2:
                  privileges:
                      - group_add_child
                      - group_remove_child
                      - group_add_parent
                      - group_leave_parent
            groups:
              - parent_group1:
                  privileges:
                      - group_add_cluster
                      - group_leave_cluster
                      - group_add_user
                      - group_remove_user
              - child_group1:
                  privileges:
                      - group_add_harvester
                      - group_remove_harvester
              - parent_group2:
                  privileges:
                      - group_add_child
                      - group_remove_child
                      - group_add_parent
                      - group_leave_parent
                      - group_add_harvester
                      - group_remove_harvester
          parent_group1:
            owner: user1
            users:
              - user2
              - user3
            groups:
              - child_group1
              - child_group2
          parent_group2:
            owner: user1
            users:
              - user3
            groups:
              - child_group2
          child_group1:
            owner: user1
          child_group2:
            owner: user1

    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User sees that group effective privileges are the sum of its direct parent direct privileges and its direct privileges
    When user of browser sees following privileges for group "parent_group1" in group "grandparent_group" members subpage:
          User management:
            granted: True
          Cluster management:
            granted: True
          Harvester management:
            granted: False
    And user of browser sees following privileges for group "child_group1" in group "grandparent_group" members subpage:
          User management:
            granted: False
          Cluster management:
            granted: False
          Harvester management:
            granted: True
    Then user of browser sees following effective privileges for group "child_group1" in group "grandparent_group" members subpage:
          User management:
            granted: True
          Cluster management:
            granted: True
          Harvester management:
            granted: True


  Scenario: User sees that user effective privileges are the sum of its direct parent direct privileges and its direct privileges
    When user of browser sees following privileges for group "parent_group1" in group "grandparent_group" members subpage:
          Group hierarchy management:
            granted: False
          User management:
            granted: True
          Cluster management:
            granted: True
    And user of browser sees following privileges for user "user2" in group "grandparent_group" members subpage:
          Group hierarchy management:
            granted: True
          User management:
            granted: False
          Cluster management:
            granted: False
    Then user of browser sees following effective privileges for user "user2" in group "grandparent_group" members subpage:
          Group hierarchy management:
            granted: True
          User management:
            granted: True
          Cluster management:
            granted: True


  Scenario: User sees that group effective privileges are the sum of its direct parents direct privileges
    When user of browser sees following privileges for group "parent_group1" in group "grandparent_group" members subpage:
          Group hierarchy management:
            granted: False
          User management:
            granted: True
          Cluster management:
            granted: True
          Harvester management:
            granted: False
    And user of browser sees following privileges for group "parent_group2" in group "grandparent_group" members subpage:
          Group hierarchy management:
            granted: True
          User management:
            granted: False
          Cluster management:
            granted: False
          Harvester management:
            granted: True
    Then user of browser sees following effective privileges for group "child_group2" in group "grandparent_group" members subpage:
          Group hierarchy management:
            granted: True
          User management:
            granted: True
          Cluster management:
            granted: True
          Harvester management:
            granted: True


  Scenario: User sees that user effective privileges are the sum of its direct parents direct privileges
    When user of browser sees following privileges for group "parent_group1" in group "grandparent_group" members subpage:
          Group hierarchy management:
            granted: False
          User management:
            granted: True
          Cluster management:
            granted: True
          Harvester management:
            granted: False
    And user of browser sees following privileges for group "parent_group2" in group "grandparent_group" members subpage:
          Group hierarchy management:
            granted: True
          User management:
            granted: False
          Cluster management:
            granted: False
          Harvester management:
            granted: True
    Then user of browser sees following effective privileges for user "user3" in group "grandparent_group" members subpage:
          Group hierarchy management:
            granted: True
          User management:
            granted: True
          Cluster management:
            granted: True
          Harvester management:
            granted: True
