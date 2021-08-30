Feature: Inventories effective privileges

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
            - user3
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
          group2:
            owner: user1
            users:
              - user2
              - user3
            groups:
                - group1
                - group4
          group3:
              owner: user1
              users:
                - user3
              groups:
                - group1
                - group4
          group4:
              owner: user1

    And initial inventories configuration in "onezone" Onezone service:
          inventory1:
            owner: user1
            users:
                - user2:
                    privileges:
                        - atm_inventory_manage_lambdas
                        - atm_inventory_manage_workflow_schemas
            groups:
                - group1:
                    privileges:
                        - atm_inventory_manage_lambdas
                        - atm_inventory_manage_workflow_schemas
                        - atm_inventory_add_user
                        - atm_inventory_remove_user
                - group2:
                    privileges:
                        - atm_inventory_delete
                        - atm_inventory_set_privileges
                        - atm_inventory_update
                        - atm_inventory_view
                        - atm_inventory_view_privileges
                - group3:
                    privileges:
                        - atm_inventory_add_group
                        - atm_inventory_remove_group


    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User sees that group effective privileges are the sum of its direct parent direct privileges and its direct privileges
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" members subpage
    And user of browser clicks "group1" group in "inventory1" automation members groups list
    And user of browser sees following privileges of "group1" group in automation members subpage:
          Inventory management:
            granted: False
          Schema management:
            granted: True
          User management:
            granted: True
    And user of browser clicks "group2" group in "inventory1" automation members groups list
    And user of browser sees following privileges of "group2" group in automation members subpage:
          Inventory management:
            granted: True
          Schema management:
            granted: False
          User management:
            granted: False
    And user of browser clicks show view expand button in automation members subpage header
    And user of browser clicks effective view mode in automation members subpage
    Then user of browser sees following privileges of "group1" group in automation members subpage:
          Inventory management:
            granted: True
          Schema management:
            granted: True
          User management:
            granted: True


  Scenario: User sees that user effective privileges are the sum of its direct parent direct privileges and its direct privileges
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" members subpage
    And user of browser clicks "group2" group in "inventory1" automation members groups list
    And user of browser sees following privileges of "group2" group in automation members subpage:
          Inventory management:
            granted: True
          Schema management:
            granted: False
    And user of browser clicks "user2" user in "inventory1" automation members users list
    And user of browser sees following privileges of "user2" user in automation members subpage:
          Inventory management:
            granted: False
          Schema management:
            granted: True
    And user of browser clicks show view expand button in automation members subpage header
    And user of browser clicks effective view mode in automation members subpage
    Then user of browser sees following privileges of "user2" user in automation members subpage:
          Inventory management:
            granted: True
          Schema management:
            granted: True


    Scenario: User sees that group effective privileges are the sum of its direct parents direct privileges
      When user of browser clicks on Groups in the main menu
      And user of browser opens group "group2" members subpage
      And user of browser clicks "group4" group in "group2" group members groups list
      And user of browser sets following privileges for "group4" group in group members subpage:
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
      And user of browser opens group "group3" members subpage
      And user of browser clicks "group4" group in "group3" group members groups list
      And user of browser sets following privileges for "group4" group in group members subpage:
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
    And user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" members subpage
    And user of browser clicks "group2" group in "inventory1" automation members groups list
    And user of browser sees following privileges of "group2" group in automation members subpage:
          Inventory management:
            granted: True
          Group management:
            granted: False
    And user of browser clicks "group3" group in "inventory1" automation members groups list
    And user of browser sees following privileges of "group3" group in automation members subpage:
          Inventory management:
            granted: False
          Group management:
            granted: True
    And user of browser clicks show view expand button in automation members subpage header
    And user of browser clicks effective view mode in automation members subpage
    And user of browser clicks "group4" group in "inventory1" automation members groups list
    Then user of browser sees following privileges of "group4" group in automation members subpage:
          Inventory management:
            granted: True
          Group management:
            granted: True


  Scenario: User sees that user effective privileges are the sum of its direct parents direct privileges
    When user of browser clicks on Groups in the main menu
    And user of browser opens group "group2" members subpage
    And user of browser clicks "user3" user in "group2" group members users list
    And user of browser sets following privileges for "user3" user in group members subpage:
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
    And user of browser opens group "group3" members subpage
    And user of browser clicks "user3" user in "group3" group members users list
    And user of browser sets following privileges for "user3" user in group members subpage:
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
    And user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" members subpage
    And user of browser clicks "group2" group in "inventory1" automation members groups list
    And user of browser sees following privileges of "group2" group in automation members subpage:
          Inventory management:
            granted: True
          Group management:
            granted: False
    And user of browser clicks "group3" group in "inventory1" automation members groups list
    And user of browser sees following privileges of "group3" group in automation members subpage:
          Inventory management:
            granted: False
          Group management:
            granted: True
    And user of browser refreshes site
    And user of browser clicks show view expand button in automation members subpage header
    And user of browser clicks effective view mode in automation members subpage
    And user of browser clicks "user3" user in "inventory1" automation members users list
    Then user of browser sees following privileges of "user3" user in automation members subpage:
          Inventory management:
            granted: True
          Group management:
            granted: True
