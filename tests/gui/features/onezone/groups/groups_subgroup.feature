Feature: Basic management of groups with multiple users in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
          group2:
            owner: user2
          group3:
            owner: user1
    And initial spaces configuration in "onezone" Onezone service:
          space1:
              owner: user1
              home space for:
                  - user1
              providers:
                  - oneprovider-1:
                      storage: posix
                      size: 1000000

    And users opened [browser1, browser2] browsers' windows
    And user of [browser1, browser2] opened [Onezone, Onezone] page
    And user of [browser1, browser2] logged as [user1, user2] to Onezone service


  Scenario Outline: Single user adds subgroup
    When user of browser1 clicks on button "Invite group using token" in group "group3" members menu
    And user of browser1 copies invitation token from modal
    And user of browser1 closes modal "Invite group using token"

    And user of browser1 clicks on button "Join as subgroup" in group "group1" menu
    And user of browser1 pastes copied token into group token text field
    And user of browser1 confirms using <confirmation_method>

    Then user of browser1 sees "group1" as "group3" child
#    And user of browser1 sees "group3" as "group1" parent

    Examples:
      | confirmation_method |
      | enter               |
      | button              |


  Scenario: User adds subgroup
    When user of browser1 copies group "group1" group invitation token
    And user of browser1 sends copied token to user of browser2
    And user of browser2 adds group "group2" as subgroup using received token

    Then users of [browser1, browser2] sees group "group1" on groups list
    And user of browser2 sees group "group2" on groups list
