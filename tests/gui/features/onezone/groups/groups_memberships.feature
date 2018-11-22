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

    And users opened [browser1, browser2] browsers' windows
    And user of [browser1, browser2] opened [Onezone, Onezone] page
    And user of [browser1, browser2] logged as [user1, user2] to Onezone service


  Scenario: User checks effective memberships
    When user of browser1 goes to group "group1" members subpage
    And user of browser1 clicks show view option in members subpage
    And user of browser1 clicks effective view mode in members subpage
    And user of browser1 clicks memberships view mode in members subpage
    And user of browser1 clicks user "user1" in group "group1" members users list
    Then user of browser1 sees 3 membership rows in memberships mode
    And user of browser1 sees user "user1" is member of group "group1" in memberships mode
    And user of browser1 sees user "user1" is member of group "group2" in memberships mode
    And user of browser1 sees user "user1" is member of group "group3" in memberships mode
    And user of browser1 sees group "group2" is member of group "group1" in memberships mode
    And user of browser1 sees group "group3" is member of group "group2" in memberships mode


  Scenario: User remove relation in members subpage
    When user of browser2 goes to group "group1" members subpage
    And user of browser2 clicks show view option in members subpage
    And user of browser2 clicks effective view mode in members subpage
    And user of browser2 clicks memberships view mode in members subpage
    And user of browser2 clicks user "user1" in group "group1" members users list
    And user of browser2 clicks on member "user1" relation menu button to group "group1"
    And user of browser2 clicks on "Remove relation" in membership relation menu
    And user of browser2 clicks on button "Remove" in modal "REMOVE MEMBER"
    Then user of browser1 goes to group "group1" members subpage
    And user of browser1 clicks show view option in members subpage
    And user of browser1 clicks effective view mode in members subpage
    And user of browser1 clicks memberships view mode in members subpage
    And user of browser1 clicks user "user1" in group "group1" members users list
    And user of browser1 sees 2 membership rows in memberships mode
    And user of browser1 does not see user "user1" is member of group "group1" in memberships mode
