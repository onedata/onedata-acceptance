Feature: Basic management of space management privileges for spaces in Onezone GUI

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


  Scenario: User fails to see privileges without view privileges
    When user of space_owner_browser clicks Members of "space1" space in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sees following privileges of "user1" user in space members subpage:
          Space management:
            granted: Partially
            privilege subtypes:
              View privileges: False

    And user of browser_user1 clicks "space1" on the spaces list in the sidebar
    And user of browser_user1 clicks Members of "space1" space in the sidebar
    And user of browser_user1 clicks "space-owner-user" user in "space1" space members users list
    Then user of browser_user1 sees Insufficient privileges alert for "space-owner-user" user in space members subpage


  Scenario: User fails to see space without view space privilege
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" space in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Space management:
            granted: Partially
            privilege subtypes:
              View space: False

    Then user of browser_user1 sees that [Members, Shares Open Data, Harvesters Discovery] of "space1" in the sidebar are disabled


  Scenario: User fails to rename space because of lack in privileges
    When user of space_owner_browser clicks "space2" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space2" space in the sidebar
    And user of space_owner_browser clicks "user1" user in "space2" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Space management:
            granted: Partially
            privilege subtypes:
              Modify space: False

    And user of browser_user1 clicks on Data in the main menu
    And user of browser_user1 clicks "space1" on the spaces list in the sidebar
    And user of browser_user1 writes "space2" into rename space text field
    And user of browser_user1 confirms rename the space using confirmation button
    Then user of browser_user1 sees that error modal with text "Changing name failed" appeared


  Scenario: Non-owner-user fails to remove space because of lack in privileges
    When user of space_owner_browser clicks "space2" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space2" space in the sidebar
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


  Scenario: Non-owner-user views space
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" space in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Space management:
            granted: True

    And user of browser_user1 clicks on Data in the main menu
    Then user of browser_user1 sees that "space1" has appeared on the spaces list in the sidebar


  Scenario: Non-owner-user fails to view space because of lack in privileges
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" space in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Space management:
            granted: False

    And user of browser_user1 clicks on Data in the main menu
    Then user of browser_user1 sees that [Members, Shares Open Data, Harvesters Discovery] of "space1" in the sidebar are disabled


  Scenario: Non-owner-user sets privileges for other user
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" space in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Space management:
            granted: Partially
            privilege subtypes:
              View privileges: True
              Set privileges: True

    And user of browser_user1 clicks on Data in the main menu
    And user of browser_user1 clicks "space1" on the spaces list in the sidebar
    And user of browser_user1 clicks Members of "space1" space in the sidebar
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
    And user of space_owner_browser clicks Members of "space1" space in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Space management:
            granted: Partially
            privilege subtypes:
              View privileges: True
              Set privileges: False

    And user of browser_user1 clicks on Data in the main menu
    And user of browser_user1 clicks "space1" on the spaces list in the sidebar
    And user of browser_user1 clicks Members of "space1" space in the sidebar
    And user of browser_user1 clicks "user2" user in "space1" space members users list
    And user of browser_user1 sets following privileges for "user2" user in space members subpage:
          Space management:
            granted: Partially
            privilege subtypes:
              View privileges: True
              Set privileges: True

    Then user of browser_user1 sees that error modal with text "insufficient privileges" appeared

