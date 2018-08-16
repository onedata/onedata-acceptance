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
    And user of [browser1, browser2] opened [onezone, onezone] page
    And user of [browser1, browser2] logged as [user1, user2] to Onezone service


  Scenario: User renames group with more users usnig button to confirm
    When user of browser1 renames group "group1" to "group2" using button to confirm

    And user of browser1 refreshes site
    And user of browser2 refreshes site

    Then user of [browser1, browser2] sees group "group2" on groups list
    And user of [browser1, browser2] does not see group "group1" on groups list


  Scenario: User renames group with more users usnig enter to confirm
    When user of browser1 renames group "group1" to "group2" using enter to confirm

    And user of browser1 refreshes site
    And user of browser2 refreshes site

    Then user of [browser1, browser2] sees group "group2" on groups list
    And user of [browser1, browser2] does not see group "group1" on groups list


  Scenario: User removes group with more users 
    When user of browser1 removes group "group1" 

    And user of browser1 refreshes site
    And user of browser2 refreshes site

    Then user of [browser1, browser2] does not see group "group1" on groups list


  Scenario: Group owner leaves group
    When user of browser1 leaves group "group1"

    And user of browser1 refreshes site
    And user of browser2 refreshes site

    Then user of browser1 does not see group "group1" on groups list
    And user of browser2 sees group "group1" on groups list


  Scenario: User leaves group with more users
    When user of browser2 leaves group "group1"

    And user of browser1 refreshes site
    And user of browser2 refreshes site

    Then user of browser2 does not see group "group1" on groups list
    And user of browser1 sees group "group1" on groups list


  Scenario: User is removed from group
    When user of browser1 removes user "user2" from group "group1" members

    And user of browser1 refreshes site
    And user of browser2 refreshes site

    Then user of browser1 does not see user "user2" on group "group1" members list
    And user of browser2 does not see group "group1" on groups list 
 
