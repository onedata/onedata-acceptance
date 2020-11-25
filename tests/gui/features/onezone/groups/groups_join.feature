Feature: Joining a group in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
            - user1
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
          space1:
              owner: space-owner-user
              home space for:
                  - space-owner-user
              groups:
                  - group1
              providers:
                  - oneprovider-1:
                      storage: posix
                      size: 1000000

    And users opened [space_owner_browser, browser1] browsers' windows
    And user of [space_owner_browser, browser1] opened [Onezone, Onezone] page
    And user of [space_owner_browser, browser1] logged as [space-owner-user, user1] to [Onezone, Onezone] service


  Scenario: User joins group using invitation token
    When user of space_owner_browser clicks on Groups in the main menu
    And user of space_owner_browser clicks "group1" on the groups list in the sidebar
    And user of space_owner_browser clicks on "Invite user using token" button in users list menu in "group1" group members view
    And user of space_owner_browser copies invitation token from modal
    And user of space_owner_browser closes "Invite using token" modal
    And user of space_owner_browser sends copied token to user of browser1

    And user of browser1 joins group using received token

    Then user of space_owner_browser sees "user1" user on "group1" group members list
    And user of browser1 sees group "group1" on groups list

    And user of browser1 clicks "space1" on the spaces list in the sidebar
    And user of browser1 sees 1 direct, 1 effective groups and 1 direct, 2 effective users in space members tile


  Scenario: User fails to join group he already belongs to
    When user of space_owner_browser clicks on Groups in the main menu
    And user of space_owner_browser clicks "group1" on the groups list in the sidebar
    And user of space_owner_browser clicks on "Invite user using token" button in users list menu in "group1" group members view
    And user of space_owner_browser copies invitation token from modal
    And user of space_owner_browser closes "Invite using token" modal

    And user of space_owner_browser joins group using copied token

    Then user of space_owner_browser sees that error modal with text "Consuming token failed" appeared


  Scenario: User fails to view group they do not belong to
    When user of space_owner_browser clicks on Groups in the main menu
    And user of space_owner_browser opens group "group1" main subpage
    And user of space_owner_browser copies a first resource ID from URL
    And user of space_owner_browser sends copied ID to user of browser1
    And user of browser1 changes webapp path to "/i#/onedata/groups" concatenated with received ID
    And user of browser1 refreshes site
    Then user of browser1 sees "YOU DON’T HAVE ACCESS TO THIS RESOURCE" error on groups page


  Scenario: User sees incrementatation of effective users and groups on space overview after a subgroup is added
    When user of browser1 creates group "group2"
    And user of space_owner_browser opens group "group1" members subpage
    And user of space_owner_browser clicks on "Invite group using token" button in groups list menu in "group1" group members view
    And user of space_owner_browser copies invitation token from modal
    And user of space_owner_browser closes "Invite using token" modal

    And user of space_owner_browser sends copied token to user of browser1
    And user of browser1 adds group "group2" as subgroup using copied token

    And user of browser1 clicks "space1" on the spaces list in the sidebar
    Then user of browser1 sees 1 direct, 2 effective groups and 1 direct, 2 effective users in space members tile

