Feature: Multi Browser invitation group to spaces


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And initial groups configuration in "onezone" Onezone service:
          group2:
            owner: user2
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000


    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, Onezone] page
    And users of [browser1, browser2] logged as [user1, user2] to Onezone service


  Scenario Outline: User joins a space with group invitation token
    When user of browser1 clicks on Spaces in the main menu
    And user of browser1 clicks "space1" on the spaces list in the sidebar
    And user of browser1 clicks Members of "space1" in the sidebar
    And user of browser1 clicks Invite group on Menu of Members of Spaces
    And user of browser1 copies invitation token from Spaces page
    And user of browser1 sends copied token to user of browser2

    And user of browser2 clicks on Groups in the main menu
    And user of browser2 clicks "group2" on the groups list in the sidebar
    And user of browser2 clicks Join space on the groups list in the sidebar
    And user of browser2 pastes Space invitation token into space token text field
    And user of browser2 confirms join the space using <confirmation_method>
    Then user of browser2 sees that "space1" has appeared on the spaces list in the sidebar

    Examples:
      | confirmation_method |
      | enter               |
      | button              |


  Scenario: User fails to join a space with invalid group invitation token
    When user of browser2 clicks on Groups in the main menu
    And user of browser2 clicks "group2" on the groups list in the sidebar
    And user of browser2 clicks Join space on the groups list in the sidebar
    And user of browser2 writes "invalid token" into space token text field
    And user of browser2 clicks Join the space button on Join to a space page
    Then user of browser2 sees that error popup has appeared


  Scenario: User joins a space with group invitation token and see space was renamed
    # user1 invites user2 via group invitation
    When user of browser1 clicks on Spaces in the main menu
    And user of browser1 clicks "space1" on the spaces list in the sidebar
    And user of browser1 clicks Members of "space1" in the sidebar
    And user of browser1 clicks Invite group on Menu of Members of Spaces
    And user of browser1 copies invitation token from Spaces page
    And user of browser1 sends copied token to user of browser2

    And user of browser2 clicks on Groups in the main menu
    And user of browser2 clicks "group2" on the groups list in the sidebar
    And user of browser2 clicks Join space on the groups list in the sidebar
    And user of browser2 pastes Space invitation token into space token text field
    And user of browser2 clicks Join the space button on Join to a space page

    # user1 renames space
    And user of browser1 clicks "space1" on the spaces list in the sidebar
    And user of browser1 clicks Overview of "space1" in the sidebar
    And user of browser1 writes "space2" into rename space text field
    And user of browser1 clicks on confirmation button on overview page

    # user2 sees space has different name
    And user of browser2 refreshes site
    Then user of browser2 sees that "space1" has disappeared on the spaces list in the sidebar
    And user of browser2 sees that "space2" has appeared on the spaces list in the sidebar