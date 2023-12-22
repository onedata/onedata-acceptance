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
          group5:
            owner: user1
            users:
                - user2
            groups:
                - group4
          group6:
            owner: user1
          group7:
            owner: user2
            users:
                - user1
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: user1
            groups:
              - group4
          space2:
            owner: user1
            users:
                - user2
          space3:
            owner: user1
            groups:
              - group5

    And users opened [browser1, browser2] browsers' windows
    And user of [browser1, browser2] opened [Onezone, Onezone] page
    And user of [browser1, browser2] logged as [user1, user2] to [Onezone, Onezone] service


  Scenario: User removes relation between two groups (effective)
    When user of browser1 clicks "space1" on the spaces list in the sidebar
    And user of browser1 sees 1 direct, 4 effective groups and 1 direct, 2 effective users in space members tile

    And user of browser2 opens group "group2" members subpage
    And user of browser2 clicks "group1" group in "group2" group members groups list
    And user of browser2 sets following privileges for "group1" group in group members subpage:
          Group hierarchy management:
            granted: Partially
            privilege subtypes:
              Leave parent group: True

    And user of browser1 opens group "group4" members subpage
    And user of browser1 clicks effective view mode in group members subpage
    And user of browser1 clicks memberships view mode in group members subpage
    And user of browser1 clicks "user1" user in "group4" group members users list
    And user of browser1 sees 2 membership rows in group memberships mode

    And user of browser1 clicks on "group2" member relation menu button to "group3" group
    And user of browser1 clicks on "Remove relation" in group membership relation menu
    And user of browser1 clicks on "Remove" button in modal "REMOVE MEMBER"

    Then user of browser1 sees 1 membership row in group memberships mode
    And user of browser1 does not see that "group2" group is member of "group3" group in group memberships mode

    And user of browser1 clicks "space1" on the spaces list in the sidebar
    And user of browser1 sees 1 direct, 2 effective groups and 1 direct, 2 effective users in space members tile
    And user of browser2 clicks "space1" on the spaces list in the sidebar
    And user of browser2 sees 2 effective groups in space members tile


  Scenario: User successfully view group if he has group management privileges
    When user of browser1 opens group "group5" members subpage
    And user of browser1 clicks "user2" user in "group5" group members users list
    And user of browser1 sees privileges for "user2" user in group members subpage
    And user of browser1 clicks on "user2" users checkbox
    And user of browser1 clicks on bulk edit button
    And user of browser1 sets following privileges on modal:
          Group management:
            granted: True

    Then user of browser2 sees group "group5" on groups list


  Scenario: User fails to view group because of lack in privileges
    When user of browser1 opens group "group5" members subpage
    And user of browser1 clicks "user2" user in "group5" group members users list
    And user of browser1 sees privileges for "user2" user in group members subpage
    And user of browser1 clicks on "user2" users checkbox
    And user of browser1 clicks on bulk edit button
    And user of browser1 sets following privileges on modal:
          Group management:
            granted: False

    Then user of browser2 does not see group "group5" on groups list


  Scenario: User fails to rename group because of lack in privileges
    When user of browser1 opens group "group5" members subpage
    And user of browser1 clicks "user2" user in "group5" group members users list
    And user of browser1 sees privileges for "user2" user in group members subpage
    And user of browser1 clicks on "user2" users checkbox
    And user of browser1 clicks on bulk edit button
    And user of browser1 sets following privileges on modal:
          Group management:
            granted: Partially
            privilege subtypes:
              Modify group: False

    And user of browser2 clicks on "Rename" button in group "group5" menu in the sidebar
    And user of browser2 writes "group_renamed" into rename group text field
    And user of browser2 confirms group rename using confirmation button
    Then user of browser2 sees that error modal with text "insufficient privileges" appeared


  Scenario: User successfully sets privileges for other user if he has group management privileges
    When user of browser1 opens group "group5" members subpage
    And user of browser1 clicks "user2" user in "group5" group members users list
    And user of browser1 sees privileges for "user2" user in group members subpage
    And user of browser1 clicks on "user2" users checkbox
    And user of browser1 clicks on bulk edit button
    And user of browser1 sets following privileges on modal:
          Group management:
            granted: Partially
            privilege subtypes:
              View privileges: True
              Set privileges: True

    And user of browser2 opens group "group5" members subpage
    And user of browser2 clicks "user1" user in "group5" group members users list
    And user of browser2 sees privileges for "user1" user in group members subpage
    And user of browser2 clicks on "user1" users checkbox
    And user of browser2 clicks on bulk edit button
    And user of browser2 sets following privileges on modal:
          Group management:
            granted: Partially
            privilege subtypes:
              View privileges: False
              Set privileges: False

    Then user of browser2 sees following privileges of "user1" user in group members subpage:
          Group management:
            granted: Partially
            privilege subtypes:
              View privileges: False
              Set privileges: False


  Scenario: User fails to set privileges for other users because of lack in privileges
    When user of browser1 opens group "group5" members subpage
    And user of browser1 clicks "user2" user in "group5" group members users list
    And user of browser1 sees privileges for "user2" user in group members subpage
    And user of browser1 clicks on "user2" users checkbox
    And user of browser1 clicks on bulk edit button
    And user of browser1 sets following privileges on modal:
          Group management:
            granted: Partially
            privilege subtypes:
              View privileges: True
              Set privileges: False

    And user of browser2 opens group "group5" members subpage
    And user of browser2 clicks "user1" user in "group5" group members users list
    And user of browser2 sees privileges for "user1" user in group members subpage
    And user of browser2 clicks on "user1" users checkbox
    And user of browser2 clicks on bulk edit button
    And user of browser2 sets following privileges on modal:
          Group management:
            granted: Partially
            privilege subtypes:
              View privileges: False
              Set privileges: False

    Then user of browser2 sees that error modal with text "insufficient privileges" appeared


  Scenario: User fails to remove group because of lack in privileges
    When user of browser1 opens group "group5" members subpage
    And user of browser1 clicks "user2" user in "group5" group members users list
    And user of browser1 sees privileges for "user2" user in group members subpage
    And user of browser1 clicks on "user2" users checkbox
    And user of browser1 clicks on bulk edit button
    And user of browser1 sets following privileges on modal:
          Group management:
            granted: False

    And user of browser2 clicks on "Remove" button in group "group5" menu in the sidebar
    And user of browser2 clicks on "Remove" button in modal "REMOVE GROUP"
    Then user of browser2 sees that error modal with text "insufficient privileges" appeared


  Scenario: User fails to invite other user to join given group because of lack in privileges
    When user of browser1 opens group "group5" members subpage
    And user of browser1 clicks "user2" user in "group5" group members users list
    And user of browser1 sees privileges for "user2" user in group members subpage
    And user of browser1 clicks on "user2" users checkbox
    And user of browser1 clicks on bulk edit button
    And user of browser1 sets following privileges on modal:
          User management:
            granted: Partially
            privilege subtypes:
              Add user: False

    And user of browser2 opens group "group5" members subpage
    And user of browser2 clicks on "Invite user using token" button in users list menu in "group5" group members view
    Then user of browser2 sees This resource could not be loaded alert in "Invite using token" modal


  Scenario: User successfully removes other user from given group if he has remove user privileges
    When user of browser2 opens group "group7" members subpage
    And user of browser2 clicks "user2" user in "group7" group members users list
    And user of browser2 sees privileges for "user2" user in group members subpage
    And user of browser2 clicks on "user2" users checkbox
    And user of browser2 clicks on bulk edit button
    And user of browser2 sets following privileges on modal:
          User management:
            granted: Partially
            privilege subtypes:
              Remove user: True

    And user of browser2 opens group "group7" members subpage
    And user of browser2 removes "user1" user from "group7" group members
    Then user of browser1 does not see group "group7" on groups list


  Scenario: User fails to invite created group as subgroup because of lack in privileges
    When user of browser1 opens group "group5" members subpage
    And user of browser1 clicks "user2" user in "group5" group members users list
    And user of browser1 sees privileges for "user2" user in group members subpage
    And user of browser1 clicks on "user2" users checkbox
    And user of browser1 clicks on bulk edit button
    And user of browser1 sets following privileges on modal:
          Group hierarchy management:
            granted: Partially
            privilege subtypes:
              Add child group: False

    And user of browser2 opens group "group5" hierarchy subpage
    And user of browser2 clicks on group "group5" menu button in hierarchy subpage
    And user of browser2 clicks on "Add child group" in group hierarchy menu
    And user of browser2 clicks on "Create new group" in group hierarchy menu
    And user of browser2 writes "child_group" into group name text field in create group modal
    And user of browser2 clicks on "Create" button in modal "CREATE GROUP"
    Then user of browser2 sees that error modal with text "Child group creation failed" appeared


  Scenario: User fails to join group to space because of lack in privileges
    When user of browser1 opens group "group5" members subpage
    And user of browser1 clicks "user2" user in "group5" group members users list
    And user of browser1 sees privileges for "user2" user in group members subpage
    And user of browser1 clicks on "user2" users checkbox
    And user of browser1 clicks on bulk edit button
    And user of browser1 sets following privileges on modal:
          Space management:
            granted: False

    And user of browser2 clicks "space1" on the spaces list in the sidebar
    And user of browser2 clicks "Members" of "space1" space in the sidebar
    And user of browser2 clicks on "Invite group using token" button in groups list menu in "space1" space members view
    Then user of browser2 sees This resource could not be loaded alert in "Invite using token" modal


  Scenario: User creates new space and invites group to it but given group fails to control it because of lack in privileges
    When user of browser2 creates space "new_space"
    And user of browser2 clicks on Data in the main menu
    And user of browser2 clicks "new_space" on the spaces list in the sidebar
    And user of browser2 clicks "Members" of "new_space" space in the sidebar
    And user of browser2 clicks on "Invite group using token" button in groups list menu in "new_space" space members view
    And user of browser2 copies invitation token from modal
    And user of browser2 closes "Invite using token" modal
    And user of browser2 sends copied token to user of browser1

    And user of browser1 adds group "group6" to space using copied token
    And user of browser1 clicks "new_space" on the spaces list in the sidebar
    And user of browser1 clicks "Members" of "new_space" space in the sidebar

    And user of browser2 clicks on Data in the main menu
    And user of browser2 clicks "new_space" on the spaces list in the sidebar
    And user of browser2 clicks "Members" of "new_space" space in the sidebar
    And user of browser2 clicks "group6" group in "new_space" space members groups list
    And user of browser2 sees privileges for "group6" group in space members subpage
          Group management:
            granted: False

    # User tries to invite group using token
    And user of browser1 clicks on "Invite group using token" button in groups list menu in "new_space" space members view
    Then user of browser1 sees This resource could not be loaded alert in "Invite using token" modal
    And user of browser1 closes "Invite using token" modal

    # User tries to add group through dropdown menu
    And user of browser1 adds "group1" group to "new_space" space using available groups dropdown
    And user of browser1 sees that error modal with text "insufficient privileges" appeared


  Scenario: User fails to leave group from space because of lack in privileges
    When user of browser1 opens group "group5" members subpage
    And user of browser1 clicks "user2" user in "group5" group members users list
    And user of browser1 sees privileges for "user2" user in group members subpage
    And user of browser1 clicks on "user2" users checkbox
    And user of browser1 clicks on bulk edit button
    And user of browser1 sets following privileges on modal:
          Space management:
            granted: False

    And user of browser2 clicks "space1" on the spaces list in the sidebar
    And user of browser2 clicks on "Leave" button in space "space1" menu
    Then user of browser2 sees You cannot leave space alert in "leave modal" modal


  Scenario: User fails to join as subgroup because of lack in privileges
    When user of browser2 opens group "group7" members subpage
    And user of browser2 clicks "user2" user in "group7" group members users list
    And user of browser2 sees privileges for "user2" user in group members subpage
    And user of browser2 clicks on "user2" users checkbox
    And user of browser2 clicks on bulk edit button
    And user of browser2 sets following privileges on modal:
          Group hierarchy management:
            granted: Partially
            privilege subtypes:
              Add parent group: False

    And user of browser1 opens group "group6" members subpage
    And user of browser1 clicks on "Invite group using token" button in groups list menu in "group1" group members view
    And user of browser1 copies invitation token from modal
    And user of browser1 closes "Invite using token" modal

    And user of browser2 adds group "group7" as subgroup using copied token
    Then user of browser2 sees that error modal with text "insufficient privileges" appeared


  Scenario: User successfully removes subgroup if he has remove child group privileges
    When user of browser1 opens group "group5" members subpage
    And user of browser1 clicks "user2" user in "group5" group members users list
    And user of browser1 sees privileges for "user2" user in group members subpage
    And user of browser1 clicks on "user2" users checkbox
    And user of browser1 clicks on bulk edit button
    And user of browser1 sets following privileges on modal:
          Group hierarchy management:
            granted: Partially
            privilege subtypes:
              Remove child group: True

    And user of browser2 opens group "group5" hierarchy subpage
    And user of browser2 clicks on group "group4" menu button to parent relation in hierarchy subpage
    And user of browser2 clicks on "Remove relation" in relation menu
    And user of browser2 clicks on "Remove" button in modal "REMOVE MEMBER"
    Then user of browser2 does not see "base_group" as a child of "parent_group" in hierarchy subpage


  Scenario: User successfully leaves group and cannot view previously accessed space
    When user of browser2 clicks "space3" on the spaces list in the sidebar
    And user of browser2 sees "space3" label on overview page

    And user of browser1 opens group "group5" members subpage
    And user of browser1 clicks "user2" user in "group5" group members users list
    And user of browser1 sees privileges for "user2" user in group members subpage
    And user of browser1 clicks on "user2" users checkbox
    And user of browser1 clicks on bulk edit button
    And user of browser1 sets following privileges on modal:
          Group management:
            granted: True
          Group hierarchy management:
            granted: True

    And user of browser2 leaves group "group5"
    Then user of browser2 sees that "space3" has disappeared on the spaces list in the sidebar
