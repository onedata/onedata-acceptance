Feature: Multi Browser basic management of groups memberships in Onezone GUI


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
          group3:
            owner: user2
            groups:
                - group2
          group4:
            owner: user1
            groups:
                - group3

    And users opened [browser1, browser2] browsers' windows
    And user of [browser1, browser2] opened [Onezone, Onezone] page
    And user of [browser1, browser2] logged as [user1, user2] to [Onezone, Onezone] service


  Scenario: User removes relation between two groups (effective)
    When user of browser2 goes to group "group2" members subpage
    And user of browser2 clicks "group1" group in "group2" group members groups list
    And user of browser2 expands "Group hierarchy management" privilege for "group1" group in group members subpage
    And user of browser2 checks "Leave parent group" privilege toggle in "Group hierarchy management" for "group1" group in group members subpage
    And user of browser2 clicks Save button for "group1" group in group members subpage

    And user of browser1 goes to group "group4" members subpage
    And user of browser1 clicks show view expand button in group members subpage header
    And user of browser1 clicks effective view mode in group members subpage
    And user of browser1 clicks memberships view mode in group members subpage
    And user of browser1 clicks "user1" user in "group4" group members users list
    And user of browser1 sees 2 membership rows in group memberships mode

    And user of browser1 clicks on "group2" member relation menu button to "group3" group
    And user of browser1 clicks on "Remove relation" in group membership relation menu
    And user of browser1 clicks on "Remove" button in modal "REMOVE MEMBER"

    Then user of browser1 sees 1 membership row in group memberships mode
    And user of browser1 does not see that "group2" group is member of "group3" group in group memberships mode