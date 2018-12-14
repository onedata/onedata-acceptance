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
    And user of browser clicks show view option in group members subpage
    And user of browser clicks effective view mode in group members subpage
    And user of browser clicks memberships view mode in group members subpage
    And user of browser clicks user "user1" in group "group1" members users list

    Then user of browser sees 3 membership rows in group memberships mode
    And user of browser sees user "user1" is member of group "group1" in group memberships mode
    And user of browser sees user "user1" is member of group "group2" in group memberships mode
    And user of browser sees user "user1" is member of group "group3" in group memberships mode
    And user of browser sees group "group2" is member of group "group1" in group memberships mode
    And user of browser sees group "group3" is member of group "group2" in group memberships mode


  Scenario: User removes relation between user and group in members subpage
    When user of browser goes to group "group1" members subpage
    And user of browser clicks show view option in group members subpage
    And user of browser clicks effective view mode in group members subpage
    And user of browser clicks memberships view mode in group members subpage
    And user of browser clicks user "user1" in group "group1" members users list
    And user of browser sees 3 membership rows in memberships mode

    And user of browser clicks on member "user1" relation menu button to group "group1"
    And user of browser clicks on "Remove relation" in group membership relation menu
    And user of browser clicks on button "Leave" in modal "LEAVE GROUP"

    Then user of browser sees 2 membership rows in memberships mode
    And user of browser does not see user "user1" is member of group "group1" in memberships mode


  Scenario: User removes relation between two groups (direct)
    When user of browser goes to group "group2" members subpage
    And user of browser clicks show view option in group members subpage
    And user of browser clicks effective view mode in group members subpage
    And user of browser clicks memberships view mode in group members subpage
    And user of browser clicks user "user1" in group "group2" members users list
    And user of browser sees 2 membership rows in group memberships mode

    And user of browser clicks on member "group3" relation menu button to group "group2"
    And user of browser clicks on "Remove relation" in group membership relation menu
    And user of browser clicks on button "Remove" in modal "REMOVE MEMBER"

    Then user of browser sees 1 membership rows in group memberships mode
    And user of browser does not see group "group3" is member of group "group2" in group memberships mode

