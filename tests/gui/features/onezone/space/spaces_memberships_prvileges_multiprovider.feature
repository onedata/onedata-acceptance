Feature: Basic management of spaces privileges in Onezone GUI with two providers


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: space-owner-user
            users:
                - user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
                - oneprovider-2:
                    storage: posix
                    size: 1000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1:
                      - file1

    And opened [browser_user1, space_owner_browser] with [user1, space-owner-user] signed in to [Onezone, Onezone] service


Scenario: Non-space-owner successfully views transfers if he got View Transfers privilege
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Transfer management:
            granted: False

    And user of browser_user1 sees that Transfers tab of "space1" is disabled
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Transfer management:
            granted: Partially
            privilege subtypes:
              View transfers: True

    And user of browser_user1 clicks Transfers of "space1" in the sidebar


  Scenario: Non-space-owner successfully schedules replication if he got Transfer management privileges
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Transfer management:
            granted: Partially
            privilege subtypes:
              View transfers: True
              Schedule replication: False

    And user of browser_user1 clicks Files of "space1" in the sidebar
    And user of browser_user1 sees file browser in files tab in Oneprovider page
    And user of browser_user1 clicks on menu for "dir1" directory in file browser
    And user of browser_user1 clicks "Data distribution" option in data row menu in file browser
    And user of browser_user1 sees that "Data distribution" modal has appeared
    And user of browser_user1 does not see Replicate here option when clicking on provider one menu button
    And user of browser_user1 closes "Data distribution" modal

    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Transfer management:
            granted: Partially
            privilege subtypes:
              View transfers: True
              Schedule replication: True

    And user of browser_user1 replicates "dir1" to provider "oneprovider-2"


  Scenario: Non-space-owner successfully cancels replication and then cancels it if he got Transfer management privileges
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Transfer management:
            granted: Partially
            privilege subtypes:
              View transfers: True
              Cancel replication: True

    And user of browser_user1 clicks Transfers of "space1" in the sidebar
    And user of browser_user1 waits for Transfers page to load

    And user of space_owner_browser clicks Files of "space1" in the sidebar
    And user of space_owner_browser sees file browser in files tab in Oneprovider page
    And user of space_owner_browser clicks on menu for "dir1" directory in file browser
    And user of space_owner_browser clicks "Data distribution" option in data row menu in file browser
    And user of space_owner_browser sees that "Data distribution" modal has appeared
    And user of space_owner_browser replicates "dir1" to provider "oneprovider-2"

    And user of browser_user1 clicks on tranfer if "dir1" menu
    And user of browser_user1 Cancels..

    Scenario: Non-space-owner successfully schedules eviction if he got Transfer management privileges
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Transfer management:
            granted: Partially
            privilege subtypes:
              View transfers: True
              Schedule eviction: False

    And user of browser_user1 clicks Files of "space1" in the sidebar
    And user of browser_user1 sees file browser in files tab in Oneprovider page
    And user of browser_user1 clicks on menu for "dir1" directory in file browser
    And user of browser_user1 clicks "Data distribution" option in data row menu in file browser
    And user of browser_user1 sees that "Data distribution" modal has appeared
    And user of browser_user1 does not see Evict option when clicking on provider one menu button
    And user of browser_user1 closes "Data distribution" modal

    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Transfer management:
            granted: Partially
            privilege subtypes:
              View transfers: True
              Schedule eviction: True

    And user of browser_user1 evicts file "file1" from provider oneprovider-2

