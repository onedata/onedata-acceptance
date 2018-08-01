Feature: Basic management of groups with multiple users in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And initial groups configuration in "onezone" Onezone service:
          group:
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
    And user of [browser1, browser2] opened [onezone, onezone] page
    And user of [browser1, browser2] logged as [user1, user2] to Onezone service


  Scenario: User joins group
    When user of browser1 gets "group" user invitation token
    And user of browser1 sends token to user of browser2

    And user of browser2 joins group using received token

    And user of browser1 refreshes site
    And user of browser2 refreshes site

    Then user of browser1 do see user "user2" on group "group" members list
    And user of browser2 do see group "group" on groups list


  Scenario: User renames group
    When user of browser1 gets "group" user invitation token
    And user of browser1 sends token to user of browser2

    And user of browser2 joins group using received token

    And user of browser1 renames group "group" to "newgroup"

    And user of browser1 refreshes site
    And user of browser2 refreshes site

    Then user of [browser1, browser2] do see group "newgroup" on groups list
    And user of [browser1, browser2] dont see group "group" on groups list


  Scenario: User adds subgroup
    When user of browser2 creates "child" group
   
    And user of browser1 gets "group" group invitation token
    And user of browser1 sends token to user of browser2
    And user of browser2 adds "child" group as subgroup using received token

    Then user of [browser1, browser2] do see group "group" on groups list
    And user of browser2 do see group "child" on groups list 


  Scenario: User removes group
    When user of browser1 gets "group" user invitation token
    And user of browser1 sends token to user of browser2

    And user of browser2 joins group using received token
    
    When user of browser1 removes "group" group

    And user of browser1 refreshes site
    And user of browser2 refreshes site

    Then user of [browser1, browser2] dont see group "group" on groups list


  Scenario: Group owner leaves group
    When user of browser1 gets "group" user invitation token
    And user of browser1 sends token to user of browser2

    And user of browser2 joins group using received token

    When user of browser1 leaves "group" group

    Then user of browser1 dont see group "group" on groups list
    And user of browser2 do see group "group" on groups list


  Scenario: User leaves group
    When user of browser1 gets "group" user invitation token
    And user of browser1 sends token to user of browser2

    And user of browser2 joins group using received token

    When user of browser2 leaves "group" group

    And user of browser1 refreshes site
    And user of browser2 refreshes site

    Then user of browser2 dont see group "group" on groups list
    And user of browser1 do see group "group" on groups list


  Scenario: User is removed from group
    When user of browser1 gets "group" user invitation token
    And user of browser1 sends token to user of browser2

    And user of browser2 joins group using received token
    
    And user of browser1 refreshes site

    And user of browser1 removes "user2" user from group "group" members

    And user of browser1 refreshes site
    And user of browser2 refreshes site

    Then user of browser1 dont see user "user2" on group "group" members list
    And user of browser2 dont see group "group" on groups list


  Scenario: Group leaves parent group
    When user of browser2 creates "child" group
   
    And user of browser1 gets "group" group invitation token
    And user of browser1 sends token to user of browser2
    And user of browser2 adds "child" group as subgroup using received token

    And user of browser2 removes group "group" from group "child" parents list

    Then user of browser1 dont see "child" as "group" child
    And user of browser2 dont see "group" as "child" parent

 
  Scenario: Parent group is removed
    When user of browser2 creates "child" group
   
    And user of browser1 gets "group" group invitation token
    And user of browser1 sends token to user of browser2
    And user of browser2 adds "child" group as subgroup using received token

    And user of browser1 removes "group" group

    And user of browser1 refreshes site
    And user of browser2 refreshes site

    Then user of browser1 dont see group "group" on groups list
    And user of browser2 do see group "child" on groups list
    And user of browser2 dont see group "group" on groups list    


  Scenario: Child group is removed from childen list
    When user of browser2 creates "child" group
    
    And user of browser1 gets "group" group invitation token
    And user of browser1 sends token to user of browser2
    And user of browser2 adds "child" group as subgroup using received token

    And user of browser1 refreshes site
    
    And user of browser1 removes "child" group from group "group" members

    And user of browser1 refreshes site
    And user of browser2 refreshes site

    Then user of browser1 dont see "child" as "group" child
    And user of browser2 dont see "group" as "child" parent


  Scenario: Child group is removed
    When user of browser2 creates "child" group
    
    And user of browser1 gets "group" group invitation token
    And user of browser1 sends token to user of browser2
    And user of browser2 adds "child" group as subgroup using received token

    And user of browser2 removes "child" group

    And user of browser1 refreshes site
    And user of browser2 refreshes site

    Then user of browser2 dont see group "child" on groups list
    And user of browser1 dont see "child" as "group" parent


