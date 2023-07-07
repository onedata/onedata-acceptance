Feature: Basic management of spaces memberships in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - space-owner-user
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
          group2:
            owner: space-owner-user
            groups:
                - group1
          group3:
            owner: space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: space-owner-user
            groups:
                - group3
          space2:
            owner: space-owner-user
            groups:
                - group2
          space3:
            owner: space-owner-user
            users:
                - user1

    And users opened [browser1, space_owner_browser] browsers' windows
    And user of [browser1, space_owner_browser] opened [Onezone, Onezone] page
    And user of [browser1, space_owner_browser] logged as [user1, space-owner-user] to [Onezone, Onezone] service


  Scenario: User removes relation between group and space (direct)
    When user of space_owner_browser clicks on Data in the main menu
    And user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks "Members" of "space1" space in the sidebar
    And user of space_owner_browser clicks effective view mode in space members subpage
    And user of space_owner_browser clicks memberships view mode in space members subpage
    And user of space_owner_browser clicks "space-owner-user" user in "space1" space members users list
    And user of space_owner_browser sees 2 membership rows in space memberships mode
    And user of space_owner_browser clicks on "group3" member relation menu button to "space1" space
    And user of space_owner_browser clicks on "Remove relation" in space membership relation menu
    And user of space_owner_browser clicks on "Remove" button in modal "REMOVE MEMBER"
    Then user of space_owner_browser sees 1 membership row in space memberships mode
    And user of space_owner_browser does not see that "group3" group is member of "space1" space in space memberships mode


  Scenario: User removes relation between group and space (effect)
    When user of space_owner_browser clicks on Data in the main menu
    And user of space_owner_browser clicks "space2" on the spaces list in the sidebar
    And user of space_owner_browser clicks "Members" of "space2" space in the sidebar
    And user of space_owner_browser clicks "group2" group in "space2" space members groups list
    And user of space_owner_browser sets following privileges for "group2" group in space members subpage:
            Group management:
              granted: Partially
              privilege subtypes:
                Remove group: True

    And user of browser1 clicks on Data in the main menu
    And user of browser1 clicks "space2" on the spaces list in the sidebar
    And user of browser1 clicks "Members" of "space2" space in the sidebar
    And user of browser1 clicks effective view mode in space members subpage
    And user of browser1 clicks memberships view mode in space members subpage
    And user of browser1 clicks "user1" user in "space2" space members users list
    And user of browser1 clicks on "group2" member relation menu button to "space2" space
    And user of browser1 clicks on "Remove relation" in space membership relation menu
    And user of browser1 clicks on "Remove" button in modal "REMOVE MEMBER"
    Then user of browser1 sees that "space2" has disappeared on the spaces list in the sidebar


  Scenario: User leaves the space in members subpage
    When user of browser1 clicks on Data in the main menu
    And user of browser1 clicks "space3" on the spaces list in the sidebar
    And user of browser1 clicks "Members" of "space3" space in the sidebar
    And user of browser1 clicks effective view mode in space members subpage
    And user of browser1 clicks memberships view mode in space members subpage
    And user of browser1 clicks "user1" user in "space3" space members users list
    And user of browser1 clicks on "user1" member relation menu button to "space3" space
    And user of browser1 clicks on "Remove relation" in space membership relation menu
    And user of browser1 clicks on "Leave" button in modal "LEAVE SPACE"
    Then user of browser1 sees that "space3" has disappeared on the spaces list in the sidebar
