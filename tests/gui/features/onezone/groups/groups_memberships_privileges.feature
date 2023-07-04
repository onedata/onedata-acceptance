Feature: Basic management of groups privileges in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
            users:
                - user2
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
    When user of browser opens group "group1" members subpage
    And user of browser clicks "group2" group in "group1" group members groups list
    And user of browser sees following privileges of "group2" group in space members subpage:
          User management:
            granted: False
    And user of browser clicks "group2" group in "group1" group members groups list
    And user of browser sets following privileges for "group2" group in space members subpage:
          User management:
            granted: True
    And user of browser clicks "group2" group in "group1" group members groups list
    Then user of browser sees following privileges of "group2" group in space members subpage:
          User management:
            granted: True


  Scenario: User sees and modifies privileges to his group
    When user of browser opens group "group1" members subpage
    And user of browser clicks "user1" user in "group1" group members users list
    And user of browser sees following privileges of "user1" user in space members subpage:
          User management:
            granted: True
    And user of browser clicks "user1" user in "group1" group members users list
    And user of browser sets following privileges for "user1" user in space members subpage:
          User management:
            granted: False
    And user of browser clicks "user1" user in "group1" group members users list
    Then user of browser sees following privileges of "user1" user in space members subpage:
          User management:
            granted: False


  Scenario: User fails to see privileges without view privileges
    When user of browser opens group "group1" members subpage
    And user of browser clicks "user2" user in "group1" group members users list
    And user of browser sees privileges for "user2" user in group members subpage
    And user of browser refreshes site
    And user of browser clicks "user1" user in "group1" group members users list
    And user of browser sets following privileges for "user1" user in group members subpage:
          Group management:
            granted: Partially
            privilege subtypes:
              View privileges: False
    And user of browser clicks "user2" user in "group1" group members users list
    Then user of browser sees Insufficient privileges alert for "user2" user in group members subpage


  Scenario: User fails to remove relation without privileges
    When user of browser opens group "group1" members subpage
    And user of browser clicks "user1" user in "group1" group members users list
    And user of browser sets following privileges for "user1" user in group members subpage:
          Group hierarchy management:
            granted: Partially
            privilege subtypes:
              Remove child group: False

    And user of browser opens group "group4" members subpage
    And user of browser clicks "user1" user in "group1" group members users list
    And user of browser sets following privileges for "user1" user in group members subpage:
          Group hierarchy management:
            granted: Partially
            privilege subtypes:
              Leave parent group: False

    And user of browser opens group "group1" members subpage
    And user of browser clicks show view expand button in group members subpage header
    And user of browser clicks effective view mode in group members subpage
    And user of browser clicks memberships view mode in group members subpage
    And user of browser clicks "user1" user in "group1" group members users list
    And user of browser clicks on "group4" member relation menu button to "group1" group
    And user of browser clicks on "Remove relation" in group membership relation menu
    And user of browser clicks on "Remove" button in modal "REMOVE MEMBER"
    Then user of browser sees that error modal with text "insufficient privileges" appeared


  Scenario: User removes relation with privilege "Remove child group" and without "Leave parent group"
    When user of browser opens group "group4" members subpage
    And user of browser clicks "user1" user in "group1" group members users list
    And user of browser sets following privileges for "user1" user in group members subpage:
          Group hierarchy management:
            granted: Partially
            privilege subtypes:
              Leave parent group: False

    And user of browser opens group "group1" members subpage
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
    When user of browser opens group "group1" members subpage
    And user of browser clicks "user1" user in "group1" group members users list
    And user of browser sets following privileges for "user1" user in group members subpage:
          Group hierarchy management:
            granted: Partially
            privilege subtypes:
              Remove child group: False

    And user of browser opens group "group1" members subpage
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


  Scenario: User successfully bulk modifies privileges of all groups nested in his parent group
    When user of browser opens group "group1" members subpage
    And user of browser clicks on groups checkbox
    And user of browser clicks on bulk edit button
    And user of browser sees following privileges on modal:
          User management:
            granted: False
    And user of browser sets following privileges on modal:
          User management:
            granted: True
    And user of browser clicks "group2" group in "group1" group members groups list
    Then user of browser sees following privileges of "group2" group in space members subpage:
          User management:
            granted: True
    And user of browser clicks "group2" group in "group1" group members groups list
    And user of browser clicks "group4" group in "group1" group members groups list
    And user of browser sees following privileges of "group4" group in space members subpage:
          User management:
            granted: True


  Scenario: User successfully bulk modifies privileges to his group
    When user of browser opens group "group1" members subpage
    And user of browser clicks on users checkbox
    And user of browser clicks on bulk edit button
    And user of browser sees following privileges on modal:
          User management:
            granted: Partially
            privilege subtypes:
              Add user: Partially
              Remove user: Partially
    And user of browser sets following privileges on modal:
          User management:
            granted: False
    And user of browser clicks "user1" user in "group1" group members users list
    Then user of browser sees following privileges of "user1" user in space members subpage:
          User management:
            granted: False
    And user of browser clicks "user1" user in "group1" group members users list
    And user of browser clicks "user2" user in "group1" group members users list
    And user of browser sees following privileges of "user2" user in space members subpage:
          User management:
            granted: False

  Scenario: User successfully bulk modifies privileges of a group and user
    When user of browser opens group "group1" members subpage
    And user of browser clicks on "user2" users checkbox
    And user of browser clicks on "group2" groups checkbox
    And user of browser clicks on bulk edit button
    And user of browser sees following privileges on modal:
          User management:
            granted: False
    And user of browser sets following privileges on modal:
          User management:
            granted: True
    And user of browser clicks "group2" group in "group1" group members groups list
    Then user of browser sees following privileges of "group2" group in space members subpage:
          User management:
            granted: True
    And user of browser clicks "group2" group in "group1" group members groups list
    And user of browser clicks "user2" user in "group1" group members users list
    And user of browser sees following privileges of "user2" user in space members subpage:
          User management:
            granted: True


  Scenario: User fails to see privileges without view privileges changed with bulk edit
    When user of browser opens group "group1" members subpage
    And user of browser clicks "user2" user in "group1" group members users list
    And user of browser sees privileges for "user2" user in group members subpage
    And user of browser clicks on users checkbox
    And user of browser clicks on bulk edit button
    And user of browser sets following privileges on modal:
          Group management:
            granted: Partially
            privilege subtypes:
              View privileges: False
    And user of browser refreshes site
    And user of browser clicks "user2" user in "group1" group members users list
    Then user of browser sees Insufficient privileges alert for "user2" user in group members subpage


 Scenario: User fails to remove relation without privileges changed with bulk edit
    When user of browser opens group "group1" members subpage
    And user of browser clicks on "user1" users checkbox
    And user of browser clicks on bulk edit button
    And user of browser sets following privileges on modal:
          Group hierarchy management:
            granted: Partially
            privilege subtypes:
              Remove child group: False

    And user of browser opens group "group4" members subpage
    And user of browser clicks on "user1" users checkbox
    And user of browser clicks on bulk edit button
    And user of browser sets following privileges on modal:
          Group hierarchy management:
            granted: Partially
            privilege subtypes:
              Leave parent group: False

    And user of browser opens group "group1" members subpage
    And user of browser clicks show view expand button in group members subpage header
    And user of browser clicks effective view mode in group members subpage
    And user of browser clicks memberships view mode in group members subpage
    And user of browser clicks "user1" user in "group1" group members users list
    And user of browser clicks on "group4" member relation menu button to "group1" group
    And user of browser clicks on "Remove relation" in group membership relation menu
    And user of browser clicks on "Remove" button in modal "REMOVE MEMBER"
    Then user of browser sees that error modal with text "insufficient privileges" appeared
