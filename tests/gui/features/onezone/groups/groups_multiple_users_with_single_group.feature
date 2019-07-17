Feature: Basic management of groups with multiple users in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
            users:
                - user2
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
    And user of [browser1, browser2] logged as [user1, user2] to [Onezone, Onezone] service


  Scenario Outline: User renames group with others users
    When user of browser1 renames group "group1" to "group2" using <confirmation_method> to confirm
    Then users of [browser1, browser2] sees group "group2" on groups list
    And users of [browser1, browser2] does not see group "group1" on groups list

    Examples:
      | confirmation_method |
      | enter               |
      | button              |


  Scenario: User removes group with others users
    When user of browser1 removes group "group1"
    Then users of [browser1, browser2] does not see group "group1" on groups list


  Scenario: Group owner leaves group
    When user of browser1 leaves group "group1"
    Then user of browser1 does not see group "group1" on groups list
    And user of browser2 sees group "group1" on groups list


  Scenario: User leaves group with others users
    When user of browser2 leaves group "group1"
    Then user of browser2 does not see group "group1" on groups list
    And user of browser1 sees group "group1" on groups list


  Scenario: User is removed from group
    When user of browser1 goes to group "group1" members subpage
    And user of browser1 removes "user2" user from "group1" group members
    Then user of browser1 does not see "user2" user on "group1" group members list
    And user of browser2 does not see group "group1" on groups list

