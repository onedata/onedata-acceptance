Feature: Basic management of spaces privileges in Onezone GUI


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
            users:
                - user2
          space2:
            owner: user1
            groups:
                - group2
          space3:
            owner: user1
            users:
                - user2

    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User fails to invite provider without privileges
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Members of "space1" in the sidebar
    And user of browser clicks "user1" user in "space1" space members users list
    And user of browser expands "Support management" privilege for "user1" user in space members subpage
    And user of browser unchecks "Add support" privilege toggle in "Support management" for "user1" user in space members subpage
    And user of browser clicks Save button for "user1" user in space members subpage
    And user of browser clicks Providers of "space1" in the sidebar
    And user of browser clicks Add support button on providers page
    Then user of browser sees Insufficient permissions alert on providers page


  Scenario: User sees and modifies privileges to his space
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Members of "space1" in the sidebar
    And user of browser clicks "user1" user in "space1" space members users list
    And user of browser sees that "User management" is checked for "user1" user in space members subpage
    And user of browser unchecks "User management" privilege toggle for "user1" user in space members subpage
    And user of browser clicks Save button for "user1" user in space members subpage
    Then user of browser sees that "User management" is not checked for "user1" user in space members subpage


  Scenario: User fails to see privileges without view privileges
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Members of "space1" in the sidebar
    And user of browser clicks "user2" user in "space1" space members users list
    And user of browser sees privileges for "user2" user in space members subpage
    And user of browser refreshes site
    And user of browser clicks "user1" user in "space1" space members users list
    And user of browser expands "Space management" privilege for "user1" user in space members subpage
    And user of browser unchecks "View privileges" privilege toggle in "Space management" for "user1" user in space members subpage
    And user of browser clicks Save button for "user1" user in space members subpage
    And user of browser refreshes site
    And user of browser clicks "user2" user in "space1" space members users list
    Then user of browser sees Insufficient permissions alert for "user2" user in space members subpage


  Scenario: User fails to see space without view space privilege
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Members of "space1" in the sidebar
    And user of browser clicks "user1" user in "space1" space members users list
    And user of browser expands "Space management" privilege for "user1" user in space members subpage
    And user of browser unchecks "View space" privilege toggle in "Space management" for "user1" user in space members subpage
    And user of browser clicks Save button for "user1" user in space members subpage
    And user of browser refreshes site
    Then user of browser sees Insufficient permissions alert in space members subpage


  Scenario: User fails to remove group from space without remove group privileges
    When user of browser clicks "space2" on the spaces list in the sidebar
    And user of browser clicks Members of "space2" in the sidebar
    And user of browser clicks "user1" user in "space2" space members users list
    And user of browser expands "Group management" privilege for "user1" user in space members subpage
    And user of browser unchecks "Remove group" privilege toggle in "Group management" for "user1" user in space members subpage
    And user of browser clicks Save button for "user1" user in space members subpage

    And user of browser clicks show view expand button in space members subpage header
    And user of browser clicks memberships view mode in space members subpage
    And user of browser clicks "group2" group in "space2" space members groups list
    And user of browser clicks on "group2" member relation menu button to "space2" space
    And user of browser clicks on "Remove relation" in space membership relation menu
    And user of browser clicks on "Remove" button in modal "REMOVE MEMBER"
    Then user of browser sees that error modal with text "insufficient privileges" appeared


  Scenario: User fails to remove user from space without remove user privileges
    When user of browser clicks "space3" on the spaces list in the sidebar
    And user of browser clicks Members of "space3" in the sidebar
    And user of browser clicks "user1" user in "space3" space members users list
    And user of browser expands "User management" privilege for "user1" user in space members subpage
    And user of browser unchecks "Remove user" privilege toggle in "User management" for "user1" user in space members subpage
    And user of browser clicks Save button for "user1" user in space members subpage

    And user of browser clicks show view expand button in space members subpage header
    And user of browser clicks memberships view mode in space members subpage
    And user of browser clicks "user2" user in "space3" space members users list
    And user of browser clicks on "user2" member relation menu button to "space3" space
    And user of browser clicks on "Remove relation" in space membership relation menu
    And user of browser clicks on "Remove" button in modal "REMOVE MEMBER"
    Then user of browser sees that error modal with text "insufficient privileges" appeared

