Feature: Basic management of privileges for spaces in Onezone GUI

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
            - space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: space-owner-user
            users:
                - user1
                - user2
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1

    And opened [browser_user1, space_owner_browser] with [user1, space-owner-user] signed in to [Onezone, Onezone] service


  Scenario: User fails to see privileges of another user until he is granted all privileges by becoming an owner
    When user of browser_user1 clicks "Members" of "space1" space in the sidebar
    And user of browser_user1 clicks "space-owner-user" user in "space1" space members users list
    And user of browser_user1 sees Insufficient privileges alert for "space-owner-user" user in space members subpage

    And user of space_owner_browser clicks "Members" of "space1" space in the sidebar
    And user of space_owner_browser clicks "Make an owner" for "user1" user in users list

    And user of browser_user1 refreshes site
    And user of browser_user1 clicks "user1" user in "space1" space members users list
    And user of browser_user1 sees "As a space owner, you are authorized to perform all operations, regardless of the assigned privileges." warning for "user1" user in space members subpage

    And user of browser_user1 clicks "space-owner-user" user in "space1" space members users list
    Then user of browser_user1 sees privileges for "space-owner-user" user in space members subpage


  Scenario: Appropriate tabs are disabled after removing some of user privileges
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks "Members" of "space1" space in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list

    # All tabs are enabled when all privileges are granted
    And user of space_owner_browser sets all privileges true for "user1" user in space members subpage
    Then user of browser_user1 sees that all tabs of "space1" are enabled

    # Some tabs are disabled when view space is not granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          Space management:
            granted: Partially
            privilege subtypes:
              View space: False
    And user of browser_user1 sees that ["Overview", "Files", "Transfers", "Providers", "Automation workflows"] tabs of "space1" are enabled
    And user of browser_user1 sees that ["Shares, Open Data", "Members", "Harvesters, Discovery"] tabs of "space1" are disabled

    # All tabs are enabled when only view space from space management category is granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          Space management:
            granted: Partially
            privilege subtypes:
              View space: True
              Modify space: False
              Remove space: False
              View privileges: False
              Set privileges: False
    And user of browser_user1 sees that all tabs of "space1" are enabled

    # Some tabs are disabled when none from space management category are granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          Space management:
            granted: False
    And user of browser_user1 sees that ["Overview", "Files", "Transfers", "Providers", "Automation workflows"] tabs of "space1" are enabled
    And user of browser_user1 sees that ["Shares, Open Data", "Members", "Harvesters, Discovery"] tabs of "space1" are disabled

    # Only files tab is disabled when only read files is not granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          Data management:
            granted: Partially
            privilege subtypes:
              Read files: False
    And user of browser_user1 sees that ["Overview", "Shares, Open Data", "Transfers", "Providers", "Members", "Harvesters, Discovery", "Automation workflows"] tabs of "space1" are enabled
    And user of browser_user1 sees that Files tab of "space1" is disabled

    # All tabs are enabled when only read files from data management category is granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          Data management:
            granted: Partially
            privilege subtypes:
              Read files: True
              Write files: False
              Register files: False
              Manage shares: False
              View database views: False
              Manage database views: False
              Query database views: False
              View statistics: False
              View changes stream: False
    And user of browser_user1 sees that all tabs of "space1" are enabled

    # Only files tab is disabled when none from data management category are granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          Data management:
            granted: False
    And user of browser_user1 sees that ["Overview", "Shares, Open Data", "Transfers", "Providers", "Members", "Harvesters, Discovery", "Automation workflows"] tabs of "space1" are enabled
    And user of browser_user1 sees that Files tab of "space1" is disabled

    # Only transfers tab is disabled when only view transfers is not granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          Transfer management:
            granted: Partially
            privilege subtypes:
              View transfers: False
    And user of browser_user1 sees that ["Overview", "Files", "Shares, Open Data", "Providers", "Members", "Harvesters, Discovery", "Automation workflows"] tabs of "space1" are enabled
    And user of browser_user1 sees that Transfers tab of "space1" is disabled

    # All tabs are enabled when only view transfers from transfer management category is granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          Transfer management:
            granted: Partially
            privilege subtypes:
              View transfers: True
              Schedule replication: False
              Cancel replication: False
              Schedule eviction: False
              Cancel eviction: False
    And user of browser_user1 sees that all tabs of "space1" are enabled

    # Only transfers tab is disabled when none from transfer management category are granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          Transfer management:
            granted: False
    And user of browser_user1 sees that ["Overview", "Files", "Shares, Open Data", "Providers", "Members", "Harvesters, Discovery", "Automation workflows"] tabs of "space1" are enabled
    And user of browser_user1 sees that Transfers tab of "space1" is disabled

    # All tabs are enabled when none from QoS management category are granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          QoS management:
            granted: False
    And user of browser_user1 sees that all tabs of "space1" are enabled

    # All tabs are enabled when none from user management category are granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          User management:
            granted: False
    And user of browser_user1 sees that all tabs of "space1" are enabled

    # All tabs are enabled when none from group management category are granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          Group management:
            granted: False
    And user of browser_user1 sees that all tabs of "space1" are enabled

    # All tabs are enabled when none from support management category are granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          Support management:
            granted: False
    And user of browser_user1 sees that all tabs of "space1" are enabled

    # All tabs are enabled when none from harvester management category are granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          Harvester management:
            granted: False
    And user of browser_user1 sees that all tabs of "space1" are enabled

    # Only automation workflows tab is disabled when only view workflow execution is not granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          Automation management:
            granted: Partially
            privilege subtypes:
              View workflow executions: False
    And user of browser_user1 sees that ["Overview", "Files", "Shares, Open Data", "Transfers", "Providers", "Members", "Harvesters, Discovery"] tabs of "space1" are enabled
    And user of browser_user1 sees that Automation workflows tab of "space1" is disabled

    # All tabs are enabled when only view workflow executions from automation management category is granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          Automation management:
            granted: Partially
            privilege subtypes:
              View workflow executions: True
              Schedule workflow executions: False
              Manage workflow executions: False
    And user of browser_user1 sees that all tabs of "space1" are enabled

    # Only automation workflows tab is disabled when none from automation management category are granted
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage when all other are granted:
          Automation management:
            granted: False
    And user of browser_user1 sees that ["Overview", "Files", "Shares, Open Data", "Transfers", "Providers", "Members", "Harvesters, Discovery"] tabs of "space1" are enabled
    And user of browser_user1 sees that Automation workflows tab of "space1" is disabled



