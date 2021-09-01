Feature: Groups effective privileges

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
            - user3
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
            users:
              - user2:
                  privileges:
                      - group_add_child
                      - group_remove_child
                      - group_add_parent
                      - group_leave_parent
            groups:
              - group2:
                  privileges:
                      - group_add_cluster
                      - group_leave_cluster
                      - group_add_user
                      - group_remove_user
              - group3:
                  privileges:
                      - group_add_harvester
                      - group_remove_harvester
              - group4:
                  privileges:
                      - group_add_child
                      - group_remove_child
                      - group_add_parent
                      - group_leave_parent
                      - group_add_harvester
                      - group_remove_harvester
          group2:
            owner: user1
            users:
              - user2
              - user3
            groups:
              - group3
              - group5
          group4:
            owner: user1
            users:
              - user3
            groups:
              - group5
          group3:
            owner: user1
          group5:
            owner: user1

    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User sees that group effective privileges are the sum of its direct parent direct privileges and its direct privileges
    When user of browser clicks on Groups in the main menu
    And user of browser opens group "group1" members subpage
    And user of browser clicks "group2" group in "group1" group members groups list
    And user of browser sees following privileges of "group2" group in group members subpage:
          User management:
            granted: True
          Cluster management:
            granted: True
          Harvester management:
            granted: False
    And user of browser clicks "group3" group in "group1" group members groups list
    And user of browser sees following privileges of "group3" group in group members subpage:
          User management:
            granted: False
          Cluster management:
            granted: False
          Harvester management:
            granted: True
    And user of browser clicks show view expand button in group members subpage header
    And user of browser clicks effective view mode in group members subpage
    And user of browser clicks "group3" group in "group1" group members groups list
    Then user of browser sees following privileges of "group3" group in group members subpage:
          User management:
            granted: True
          Cluster management:
            granted: True
          Harvester management:
            granted: True


  Scenario: User sees that user effective privileges are the sum of its direct parent direct privileges and its direct privileges
    When user of browser clicks on Groups in the main menu
    And user of browser opens group "group1" members subpage
    And user of browser clicks "group2" group in "group1" group members groups list
    And user of browser sees following privileges of "group2" group in group members subpage:
          Group hierarchy management:
            granted: False
          User management:
            granted: True
          Cluster management:
            granted: True
    And user of browser clicks "user2" user in "group1" group members users list
    And user of browser sees following privileges of "user2" user in group members subpage:
          Group hierarchy management:
            granted: True
          User management:
            granted: False
          Cluster management:
            granted: False
    And user of browser clicks show view expand button in group members subpage header
    And user of browser clicks effective view mode in group members subpage
    And user of browser clicks "user2" user in "group1" group members users list
    Then user of browser sees following privileges of "user2" user in group members subpage:
          Group hierarchy management:
            granted: True
          User management:
            granted: True
          Cluster management:
            granted: True


  Scenario: User sees that group effective privileges are the sum of its direct parents direct privileges
    When user of browser clicks on Groups in the main menu
    And user of browser opens group "group2" members subpage
    And user of browser clicks "group5" group in "group2" group members groups list
    And user of browser sets all privileges true for "group5" group in group members subpage
    And user of browser opens group "group4" members subpage
    And user of browser clicks "group5" group in "group4" group members groups list
    And user of browser sets all privileges true for "group5" group in group members subpage

    And user of browser opens group "group1" members subpage
    And user of browser clicks "group2" group in "group1" group members groups list
    And user of browser sees following privileges of "group2" group in group members subpage:
          Group hierarchy management:
            granted: False
          User management:
            granted: True
          Cluster management:
            granted: True
          Harvester management:
            granted: False
    And user of browser clicks "group4" group in "group1" group members groups list
    And user of browser sees following privileges of "group4" group in group members subpage:
          Group hierarchy management:
            granted: True
          User management:
            granted: False
          Cluster management:
            granted: False
          Harvester management:
            granted: True
    And user of browser clicks show view expand button in group members subpage header
    And user of browser clicks effective view mode in group members subpage
    And user of browser clicks "group5" group in "group1" group members groups list
    Then user of browser sees following privileges of "group5" group in group members subpage:
          Group hierarchy management:
            granted: True
          User management:
            granted: True
          Cluster management:
            granted: True
          Harvester management:
            granted: True


  Scenario: User sees that user effective privileges are the sum of its direct parents direct privileges
    When user of browser clicks on Groups in the main menu
    And user of browser opens group "group2" members subpage
    And user of browser clicks "user3" user in "group2" group members users list
    And user of browser sets all privileges true for "user3" user in group members subpage
    And user of browser opens group "group4" members subpage
    And user of browser clicks "user3" user in "group4" group members users list
    And user of browser sets all privileges true for "user3" user in group members subpage

    And user of browser opens group "group1" members subpage
    And user of browser clicks "group2" group in "group1" group members groups list
    And user of browser sees following privileges of "group2" group in group members subpage:
          Group hierarchy management:
            granted: False
          User management:
            granted: True
          Cluster management:
            granted: True
          Harvester management:
            granted: False
    And user of browser clicks "group4" group in "group1" group members groups list
    And user of browser sees following privileges of "group4" group in group members subpage:
          Group hierarchy management:
            granted: True
          User management:
            granted: False
          Cluster management:
            granted: False
          Harvester management:
            granted: True
    And user of browser clicks show view expand button in group members subpage header
    And user of browser clicks effective view mode in group members subpage
    And user of browser clicks "user3" user in "group1" group members users list
    Then user of browser sees following privileges of "user3" user in group members subpage:
          Group hierarchy management:
            granted: True
          User management:
            granted: True
          Cluster management:
            granted: True
          Harvester management:
            granted: True
