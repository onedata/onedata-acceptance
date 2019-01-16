Feature: Basic management of groups privileges in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
            groups:
                - group2
                - group4
          group2:
            owner: user2
          group3:
            owner: user2
            users:
                - user1
            groups:
                - group1
          group4:
            owner: user1

    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User sees and modifies privileges to group, which is nested in his parent group
    When user of browser goes to group "group1" members subpage
    And user of browser clicks "group2" group in "group1" group members groups list
    And user of browser sees that "User management" is not checked for "group2" group in group members subpage
    And user of browser checks "User management" privilege toggle for "group2" group in group members subpage
    And user of browser clicks Save button for "group2" group in group members subpage
    Then user of browser sees that "User management" is checked for "group2" group in group members subpage


  Scenario: User sees and modifies privileges to his group
    When user of browser goes to group "group1" members subpage
    And user of browser clicks "user1" user in "group1" group members users list
    And user of browser sees that "User management" is checked for "user1" user in group members subpage
    And user of browser unchecks "User management" privilege toggle for "user1" user in group members subpage
    And user of browser clicks Save button for "user1" user in group members subpage
    Then user of browser sees that "User management" is not checked for "user1" user in group members subpage


  Scenario: User fails to see privileges without view privileges
    When user of browser goes to group "group1" members subpage
    And user of browser clicks "user1" user in "group1" group members users list
    And user of browser expands "Group management" privilege for "user1" user in group members subpage
    And user of browser unchecks "View privileges" privilege toggle in "Group management" for "user1" user in group members subpage
    And user of browser clicks Save button for "user1" user in group members subpage
    And user of browser refreshes site
    And user of browser clicks "user1" user in "group1" group members users list
    Then user of browser sees Insufficient permissions alert for "user1" user in group members subpage


  Scenario: User fails to remove relation without privileges
    When user of browser goes to group "group1" members subpage
    And user of browser clicks "user1" user in "group1" group members users list
    And user of browser expands "Group hierarchy management" privilege for "user1" user in group members subpage
    And user of browser unchecks "Remove child group" privilege toggle in "Group hierarchy management" for "user1" user in group members subpage
    And user of browser clicks Save button for "user1" user in group members subpage

    And user of browser goes to group "group4" members subpage
    And user of browser clicks "user1" user in "group1" group members users list
    And user of browser expands "Group hierarchy management" privilege for "user1" user in group members subpage
    And user of browser unchecks "Leave parent group" privilege toggle in "Group hierarchy management" for "user1" user in group members subpage
    And user of browser clicks Save button for "user1" user in group members subpage

    And user of browser goes to group "group1" members subpage
    And user of browser clicks show view expand button in group members subpage header
    And user of browser clicks effective view mode in group members subpage
    And user of browser clicks memberships view mode in group members subpage
    And user of browser clicks "user1" user in "group1" group members users list
    And user of browser clicks on "group4" member relation menu button to "group1" group
    And user of browser clicks on "Remove relation" in group membership relation menu
    And user of browser clicks on "Remove" button in modal "REMOVE MEMBER"
    Then user of browser sees that error modal with text "Insufficient permissions" appeared


  Scenario: User removes relation with privilege "Remove child group" and without "Leave parent group"
    When user of browser goes to group "group4" members subpage
    And user of browser clicks "user1" user in "group1" group members users list
    And user of browser expands "Group hierarchy management" privilege for "user1" user in group members subpage
    And user of browser unchecks "Leave parent group" privilege toggle in "Group hierarchy management" for "user1" user in group members subpage
    And user of browser clicks Save button for "user1" user in group members subpage

    And user of browser goes to group "group1" members subpage
    And user of browser clicks show view expand button in group members subpage header
    And user of browser clicks effective view mode in group members subpage
    And user of browser clicks memberships view mode in group members subpage
    And user of browser clicks "user1" user in "group1" group members users list
    And user of browser sees 2 membership rows in space memberships mode
    And user of browser clicks on "group4" member relation menu button to "group1" group
    And user of browser clicks on "Remove relation" in group membership relation menu
    And user of browser clicks on "Remove" button in modal "REMOVE MEMBER"
    Then user of browser sees 1 membership row in space memberships mode
    And user of browser does not see that "group4" group is member of "group1" group in group memberships mode


  Scenario: User removes relation with privilege "Leave parent group" and without "Remove child group"
    When user of browser goes to group "group1" members subpage
    And user of browser clicks "user1" user in "group1" group members users list
    And user of browser expands "Group hierarchy management" privilege for "user1" user in group members subpage
    And user of browser unchecks "Remove child group" privilege toggle in "Group hierarchy management" for "user1" user in group members subpage
    And user of browser clicks Save button for "user1" user in group members subpage

    And user of browser goes to group "group1" members subpage
    And user of browser clicks show view expand button in group members subpage header
    And user of browser clicks effective view mode in group members subpage
    And user of browser clicks memberships view mode in group members subpage
    And user of browser clicks "user1" user in "group1" group members users list
    And user of browser sees 2 membership rows in space memberships mode
    And user of browser clicks on "group4" member relation menu button to "group1" group
    And user of browser clicks on "Remove relation" in group membership relation menu
    And user of browser clicks on "Remove" button in modal "REMOVE MEMBER"
    Then user of browser sees 1 membership row in space memberships mode
    And user of browser does not see that "group4" group is member of "group1" group in group memberships mode