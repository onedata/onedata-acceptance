Feature: Spaces effective privileges

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
            - user3
    And initial groups configuration in "onezone" Onezone service:
          child_group1:
            owner: user1
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
                - child_group1
                - child_group2
          child_group2:
              owner: user1

    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: user1
            users:
                - user2:
                    privileges:
                      - space_add_harvester
                      - space_remove_harvester
            groups:
                - child_group1:
                    privileges:
                      - space_add_harvester
                      - space_remove_harvester
                      - space_remove_group
                - parent_group1:
                    privileges:
                      - space_view_qos
                      - space_manage_qos
                      - space_add_group
                - parent_group2:
                    privileges:
                      - space_add_support
                      - space_remove_support


    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User sees that group effective privileges are the sum of its direct parent direct privileges and its direct privileges
    When user of browser clicks on Data in the main menu
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Members of "space1" space in the sidebar
    And user of browser clicks "child_group1" group in "space1" space members groups list
    And user of browser sees following privileges of "child_group1" group in space members subpage:
          QoS management:
            granted: False
          Group management:
            granted: Partially
            privilege subtypes:
              Add group: False
              Remove group: True
          Harvester management:
            granted: True
    And user of browser clicks "parent_group1" group in "space1" space members groups list
    And user of browser sees following privileges of "parent_group1" group in space members subpage:
          QoS management:
            granted: True
          Group management:
            granted: Partially
            privilege subtypes:
              Add group: True
              Remove group: False
          Harvester management:
            granted: False
    And user of browser clicks show view expand button in space members subpage header
    And user of browser clicks effective view mode in space members subpage
    And user of browser clicks "child_group1" group in "space1" space members groups list
    Then user of browser sees following privileges of "child_group1" group in space members subpage:
          QoS management:
            granted: True
          Group management:
            granted: True
          Harvester management:
            granted: True


  Scenario: User sees that user effective privileges are the sum of its direct parent direct privileges and its direct privileges
    When user of browser clicks on Data in the main menu
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Members of "space1" space in the sidebar
    And user of browser clicks "parent_group1" group in "space1" space members groups list
    And user of browser sees following privileges of "parent_group1" group in space members subpage:
          QoS management:
            granted: True
          Group management:
            granted: Partially
            privilege subtypes:
              Add group: True
              Remove group: False
          Harvester management:
            granted: False
    And user of browser clicks "user2" user in "space1" space members users list
    And user of browser sees following privileges of "user2" user in space members subpage:
          QoS management:
            granted: False
          Group management:
            granted: False
          Harvester management:
            granted: True
    And user of browser clicks show view expand button in space members subpage header
    And user of browser clicks effective view mode in space members subpage
    And user of browser clicks "user2" user in "space1" space members users list
    Then user of browser sees following privileges of "user2" user in space members subpage:
          QoS management:
            granted: True
          Group management:
            granted: Partially
            privilege subtypes:
              Add group: True
              Remove group: False
          Harvester management:
            granted: True


  Scenario: User sees that group effective privileges are the sum of its direct parents direct privileges
    When user of browser clicks on Data in the main menu
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Members of "space1" space in the sidebar
    And user of browser clicks "parent_group1" group in "space1" space members groups list
    And user of browser sees following privileges of "parent_group1" group in space members subpage:
          QoS management:
            granted: True
          Group management:
            granted: Partially
            privilege subtypes:
              Add group: True
              Remove group: False
          Harvester management:
            granted: False
    And user of browser clicks "parent_group2" group in "space1" space members groups list
    And user of browser sees following privileges of "parent_group2" group in space members subpage:
          QoS management:
            granted: False
          Group management:
            granted: False
          Support management:
            granted: True
    And user of browser clicks show view expand button in space members subpage header
    And user of browser clicks effective view mode in space members subpage
    And user of browser clicks "child_group2" group in "space1" space members groups list
    Then user of browser sees following privileges of "child_group2" group in space members subpage:
          QoS management:
            granted: True
          Group management:
            granted: Partially
            privilege subtypes:
              Add group: True
              Remove group: False
          Support management:
            granted: True


  Scenario: User sees that user effective privileges are the sum of its direct parents direct privileges
    When user of browser clicks on Data in the main menu
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Members of "space1" space in the sidebar
    And user of browser clicks "parent_group1" group in "space1" space members groups list
    And user of browser sees following privileges of "parent_group1" group in space members subpage:
          QoS management:
            granted: True
          Group management:
            granted: Partially
            privilege subtypes:
              Add group: True
              Remove group: False
          Harvester management:
            granted: False
    And user of browser clicks "parent_group2" group in "space1" space members groups list
    And user of browser sees following privileges of "parent_group2" group in space members subpage:
          QoS management:
            granted: False
          Group management:
            granted: False
          Support management:
            granted: True
    And user of browser clicks show view expand button in space members subpage header
    And user of browser clicks effective view mode in space members subpage
    And user of browser clicks "user3" user in "space1" space members users list
    Then user of browser sees following privileges of "user3" user in space members subpage:
          QoS management:
            granted: True
          Group management:
            granted: Partially
            privilege subtypes:
              Add group: True
              Remove group: False
          Support management:
            granted: True
