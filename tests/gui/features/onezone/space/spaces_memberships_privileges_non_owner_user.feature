Feature: Basic management of spaces privileges using non owner user in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
            - space-owner-user
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
          group2:
            owner: space-owner-user
            groups:
                - group1
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
          space2:
            owner: space-owner-user
            users:
                - user1
                - user2
            groups:
                - group2
          space3:
            owner: space-owner-user
            users:
                - user1

    And opened [browser_user1, space_owner_browser] with [user1, space-owner-user] signed in to [Onezone, Onezone] service


  Scenario: Non-owner-user fails to remove space because of lack in privileges
    When user of space_owner_browser clicks "space2" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space2" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space2" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Space management:
            granted: Partially
            privilege subtypes:
              Remove space: False

    And user of browser_user1 clicks "space2" on the spaces list in the sidebar
    And user of browser_user1 clicks on "Remove" button in space "space2" menu
    And user of browser_user1 clicks on understand notice checkbox in "Remove space" modal
    And user of browser_user1 clicks on "Remove" button in "Remove space" modal
    Then user of browser_user1 sees that error modal with text "Removing the space failed" appeared


  Scenario: Non-owner-user fails to generate group invite token because of lack in privileges
    When user of space_owner_browser clicks "space2" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space2" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space2" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Group management:
            granted: False

    And user of browser_user1 clicks on Data in the main menu
    And user of browser_user1 clicks "space2" on the spaces list in the sidebar
    And user of browser_user1 clicks Members of "space2" in the sidebar
    And user of browser_user1 clicks on "Invite group using token" button in groups list menu in "space2" space members view
    Then user of browser_user1 sees This resource could not be loaded alert in "Invite using token" modal


  Scenario: Non-owner-user generates group invite token to join space
    When user of space_owner_browser clicks "space2" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space2" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space2" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Group management:
            granted: Partially
            privilege subtypes:
              Add group: True

    And user of browser_user1 clicks on Data in the main menu
    And user of browser_user1 clicks "space2" on the spaces list in the sidebar
    And user of browser_user1 clicks Members of "space2" in the sidebar
    And user of browser_user1 clicks on "Invite group using token" button in groups list menu in "space2" space members view
    And user of browser_user1 sees that "Invite group using token" modal has appeared
    Then user of browser_user1 copies invitation token from modal


  Scenario: Non-owner-user generates add support token
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Support management:
            granted: True

    And user of browser_user1 clicks Providers of "space1" in the sidebar
    And user of browser_user1 clicks Add support button on providers page
    And user of browser_user1 clicks Copy button on Add support page
    Then user of browser_user1 sees an info notify with text matching to: .*copied.*


  Scenario: Non-owner-user views space
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Space management:
            granted: True

    And user of browser_user1 clicks on Data in the main menu
    Then user of browser_user1 sees that "space1" has appeared on the spaces list in the sidebar


  Scenario: Non-owner-user fails to view space because of lack in privileges
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Space management:
            granted: False

    And user of browser_user1 clicks on Data in the main menu
    Then user of browser_user1 sees that [Members, Shares, Harvesters] of "space1" in the sidebar are disabled


  Scenario: Non-owner-user sets privileges for other user
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Space management:
            granted: Partially
            privilege subtypes:
              View privileges: True
              Set privileges: True

    And user of browser_user1 clicks on Data in the main menu
    And user of browser_user1 clicks "space1" on the spaces list in the sidebar
    And user of browser_user1 clicks Members of "space1" in the sidebar
    And user of browser_user1 clicks "user2" user in "space1" space members users list
    And user of browser_user1 sets following privileges for "user2" user in space members subpage:
          Space management:
            granted: Partially
            privilege subtypes:
              View privileges: False
              Set privileges: False

    And user of browser_user1 clicks "user2" user in "space1" space members users list
    Then user of browser_user1 sees following privileges of "user2" user in space members subpage:
          Space management:
            granted: Partially
            privilege subtypes:
              View privileges: False
              Set privileges: False


  Scenario: Non-owner-user fails to set privileges to other user because of lack in privileges
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Space management:
            granted: Partially
            privilege subtypes:
              View privileges: True
              Set privileges: False

    And user of browser_user1 clicks on Data in the main menu
    And user of browser_user1 clicks "space1" on the spaces list in the sidebar
    And user of browser_user1 clicks Members of "space1" in the sidebar
    And user of browser_user1 clicks "user2" user in "space1" space members users list
    And user of browser_user1 sets following privileges for "user2" user in space members subpage:
          Space management:
            granted: Partially
            privilege subtypes:
              View privileges: True
              Set privileges: True

    Then user of browser_user1 sees that error modal with text "insufficient privileges" appeared

