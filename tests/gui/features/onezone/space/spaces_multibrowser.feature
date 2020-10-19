Feature: Multi Browser basic management of spaces


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
            - user1
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


  Scenario: User successfully joins space using invitation token
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks on "Invite user using token" button in users list menu in "space1" space members view
    And user of space_owner_browser copies invitation token from modal
    And user of space_owner_browser sends invitation token to "browser1"
    And user of space_owner_browser closes "Invite using token" modal

    And user of browser1 joins group using received token
    Then user of browser1 sees that "space1" has appeared on the spaces list in the sidebar


  Scenario: User successfully joins space using invitation token (with Get started button)
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Members of "space1" in the sidebar
    And user of space_owner_browser clicks on "Invite user using token" button in users list menu in "space1" space members view
    And user of space_owner_browser copies invitation token from modal
    And user of space_owner_browser sends invitation token to "browser1"
    And user of space_owner_browser closes "Invite using token" modal

    And user of browser1 clicks join an existing space on Welcome page
    And user of browser1 pastes received token into token text field
    And user of browser1 clicks on Join button on consume token page
    Then user of browser1 sees that "space1" has appeared on the spaces list in the sidebar
