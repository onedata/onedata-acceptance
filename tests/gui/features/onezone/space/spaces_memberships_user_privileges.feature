Feature: Basic management of user privileges for spaces in Onezone GUI

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

    And opened [browser_user1, space_owner_browser] with [user1, space-owner-user] signed in to [Onezone, Onezone] service


  Scenario: User sees and modifies privileges to his space
    When user of browser_user1 clicks "space1" on the spaces list in the sidebar
    And user of browser_user1 clicks Members of "space1" in the sidebar
    And user of browser_user1 clicks "user1" user in "space1" space members users list
    And user of browser_user1 sees following privileges of "user1" user in space members subpage:
          User management:
            granted: False
    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          User management:
            granted: True
    And user of browser_user1 refreshes site
    And user of browser_user1 clicks "user1" user in "space1" space members users list
    Then user of browser_user1 sees following privileges of "user1" user in space members subpage:
          User management:
            granted: True


  Scenario: User fails to generate space invite token because of lack in privileges
    When user of space_owner_browser clicks on Data in the main menu
    And user of space_owner_browser clicks "space2" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space2" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space2" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          User management:
            granted: False

    And user of browser_user1 clicks on Data in the main menu
    And user of browser_user1 clicks "space2" on the spaces list in the sidebar
    And user of browser_user1 clicks Members of "space2" in the sidebar
    And user of browser_user1 clicks on "Invite user using token" button in users list menu in "space2" space members view
    Then user of browser_user1 sees This resource could not be loaded alert in "Invite using token" modal


  Scenario: User fails to remove other user from given space because of lack in privileges
    When user of space_owner_browser clicks on Data in the main menu
    And user of space_owner_browser clicks "space2" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space2" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space2" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          User management:
            granted: False

    And user of browser_user1 clicks on Data in the main menu
    And user of browser_user1 clicks "space2" on the spaces list in the sidebar
    And user of browser_user1 removes "user2" user from "space2" space members
    Then user of browser_user1 sees that error modal with text "insufficient privileges" appeared


  Scenario: Non-space-owner successfully generates space invite token if he got user management privilege
    When user of space_owner_browser clicks on Data in the main menu
    And user of space_owner_browser clicks "space2" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space2" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space2" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
            User management:
              granted: True

    And user of browser_user1 clicks on Data in the main menu
    And user of browser_user1 clicks "space2" on the spaces list in the sidebar
    And user of browser_user1 clicks Members of "space2" in the sidebar
    And user of browser_user1 clicks on "Invite user using token" button in users list menu in "space2" space members view
    And user of browser_user1 sees that "Invite user using token" modal has appeared
    Then user of browser_user1 copies invitation token from modal
