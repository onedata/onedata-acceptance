Feature: Harvesters effective privileges

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user2
            - user3
    # rozwiazanie tymczasowe

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
    And user of browser writes elasticsearch ip: 172.17.0.4
    And user admin has no harvesters
    And user admin has "harvester1" harvester in "onezone" Onezone service
    And users opened [browser_admin, browser_user2] browsers' windows
    And users of [browser_admin, browser_user2] opened [Onezone, Onezone] page
    And user of [browser_admin, browser_user2] logged as [admin, user2] to [Onezone, Onezone] service


  Scenario: User sees that group effective privileges are the sum of its direct parent direct privileges and its direct privileges
    When user of browser_admin clicks on Discovery in the main menu
    And user of browser_admin clicks "harvester1" on the harvesters list in the sidebar
    And user of browser_admin adds "group1" group to "harvester1" harvester using available groups dropdown
    And user of browser_admin adds "group2" group to "harvester1" harvester using available groups dropdown
    And user of browser_admin clicks "group1" group in "harvester1" harvester members groups list
    And user of browser_admin sets following privileges for "group1" group in harvester members subpage:
          Harvester management:
            granted: False
          User management:
            granted: False
          Group management:
            granted: True
          Space management:
            granted: False
    And user of browser_admin clicks "group2" group in "harvester1" harvester members groups list
    And user of browser_admin sets following privileges for "group2" group in harvester members subpage:
          Harvester management:
            granted: True
          User management:
            granted: False
          Group management:
            granted: False
          Space management:
            granted: False
    And user of browser_admin clicks show view expand button in harvester members subpage header
    And user of browser_admin clicks effective view mode in harvester members subpage
    And user of browser_admin clicks "group1" group in "harvester1" harvester members groups list
    Then user of browser_admin sees following privileges of "group1" group in harvester members subpage:
          Harvester management:
            granted: True
          User management:
            granted: False
          Group management:
            granted: True
          Space management:
            granted: False


  Scenario: User sees that user effective privileges are the sum of its direct parent direct privileges and its direct privileges
    When user of browser_admin sends invitation token from "harvester1" harvester to user of browser_user2
    And user of browser_user2 joins to harvester in Onezone page

    And user of browser_admin clicks on Discovery in the main menu
    And user of browser_admin clicks "harvester1" on the harvesters list in the sidebar
    And user of browser_admin adds "group2" group to "harvester1" harvester using available groups dropdown
    And user of browser_admin clicks "group2" group in "harvester1" harvester members groups list
    And user of browser_admin sets following privileges for "group2" group in harvester members subpage:
          Harvester management:
            granted: True
          User management:
            granted: False
          Group management:
            granted: True
          Space management:
            granted: False
    And user of browser_admin clicks "user2" user in "harvester1" harvester members users list
    And user of browser_admin sets following privileges for "user2" user in harvester members subpage:
          Harvester management:
            granted: False
          User management:
            granted: False
          Group management:
            granted: False
          Space management:
            granted: True
    And user of browser_admin clicks show view expand button in harvester members subpage header
    And user of browser_admin clicks effective view mode in harvester members subpage
    And user of browser_admin clicks "user2" user in "harvester1" harvester members users list
    And user of browser_admin sees following privileges of "user2" user in harvester members subpage:
          Harvester management:
            granted: True
          User management:
            granted: False
          Group management:
            granted: True
          Space management:
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
    And user of browser_admin clicks on Discovery in the main menu
    And user of browser_admin clicks "harvester1" on the harvesters list in the sidebar
    And user of browser_admin adds "group2" group to "harvester1" harvester using available groups dropdown
    And user of browser_admin adds "group3" group to "harvester1" harvester using available groups dropdown
    And user of browser_admin clicks "group2" group in "harvester1" harvester members groups list
    And user of browser_admin sets following privileges for "group2" group in harvester members subpage:
          Harvester management:
            granted: False
          User management:
            granted: False
          Group management:
            granted: True
          Space management:
            granted: True
    And user of browser_admin clicks "group3" group in "harvester1" harvester members groups list
    And user of browser_admin sets following privileges for "group3" group in harvester members subpage:
          Harvester management:
            granted: True
          User management:
            granted: True
          Group management:
            granted: False
          Space management:
            granted: False
    And user of browser_admin clicks show view expand button in harvester members subpage header
    And user of browser_admin clicks effective view mode in harvester members subpage
    And user of browser_admin clicks "group4" group in "harvester1" harvester members groups list
    Then user of browser_admin sees following privileges of "group4" group in harvester members subpage:
          Harvester management:
            granted: True
          User management:
            granted: True
          Group management:
            granted: True
          Space management:
            granted: True


  Scenario: User sees that user effective privileges are the sum of its direct parents direct privileges
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
    And user of browser_admin clicks on Discovery in the main menu
    And user of browser_admin clicks "harvester1" on the harvesters list in the sidebar
    And user of browser_admin adds "group2" group to "harvester1" harvester using available groups dropdown
    And user of browser_admin adds "group3" group to "harvester1" harvester using available groups dropdown
    And user of browser_admin clicks "group2" group in "harvester1" harvester members groups list
    And user of browser_admin sets following privileges for "group2" group in harvester members subpage:
          Harvester management:
            granted: True
          User management:
            granted: False
          Group management:
            granted: False
          Space management:
            granted: True
    And user of browser_admin clicks "group3" group in "harvester1" harvester members groups list
    And user of browser_admin sets following privileges for "group3" group in harvester members subpage:
          Harvester management:
            granted: True
          User management:
            granted: True
          Group management:
            granted: False
          Space management:
            granted: False
    And user of browser_admin clicks show view expand button in harvester members subpage header
    And user of browser_admin clicks effective view mode in harvester members subpage
    And user of browser_admin clicks "user3" user in "harvester1" harvester members users list
    Then user of browser_admin sees following privileges of "user3" user in harvester members subpage:
          Harvester management:
            granted: True
          User management:
            granted: True
          Group management:
            granted: False
          Space management:
            granted: True
