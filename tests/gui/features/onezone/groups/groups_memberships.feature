Feature: Basic management of groups memberships in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user2
            users:
                - user1
            groups:
                - group2
          group2:
            owner: user1
            groups:
                - group3
          group3:
            owner: user1

    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User checks effective memberships
    When user of browser goes to group "group1" members subpage
    And user of browser clicks show view expand button in group members subpage header
    And user of browser clicks effective view mode in group members subpage
    And user of browser clicks memberships view mode in group members subpage
    And user of browser clicks "user1" user in "group1" group members users list

    Then user of browser sees 3 membership rows in group memberships mode
    And user of browser sees that "user1" user is member of "group1" group in group memberships mode
    And user of browser sees that "user1" user is member of "group2" group in group memberships mode
    And user of browser sees that "user1" user is member of "group3" group in group memberships mode
    And user of browser sees that "group2" group is member of "group1" group in group memberships mode
    And user of browser sees that "group3" group is member of "group2" group in group memberships mode


  Scenario: User removes relation between user and group in members subpage
    When user of browser goes to group "group1" members subpage
    And user of browser clicks show view expand button in group members subpage header
    And user of browser clicks effective view mode in group members subpage
    And user of browser clicks memberships view mode in group members subpage
    And user of browser clicks "user1" user in "group1" group members users list
    And user of browser sees 3 membership rows in group memberships mode

    And user of browser clicks on "user1" member relation menu button to "group1" group
    And user of browser clicks on "Remove relation" in group membership relation menu
    And user of browser clicks on "Leave" button in modal "LEAVE GROUP"

    Then user of browser sees 2 membership rows in group memberships mode
    And user of browser does not see that "user1" user is member of "group1" group in memberships mode


  Scenario: User removes relation between two groups (direct)
    When user of browser goes to group "group2" members subpage
    And user of browser clicks show view expand button in group members subpage header
    And user of browser clicks effective view mode in group members subpage
    And user of browser clicks memberships view mode in group members subpage
    And user of browser clicks "user1" user in "group2" group members users list
    And user of browser sees 2 membership rows in group memberships mode

    And user of browser clicks on "group3" member relation menu button to "group2" group
    And user of browser clicks on "Remove relation" in group membership relation menu
    And user of browser clicks on "Remove" button in modal "REMOVE MEMBER"

    Then user of browser sees 1 membership row in group memberships mode
    And user of browser does not see that "group3" group is member of "group2" group in group memberships mode

