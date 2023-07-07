Feature: Multi Browser basic management of spaces ownership


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
            - user1
    And initial groups configuration in "onezone" Onezone service:
      group1:
          owner: user1
    And initial spaces configuration in "onezone" Onezone service:
          space1:
              owner: space-owner-user
              users:
                - user1
          space2:
              owner: space-owner-user
              groups:
                - group1


    And users opened [space_owner_browser, browser1] browsers' windows
    And users of [space_owner_browser, browser1] opened [Onezone, Onezone] page
    And users of [space_owner_browser, browser1] logged as [space-owner-user, user1] to [Onezone, Onezone] service


  Scenario: User can resign space ownership if there is another space owner
    When user of space_owner_browser clicks "Members" of "space1" space in the sidebar
    And user of space_owner_browser sees [Remove ownership, Remove this member] are disabled for "space-owner-user" user in users list
    And user of space_owner_browser clicks "Make an owner" for "user1" user in users list
    And user of space_owner_browser clicks "Remove ownership" for "space-owner-user" user in users list
    Then user of space_owner_browser sees [you] status labels for "space-owner-user" user in space members subpage


  Scenario: User can be revoked of ownership by another space owner
    When user of browser1 clicks "Members" of "space1" space in the sidebar
    And user of browser1 sees [Remove ownership, Remove this member] are disabled for "space-owner-user" user in users list
    And user of space_owner_browser clicks "Members" of "space1" space in the sidebar
    And user of space_owner_browser clicks "Make an owner" for "user1" user in users list
    And user of browser1 clicks "Remove ownership" for "space-owner-user" user in users list
    Then user of space_owner_browser sees [you] status label for "space-owner-user" user in space members subpage


  Scenario: User can leave space after passing ownership to another user
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks on "Leave" button in space "space1" menu
    And user of space_owner_browser clicks on Leave button
    And user of space_owner_browser sees that error modal with text "Leaving space failed!" appeared
    And user of space_owner_browser clicks on "Close" button in modal "Error"

    And user of space_owner_browser clicks "Members" of "space1" space in the sidebar
    And user of space_owner_browser sees [Remove this member, Remove ownership] are disabled for "space-owner-user" user in users list
    And user of browser1 clicks "Members" of "space1" space in the sidebar
    And user of browser1 sees [Remove this member, Remove ownership] are disabled for "space-owner-user" user in users list

    And user of space_owner_browser clicks "Make an owner" for "user1" user in users list
    And user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks on "Leave" button in space "space1" menu
    And user of space_owner_browser clicks on Leave button

    Then user of space_owner_browser sees that "space1" has disappeared on the spaces list in the sidebar
    And user of browser1 does not see "space-owner-user" user on "space1" space members list


  Scenario: Effective user who gets ownership becomes direct user
    When user of space_owner_browser clicks "Members" of "space2" space in the sidebar
    And user of space_owner_browser clicks effective view mode in space members subpage

    And user of space_owner_browser clicks "Make an owner" for "user1" user in users list

    And user of browser1 clicks "Members" of "space2" space in the sidebar
    And user of browser1 clicks effective view mode in space members subpage

    Then user of browser1 sees [you, owner, direct] status labels for "user1" user in space members subpage


  Scenario: Space creator becomes owner of space
    When user of space_owner_browser creates "space3" space in Onezone
    And user of space_owner_browser clicks "Members" of "space3" space in the sidebar
    Then user of space_owner_browser sees [you, owner] status labels for "space-owner-user" user in space members subpage


  Scenario: User who is not space owner can remove himself from space
    When user of space_owner_browser clicks "Members" of "space1" space in the sidebar
    And user of browser1 clicks "Members" of "space1" space in the sidebar
    And user of browser1 removes "user1" user from "space1" space members
    Then user of browser1 sees that "space1" has disappeared on the spaces list in the sidebar
    And user of space_owner_browser does not see "user1" user on "space1" space members list


  Scenario: Space deleted by space owner disappears from other space user list
    When user of browser1 sees that "space1" has appeared on the spaces list in the sidebar
    And user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks on "Remove" button in space "space1" menu
    And user of space_owner_browser clicks on understand notice checkbox in "Remove space" modal
    And user of space_owner_browser clicks on "Remove" button in "Remove space" modal
    And user of space_owner_browser sees that "space1" has disappeared on the spaces list in the sidebar
    Then user of browser1 sees that "space1" has disappeared on the spaces list in the sidebar