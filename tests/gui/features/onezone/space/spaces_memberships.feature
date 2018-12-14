Feature: Basic management of spaces memberships in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
          group2:
            owner: user2
            groups:
                - group1
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: user1
            groups:
                - group1
          space2:
            owner: user2
            groups:
                - group2
          space3:
            owner: user2
            users:
                - user1

    And users opened [browser1, browser2] browsers' windows
    And user of [browser1, browser2] opened [Onezone, Onezone] page
    And user of [browser1, browser2] logged as [user1, user2] to Onezone service


  Scenario: User leaves from space in members subpage
    When user of browser1 clicks on Spaces in the sidebar
    And user of browser1 clicks "space3" on the spaces list in the sidebar
    And user of browser1 clicks Members of "space3" in the sidebar
    And user of browser1 clicks show view option in space members subpage
    And user of browser1 clicks effective view mode in space members subpage
    And user of browser1 clicks memberships view mode in space members subpage
    And user of browser1 clicks "user1" user in "space3" space members users list
    And user of browser1 clicks on "user1" member relation menu button to "space3" space
    And user of browser1 clicks on "Remove relation" in space membership relation menu
    And user of browser1 clicks on "Leave" button in modal "LEAVE SPACE"
    Then user of browser1 sees that "space3" has disappeared on the spaces list in the sidebar


  Scenario: User removes relation between group and space (direct)
    When user of browser1 clicks on Spaces in the sidebar
    And user of browser1 clicks "space1" on the spaces list in the sidebar
    And user of browser1 clicks Members of "space1" in the sidebar
    And user of browser1 clicks show view option in space members subpage
    And user of browser1 clicks effective view mode in space members subpage
    And user of browser1 clicks memberships view mode in space members subpage
    And user of browser1 clicks "user1" user in "space1" space members users list
    And user of browser1 sees 2 membership rows in space memberships mode
    And user of browser1 clicks on "group1" member relation menu button to "space1" space
    And user of browser1 clicks on "Remove relation" in space membership relation menu
    And user of browser1 clicks on "Remove" button in modal "REMOVE MEMBER"
    Then user of browser1 sees 1 membership rows in space memberships mode
    And user of browser1 does not see "group1" group is member of "space1" space in space memberships mode


  Scenario: User removes relation between group and space (effect)
    When user of browser2 clicks on Spaces in the sidebar
    And user of browser2 clicks "space2" on the spaces list in the sidebar
    And user of browser2 clicks Members of "space2" in the sidebar
    And user of browser2 clicks "group2" group in "space2" space members groups list
    And user of browser2 expands "Group management" privilege for "group2" group in space members subpage
    And user of browser2 checks "Remove group" privilege toggle in "Group management" for "group2" group in space members subpage
    And user of browser2 clicks Save button for "group2" group in space members subpage

    And user of browser1 clicks on Spaces in the sidebar
    And user of browser1 clicks "space2" on the spaces list in the sidebar
    And user of browser1 clicks Members of "space2" in the sidebar
    And user of browser1 clicks show view option in space members subpage
    And user of browser1 clicks effective view mode in space members subpage
    And user of browser1 clicks memberships view mode in space members subpage
    And user of browser1 clicks "user1" user in "space2" space members users list
    And user of browser1 clicks on "group2" member relation menu button to "space2" space
    And user of browser1 clicks on "Remove relation" in space membership relation menu
    And user of browser1 clicks on "Remove" button in modal "REMOVE MEMBER"
    Then user of browser1 sees that "space2" has disappeared on the spaces list in the sidebar
