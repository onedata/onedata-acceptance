Feature: Multi Browser invitation group to spaces


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
            - user1
    And initial groups configuration in "onezone" Onezone service:
          group2:
            owner: user1
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: space-owner-user
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000


    And users opened [space_owner_browser, browser1] browsers' windows
    And users of [space_owner_browser, browser1] opened [Onezone, Onezone] page
    And users of [space_owner_browser, browser1] logged as [space-owner-user, user1] to [Onezone, Onezone] service


  Scenario: User joins a space with group invitation token
    When user of space_owner_browser clicks on Data in the main menu
    And user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks "Members" of "space1" space in the sidebar
    And user of space_owner_browser clicks on "Invite group using token" button in groups list menu in "space1" space members view
    And user of space_owner_browser copies invitation token from modal
    And user of space_owner_browser closes "Invite using token" modal
    And user of space_owner_browser sends copied token to user of browser1

    And user of browser1 adds group "group2" to space using copied token

    Then user of browser1 sees that "space1" has appeared on the spaces list in the sidebar


  Scenario: User joins a space with group invitation token and see space was renamed
    # Space-owner-user invites user1 via group invitation
    When user of space_owner_browser clicks on Data in the main menu
    And user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks "Members" of "space1" space in the sidebar
    And user of space_owner_browser clicks on "Invite group using token" button in groups list menu in "space1" space members view
    And user of space_owner_browser copies invitation token from modal
    And user of space_owner_browser closes "Invite using token" modal
    And user of space_owner_browser sends copied token to user of browser1

    And user of browser1 adds group "group2" to space using copied token

    # Space-owner-user renames space
    And user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser writes "space2" into rename space text field
    And user of space_owner_browser clicks on confirmation button on overview page

    # User1 sees space has different name
    Then user of browser1 sees that "space1" has disappeared on the spaces list in the sidebar
    And user of browser1 sees that "space2" has appeared on the spaces list in the sidebar
