Feature: Basic management of groups with multiple users in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And initial groups configuration in "onezone" Onezone service:
          group1:
            owner: user1
            groups:
                - group2
          group2:
            owner: user2
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


  Scenario: Group leaves parent group
    When user of browser2 removes group "group1" from group "group2" parents list

    And user of browser1 refreshes site
    And user of browser2 refreshes site

    Then user of browser1 does not see "group2" as "group1" child
    And user of browser2 does not see "group1" as "group2" parent

 
  Scenario: Parent group is removed
    When user of browser1 removes group "group1"

    And user of browser1 refreshes site
    And user of browser2 refreshes site

    Then user of browser1 does not see group "group1" on groups list
    And user of browser2 sees group "group2" on groups list
    And user of browser2 does not see group "group1" on groups list    


  Scenario: Child group is removed from childen list
    When user of browser1 removes group "group2" from group "group1" members

    And user of browser1 refreshes site
    And user of browser2 refreshes site

    Then user of browser1 does not see "group2" as "group1" child
    And user of browser2 does not see "group1" as "group2" parent


  Scenario: Child group is removed
    When user of browser2 removes group "group2"

    And user of browser1 refreshes site
    And user of browser2 refreshes site

    Then user of browser2 does not see group "group2" on groups list
    And user of browser1 does not see "group2" as "group1" child


