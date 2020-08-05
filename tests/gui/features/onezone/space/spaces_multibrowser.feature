Feature: Multi Browser basic management of spaces


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And initial spaces configuration in "onezone" Onezone service:
          space1:
              owner: user1
              providers:
                  - oneprovider-1:
                      storage: posix
                      size: 1000000
          space2:
              owner: user1
              users:
                - user2


    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, Onezone] page
    And users of [browser1, browser2] logged as [user1, user2] to [Onezone, Onezone] service


  Scenario: User successfully joins space using invitation token
    When user of browser1 clicks "space1" on the spaces list in the sidebar
    And user of browser1 clicks Members of "space1" in the sidebar
    And user of browser1 clicks on "Invite user using token" button in users list menu in "space1" space members view
    And user of browser1 copies invitation token from modal
    And user of browser1 sends invitation token to "browser2"
    And user of browser1 closes "Invite using token" modal

    And user of browser2 joins group using received token
    Then user of browser2 sees that "space1" has appeared on the spaces list in the sidebar


  Scenario: User successfully joins space using invitation token (with Get started button)
    When user of browser1 clicks "space1" on the spaces list in the sidebar
    And user of browser1 clicks Members of "space1" in the sidebar
    And user of browser1 clicks on "Invite user using token" button in users list menu in "space1" space members view
    And user of browser1 copies invitation token from modal
    And user of browser1 sends invitation token to "browser2"
    And user of browser1 closes "Invite using token" modal

    And user of browser2 clicks join an existing space on Welcome page
    And user of browser2 pastes received token into token text field
    And user of browser2 clicks on Join button on consume token page
    Then user of browser2 sees that "space1" has appeared on the spaces list in the sidebar


  Scenario: User makes another user an owner and leaves space
    When user of browser1 clicks "space2" on the spaces list in the sidebar
    And user of browser1 clicks Members of "space2" in the sidebar
    And user of browser1 sees [Remove this member,Remove ownership] are disabled for "user1" user in users list
    And user of browser1 clicks "Make an owner" for "user2" user in users list
    And user of browser1 clicks "Remove ownership" for "user1" user in users list
    And user of browser1 clicks "Remove this member" for "user1" user in users list

