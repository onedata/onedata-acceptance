Feature: Harvesters effective privileges

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user2
            - user3
    And there is no groups in Onezone page used by admin before definition in next steps
    And initial groups configuration in "onezone" Onezone service:
          child_group_1:
            owner: admin
          parent_group_1:
            owner: admin
            users:
              - user2
              - user3
            groups:
                - child_group_1
                - child_group_2
          parent_group_2:
              owner: admin
              users:
                - user3
              groups:
                - child_group_1
                - child_group_2
          child_group_2:
              owner: admin
    And user admin has no harvesters other than defined in next steps
    And user admin has "harvester1" harvester in "onezone" Onezone service
    And users opened [browser_admin, browser_user2] browsers' windows
    And users of [browser_admin, browser_user2] opened [Onezone, Onezone] page
    And user of [browser_admin, browser_user2] logged as [admin, user2] to [Onezone, Onezone] service


  Scenario: User sees that group effective privileges are the sum of its direct parent direct privileges and its direct privileges
    When user of browser_admin clicks on Discovery in the main menu
    And user of browser_admin clicks "harvester1" on the harvesters list in the sidebar
    And user of browser_admin adds "child_group_1" group to "harvester1" harvester using available groups dropdown
    And user of browser_admin adds "parent_group_1" group to "harvester1" harvester using available groups dropdown
    And user of browser_admin clicks "child_group_1" group in "harvester1" harvester members groups list
    And user of browser_admin sets following privileges for "child_group_1" group in harvester members subpage:
          Harvester management:
            granted: False
          User management:
            granted: False
          Group management:
            granted: True
          Space management:
            granted: False
    And user of browser_admin clicks "parent_group_1" group in "harvester1" harvester members groups list
    And user of browser_admin sets following privileges for "parent_group_1" group in harvester members subpage:
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
    And user of browser_admin clicks "child_group_1" group in "harvester1" harvester members groups list
    Then user of browser_admin sees following privileges of "child_group_1" group in harvester members subpage:
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
    And user of browser_admin adds "parent_group_1" group to "harvester1" harvester using available groups dropdown
    And user of browser_admin clicks "parent_group_1" group in "harvester1" harvester members groups list
    And user of browser_admin sets following privileges for "parent_group_1" group in harvester members subpage:
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
    Then user of browser_admin sees following privileges of "user2" user in harvester members subpage:
          Harvester management:
            granted: True
          User management:
            granted: False
          Group management:
            granted: True
          Space management:
            granted: True


  Scenario: User sees that group effective privileges are the sum of its direct parents direct privileges
    When user of browser_admin clicks on Discovery in the main menu
    And user of browser_admin clicks "harvester1" on the harvesters list in the sidebar
    And user of browser_admin adds "parent_group_1" group to "harvester1" harvester using available groups dropdown
    And user of browser_admin adds "parent_group_2" group to "harvester1" harvester using available groups dropdown
    And user of browser_admin clicks "parent_group_1" group in "harvester1" harvester members groups list
    And user of browser_admin sets following privileges for "parent_group_1" group in harvester members subpage:
          Harvester management:
            granted: False
          User management:
            granted: False
          Group management:
            granted: True
          Space management:
            granted: True
    And user of browser_admin clicks "parent_group_2" group in "harvester1" harvester members groups list
    And user of browser_admin sets following privileges for "parent_group_2" group in harvester members subpage:
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
    And user of browser_admin clicks "child_group_2" group in "harvester1" harvester members groups list
    Then user of browser_admin sees following privileges of "child_group_2" group in harvester members subpage:
          Harvester management:
            granted: True
          User management:
            granted: True
          Group management:
            granted: True
          Space management:
            granted: True


  Scenario: User sees that user effective privileges are the sum of its direct parents direct privileges
    When user of browser_admin clicks on Discovery in the main menu
    And user of browser_admin clicks "harvester1" on the harvesters list in the sidebar
    And user of browser_admin adds "parent_group_1" group to "harvester1" harvester using available groups dropdown
    And user of browser_admin adds "parent_group_2" group to "harvester1" harvester using available groups dropdown
    And user of browser_admin clicks "parent_group_1" group in "harvester1" harvester members groups list
    And user of browser_admin sets following privileges for "parent_group_1" group in harvester members subpage:
          Harvester management:
            granted: True
          User management:
            granted: False
          Group management:
            granted: False
          Space management:
            granted: True
    And user of browser_admin clicks "parent_group_2" group in "harvester1" harvester members groups list
    And user of browser_admin sets following privileges for "parent_group_2" group in harvester members subpage:
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
