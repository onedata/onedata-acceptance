Feature: Basic management of groups with one user in Onezone GUI


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial spaces configuration in "onezone" Onezone service:
          space1:
              owner: user1
              home space for:
                  - user1
              providers:
                  - oneprovider-1:
                      storage: posix
                      size: 1000000

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User creates group
    When user of browser clicks on the create button in "groups" Onezone panel
    And user of browser writes "newgroup" into group name text field
    And user of browser clicks on confirmation button

    Then user of browser do see group "newgroup" on groups list


  Scenario: User renames group
    # create new group
    When user of browser clicks on the create button in "groups" Onezone panel
    And user of browser writes "newgroup" into group name text field
    And user of browser clicks on confirmation button

    # rename group
    And user of browser clicks on "Rename" button in "newgroup" group menu
    And user of browser writes "newname" into rename group text field
    And user of browser confirms group rename  

    Then user of browser do see group "newname" on groups list
    And user of browser dont see group "newgroup" on groups list


  Scenario: User tries to create unnamed group
    When user of browser clicks on the create button in "groups" Onezone panel

    Then user of browser see that create group button is inactive 


  Scenario: User deletes group
    # create new group
    When user of browser clicks on the create button in "groups" Onezone panel
    And user of browser writes "group" into group name text field
    And user of browser clicks on confirmation button

    # delete group
    And user of browser clicks on "Remove" button in "group" group menu
    And user of browser clicks on "Remove" button in "REMOVE GROUP" modal

    Then user of browser dont see group "group" on groups list


  Scenario: User leaves group
    # create new group
    When user of browser clicks on the create button in "groups" Onezone panel
    And user of browser writes "group" into group name text field
    And user of browser clicks on confirmation button

    # leave group
    And user of browser clicks on "Leave" button in "group" group menu
    And user of browser clicks on "Leave" button in "LEAVE GROUP" modal

    Then user of browser dont see group "group" on groups list


  Scenario: User tries to join group using incorrect token
    When user of browser clicks on the join button in "groups" Onezone panel
    And user of browser writes "aaa" into group token text field
    And user of browser clicks on confirmation button
    
    Then user of browser see that error modal with "joining the group failed" text appeared


  Scenario: User adds subgroup  
    # create groups
    When user of browser creates "group1" group
    And user of browser creates "group2" group

    # get invitation token
    And user of browser clicks on "generate an invitation token" text in "group2" members groups list
    And user of browser copies generated token
    
    # join as subgroups
    And user of browser goes to "group1" parents subpage
    And user of browser pastes copied token into group token text field
    And user of browser clicks on confirmation button
    
    Then user of browser do see "group1" as "group2" child
    And user of browser do see "group2" as "group1" parent


  Scenario: User tries to add group as its subgroup
    # create group
    When user of browser creates "group" group
    
    # get invitation token
    And user of browser clicks on "generate an invitation token" text in "group" members groups list
    And user of browser copies generated token
    
    # join as subgroups
    And user of browser goes to "group" parents subpage
    And user of browser pastes copied token into group token text field
    And user of browser clicks on confirmation button

    Then user of browser see that error modal with "joining group as subgroup failed" text appeared


  Scenario: User tries to join group he already is in
    # create group
    When user of browser creates "group" group

    # get invitation token
    And user of browser gets "group" member invitation token

    # join group
    And user of browser clicks on the join button in "groups" Onezone panel
    And user of browser pastes copied token into group token text field
    And user of browser clicks on confirmation button

    Then user of browser see that error modal with "joining the group failed" text appeared


