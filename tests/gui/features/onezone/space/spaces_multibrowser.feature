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


    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, Onezone] page
    And users of [browser1, browser2] logged as [user1, user2] to [Onezone, Onezone] service


  Scenario Outline: User successfully joins space using invitation token
    When user of browser1 clicks "space1" on the spaces list in the sidebar
    And user of browser1 clicks Members of "space1" in the sidebar
    And user of browser1 clicks on "Invite user using token" button in users list menu in "space1" space members view
    And user of browser1 copies invitation token from modal
    And user of browser1 sends invitation token to "browser2"
    And user of browser1 closes "Invite using token" modal
    And user of browser2 clicks Join some space using a space invitation token button
    And user of browser2 pastes Space invitation token into space token text field on data page
    And user of browser2 confirms join the space using <confirmation_method> on data page
    Then user of browser2 sees that "space1" has appeared on the spaces list in the sidebar

    Examples:
      | confirmation_method |
      | enter               |
      | button              |


  Scenario: User successfully joins space using invitation token (with Get started button)
    When user of browser1 clicks "space1" on the spaces list in the sidebar
    And user of browser1 clicks Members of "space1" in the sidebar
    And user of browser1 clicks on "Invite user using token" button in users list menu in "space1" space members view
    And user of browser1 copies invitation token from modal
    And user of browser1 sends invitation token to "browser2"
    And user of browser1 closes "Invite using token" modal
    And user of browser2 clicks join an existing space on Welcome page
    And user of browser2 pastes Space invitation token into space token text field on data page
    And user of browser2 clicks Join the space button on Join user to a space page
    Then user of browser2 sees that "space1" has appeared on the spaces list in the sidebar
