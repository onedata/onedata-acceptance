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
    And user of [browser1, browser2] opened [onezone, onezone] page
    And user of [browser1, browser2] logged as [user1, user2] to Onezone service


  Scenario: Single user adds subgroup using button to confirm
    When user of browser1 clicks on button "Invite group" in group "group3" members menu
    And user of browser1 copies generated token
    
    And user of browser1 goes to group "group1" parents subpage
    And user of browser1 pastes copied token into group token text field
    And user of browser1 clicks on confirmation button

    And user of browser1 refreshes site
    
    Then user of browser1 sees "group1" as "group3" child
    And user of browser1 sees "group3" as "group1" parent


  Scenario: Single user adds subgroup using enter to confirm
    When user of browser1 clicks on button "Invite group" in group "group3" members menu
    And user of browser1 copies generated token
    
    And user of browser1 goes to group "group1" parents subpage
    And user of browser1 pastes copied token into group token text field
    And user of browser1 presses enter on keyboard

    And user of browser1 refreshes site
    
    Then user of browser1 sees "group1" as "group3" child
    And user of browser1 sees "group3" as "group1" parent


  Scenario: User adds subgroup
    When user of browser1 copies group "group1" group invitation token
    And user of browser1 sends copied token to user of browser2
    And user of browser2 adds group "group2" as subgroup using received token

    And user of browser1 refreshes site
    And user of browser2 refreshes site

    Then user of [browser1, browser2] sees group "group1" on groups list
    And user of browser2 sees group "group2" on groups list 




