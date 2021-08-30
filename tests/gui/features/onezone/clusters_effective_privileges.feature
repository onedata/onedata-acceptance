Feature: Clusters effective privileges

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user2
            - user3
    And user admin has no groups
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: admin
          group2:
            owner: admin
            users:
              - user2
              - user3
            groups:
                - group1
                - group4
          group3:
              owner: admin
              users:
                - user3
              groups:
                - group1
                - group4
          group4:
              owner: admin

    And users opened [browser_admin, browser_user2] browsers' windows
    And users of [browser_admin, browser_user2] opened [Onezone, Onezone] page
    And user of [browser_admin, browser_user2] logged as [admin, user2] to [Onezone, Onezone] service


  Scenario: User sees that group effective privileges are the sum of its direct parent direct privileges and its direct privileges
    When user of browser_admin adds "group1" group to "oneprovider-1" cluster
    And user of browser_admin adds "group2" group to "oneprovider-1" cluster
    And user of browser_admin clicks "group1" group in "oneprovider-1" cluster members groups list
    And user of browser_admin sets following privileges for "group1" group in cluster members subpage:
          Cluster management:
            granted: True
          Group management:
            granted: False
    And user of browser_admin clicks "group2" group in "oneprovider-1" cluster members groups list
    And user of browser_admin sets following privileges for "group2" group in cluster members subpage:
          Cluster management:
            granted: False
          Group management:
            granted: True
    And user of browser_admin clicks show view expand button in cluster members subpage header
    And user of browser_admin clicks effective view mode in cluster members subpage
    And user of browser_admin clicks "group1" group in "oneprovider-1" cluster members groups list
    Then user of browser_admin sees following privileges of "group1" group in cluster members subpage:
          Cluster management:
            granted: True
          Group management:
            granted: True


  Scenario: User sees that user effective privileges are the sum of its direct parent direct privileges and its direct privileges
    When user of browser_admin invites user of browser_user2 to "oneprovider-1" cluster
    And user of browser_user2 joins to cluster

    And user of browser_admin adds "group2" group to "oneprovider-1" cluster
    And user of browser_admin clicks "group2" group in "oneprovider-1" cluster members groups list
    And user of browser_admin sets following privileges for "group2" group in cluster members subpage:
          Cluster management:
            granted: True
          Group management:
            granted: False

    And user of browser_admin clicks "user2" user in "oneprovider-1" cluster members users list
    And user of browser_admin sets following privileges for "user2" user in cluster members subpage:
          Cluster management:
            granted: False
          User management:
            granted: False
          Group management:
            granted: True
    And user of browser_admin clicks show view expand button in cluster members subpage header
    And user of browser_admin clicks effective view mode in cluster members subpage
    And user of browser_admin clicks "user2" user in "oneprovider-1" cluster members users list
   Then user of browser_admin sees following privileges of "user2" user in cluster members subpage:
          Cluster management:
            granted: True
          User management:
            granted: False
          Group management:
            granted: True


  Scenario: User sees that group effective privileges are the sum of its direct parents direct privileges
    When user of browser_admin clicks on Groups in the main menu
    And user of browser_admin opens group "group2" members subpage
    And user of browser_admin clicks "group4" group in "group2" group members groups list
    And user of browser_admin sets following privileges for "group4" group in group members subpage:
          Group management:
            granted: True
          Group hierarchy management:
            granted: True
          User management:
            granted: True
          Space management:
            granted: True
          Handle management:
            granted: True
          Cluster management:
            granted: True
          Harvester management:
            granted: True
          Automation inventory management:
            granted: True
    And user of browser_admin opens group "group3" members subpage
    And user of browser_admin clicks "group4" group in "group3" group members groups list
    And user of browser_admin sets following privileges for "group4" group in group members subpage:
          Group management:
            granted: True
          Group hierarchy management:
            granted: True
          User management:
            granted: True
          Space management:
            granted: True
          Handle management:
            granted: True
          Cluster management:
            granted: True
          Harvester management:
            granted: True
          Automation inventory management:
            granted: True
    And user of browser_admin adds "group2" group to "oneprovider-1" cluster
    And user of browser_admin adds "group3" group to "oneprovider-1" cluster
    And user of browser_admin clicks "group2" group in "oneprovider-1" cluster members groups list
    And user of browser_admin sets following privileges for "group2" group in cluster members subpage:
          Cluster management:
            granted: False
          User management:
            granted: True
          Group management:
            granted: False
    And user of browser_admin clicks "group3" group in "oneprovider-1" cluster members groups list
    And user of browser_admin sets following privileges for "group3" group in cluster members subpage:
          Cluster management:
            granted: False
          Group management:
            granted: True
    And user of browser_admin clicks show view expand button in cluster members subpage header
    And user of browser_admin clicks effective view mode in cluster members subpage
    And user of browser_admin clicks "group4" group in "oneprovider-1" cluster members groups list
    Then user of browser_admin sees following privileges of "group4" group in cluster members subpage:
          User management:
            granted: True
          Group management:
            granted: True


  Scenario: User sees that user effective privileges are the sum of its direct parents direct privileges
    When user of browser_admin clicks on Groups in the main menu
    And user of browser_admin opens group "group2" members subpage
    And user of browser_admin clicks "user3" user in "group2" group members users list
    And user of browser_admin sets following privileges for "user3" user in group members subpage:
          Group management:
            granted: True
          Group hierarchy management:
            granted: True
          User management:
            granted: True
          Space management:
            granted: True
          Handle management:
            granted: True
          Cluster management:
            granted: True
          Harvester management:
            granted: True
          Automation inventory management:
            granted: True
    And user of browser_admin opens group "group3" members subpage
    And user of browser_admin clicks "user3" user in "group3" group members users list
    And user of browser_admin sets following privileges for "user3" user in group members subpage:
          Group management:
            granted: True
          Group hierarchy management:
            granted: True
          User management:
            granted: True
          Space management:
            granted: True
          Handle management:
            granted: True
          Cluster management:
            granted: True
          Harvester management:
            granted: True
          Automation inventory management:
            granted: True
    And user of browser_admin adds "group2" group to "oneprovider-1" cluster
    And user of browser_admin adds "group3" group to "oneprovider-1" cluster
    And user of browser_admin clicks "group2" group in "oneprovider-1" cluster members groups list
    And user of browser_admin sets following privileges for "group2" group in cluster members subpage:
          Cluster management:
            granted: False
          User management:
            granted: True
          Group management:
            granted: False
    And user of browser_admin clicks "group3" group in "oneprovider-1" cluster members groups list
    And user of browser_admin sets following privileges for "group3" group in cluster members subpage:
          Cluster management:
            granted: False
          Group management:
            granted: True
    And user of browser_admin clicks show view expand button in cluster members subpage header
    And user of browser_admin clicks effective view mode in cluster members subpage
    And user of browser_admin clicks "user3" user in "oneprovider-1" cluster members users list
    Then user of browser_admin sees following privileges of "user3" user in cluster members subpage:
          Cluster management:
            granted: False
          User management:
            granted: True
          Group management:
            granted: True
