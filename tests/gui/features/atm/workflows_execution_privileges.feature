Feature: Workflows execution privileges

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
            - user1
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
          group2:
            owner: space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: space-owner-user
            users:
                - user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1
            groups:
                - group1
                - group2
    And initial inventories configuration in "onezone" Onezone service:
        inventory1:
            owner: user1

    And users opened [space_owner_browser, browser1] browsers' windows
    And users of [space_owner_browser, browser1] opened [Onezone, Onezone] page
    And users of [space_owner_browser, browser1] logged as [space-owner-user, user1] to [Onezone, Onezone] service


  Scenario: User can see owned group in "Select groups" modal when executing workflow without view space privilege
    # User1 uploads workflow which takes as input groups
    When user of browser1 uploads "initialize-eureka3D-project" workflow from automation-examples repository to "inventory1" inventory
    And user of browser1 opens inventory "inventory1" members subpage

   # Space-owner-user sets privileges for group1
    And user of space_owner_browser clicks "Members" of "space1" space in the sidebar
    And user of space_owner_browser clicks "group1" group in "space1" space members groups list
    And user of space_owner_browser sets following privileges for "group1" group in space members subpage:
          Space management:
            granted: False
          Automation management:
            granted: Partially
            privilege subtypes:
              View workflow executions: True
              Schedule workflow executions: False
              Manage workflow executions: False

    # Space-owner-user sets privileges for user1
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Space management:
            granted: False
          Automation management:
            granted: Partially
            privilege subtypes:
              View workflow executions: True
              Schedule workflow executions: False
              Manage workflow executions: False

    And user of browser1 clicks on Data in the main menu
    And user of browser1 clicks "Automation Workflows" of "space1" space in the sidebar
    And user of browser1 clicks "Run workflow" in the automation tab bar
    And user of browser1 chooses to run 1st revision of "Initialize Eureka3D project" workflow
    And user of browser1 clicks "Add groups..." link in "Managing groups" store

    # User1 sees only owned group in Select groups modal
    Then user of browser1 sees "group1" group in "Select groups" modal
    And user of browser1 does not see "group2" group in "Select groups" modal
