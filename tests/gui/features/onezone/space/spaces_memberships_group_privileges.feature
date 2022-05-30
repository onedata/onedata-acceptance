Feature: Basic management of group privileges for spaces in Onezone GUI

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


  Scenario: Non-space-owner fails to generate group invite token because of lack in privileges
    When user of space_owner_browser clicks "space2" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space2" space in the sidebar
    And user of space_owner_browser clicks "user1" user in "space2" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Group management:
            granted: False

    And user of browser_user1 clicks on Data in the main menu
    And user of browser_user1 clicks "space2" on the spaces list in the sidebar
    And user of browser_user1 clicks Members of "space2" space in the sidebar
    And user of browser_user1 clicks on "Invite group using token" button in groups list menu in "space2" space members view
    Then user of browser_user1 sees This resource could not be loaded alert in "Invite using token" modal


  Scenario: Non-space-owner generates group invite token to join space
    When user of space_owner_browser clicks "space2" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space2" space in the sidebar
    And user of space_owner_browser clicks "user1" user in "space2" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Group management:
            granted: Partially
            privilege subtypes:
              Add group: True

    And user of browser_user1 clicks on Data in the main menu
    And user of browser_user1 clicks "space2" on the spaces list in the sidebar
    And user of browser_user1 clicks Members of "space2" space in the sidebar
    And user of browser_user1 clicks on "Invite group using token" button in groups list menu in "space2" space members view
    And user of browser_user1 sees that "Invite group using token" modal has appeared
    Then user of browser_user1 copies invitation token from modal


  Scenario: User fails to remove group from space without remove group privileges
    When user of space_owner_browser clicks "space2" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space2" space in the sidebar
    And user of space_owner_browser clicks "user1" user in "space2" space members users list
    And user of space_owner_browser sees following privileges of "user1" user in space members subpage:
          Group management:
            granted: False

    And user of browser_user1 clicks Members of "space2" space in the sidebar
    And user of browser_user1 clicks show view expand button in space members subpage header
    And user of browser_user1 clicks memberships view mode in space members subpage
    And user of browser_user1 clicks "group2" group in "space2" space members groups list
    And user of browser_user1 clicks on "group2" member relation menu button to "space2" space
    And user of browser_user1 clicks on "Remove relation" in space membership relation menu
    And user of browser_user1 clicks on "Remove" button in modal "REMOVE MEMBER"
    Then user of browser_user1 sees that error modal with text "insufficient privileges" appeared
