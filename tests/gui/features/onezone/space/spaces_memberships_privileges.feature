Feature: Basic management of spaces privileges in Onezone GUI


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
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: space-owner-user
            users:
                - user1
          space2:
            owner: space-owner-user
            users:
                - user1
            groups:
                - group2
          space3:
            owner: space-owner-user
            users:
                - user1

    And opened [browser_user1, space_owner_browser] with [user1, space-owner-user] signed in to [Onezone, Onezone] service


  Scenario: User fails to invite provider without privileges
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sees following privileges of "user1" user in space members subpage:
          Support management:
            granted: False
    And user of browser_user1 clicks Providers of "space1" in the sidebar
    And user of browser_user1 clicks Add support button on providers page
    Then user of browser_user1 sees This resource could not be loaded alert on providers page


  Scenario: User sees and modifies privileges to his space
    When user of browser_user1 clicks "space1" on the spaces list in the sidebar
    And user of browser_user1 clicks Members of "space1" in the sidebar
    And user of browser_user1 clicks "user1" user in "space1" space members users list
    And user of browser_user1 sees following privileges of "user1" user in space members subpage:
          User management:
            granted: False
    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          User management:
            granted: True
    And user of browser_user1 refreshes site
    And user of browser_user1 clicks "user1" user in "space1" space members users list
    Then user of browser_user1 sees following privileges of "user1" user in space members subpage:
          User management:
            granted: True


  Scenario: User fails to see privileges without view privileges
    When user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sees following privileges of "user1" user in space members subpage:
          Space management:
            granted: Partially
            privilege subtypes:
              View privileges: False

    And user of browser_user1 clicks "space1" on the spaces list in the sidebar
    And user of browser_user1 clicks Members of "space1" in the sidebar
    And user of browser_user1 clicks "space-owner-user" user in "space1" space members users list
    Then user of browser_user1 sees Insufficient privileges alert for "space-owner-user" user in space members subpage


  Scenario: User fails to see privileges of another user until he is granted all privileges by becoming an owner
    When user of browser_user1 clicks Members of "space1" in the sidebar
    And user of browser_user1 clicks "space-owner-user" user in "space1" space members users list
    And user of browser_user1 sees Insufficient privileges alert for "space-owner-user" user in space members subpage

    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "Make an owner" for "user1" user in users list

    And user of browser_user1 refreshes site
    And user of browser_user1 clicks "user1" user in "space1" space members users list
    And user of browser_user1 sees "This user is a space owner and is authorized to perform all operations, regardless of the assigned privileges." warning for "user1" user in space members subpage

    And user of browser_user1 clicks "space-owner-user" user in "space1" space members users list
    Then user of browser_user1 sees privileges for "space-owner-user" user in space members subpage


  Scenario: User fails to see space without view space privilege
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space1" space members users list
    And user of space_owner_browser sets following privileges for "user1" user in space members subpage:
          Space management:
            granted: Partially
            privilege subtypes:
              View space: False

    Then user of browser_user1 sees that [Members, Shares, Harvesters] of "space1" in the sidebar are disabled

  Scenario: User fails to remove group from space without remove group privileges
    When user of space_owner_browser clicks "space2" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space2" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space2" space members users list
    And user of space_owner_browser sees following privileges of "user1" user in space members subpage:
          Group management:
            granted: False

    And user of browser_user1 clicks Members of "space2" in the sidebar
    And user of browser_user1 clicks show view expand button in space members subpage header
    And user of browser_user1 clicks memberships view mode in space members subpage
    And user of browser_user1 clicks "group2" group in "space2" space members groups list
    And user of browser_user1 clicks on "group2" member relation menu button to "space2" space
    And user of browser_user1 clicks on "Remove relation" in space membership relation menu
    And user of browser_user1 clicks on "Remove" button in modal "REMOVE MEMBER"
    Then user of browser_user1 sees that error modal with text "insufficient privileges" appeared


  Scenario: User fails to remove user from space without remove user privileges
    When user of space_owner_browser clicks "space3" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space3" in the sidebar
    And user of space_owner_browser clicks "user1" user in "space3" space members users list
    And user of space_owner_browser sees following privileges of "user1" user in space members subpage:
          User management:
            granted: False

    And user of browser_user1 clicks Members of "space3" in the sidebar
    And user of browser_user1 clicks "user1" user in "space3" space members users list
    And user of browser_user1 clicks show view expand button in space members subpage header
    And user of browser_user1 clicks memberships view mode in space members subpage
    And user of browser_user1 clicks "space-owner-user" user in "space3" space members users list
    And user of browser_user1 clicks on "space-owner-user" member relation menu button to "space3" space
    And user of browser_user1 clicks on "Remove relation" in space membership relation menu
    And user of browser_user1 clicks on "Remove" button in modal "REMOVE MEMBER"
    Then user of browser_user1 sees that error modal with text "insufficient privileges" appeared

