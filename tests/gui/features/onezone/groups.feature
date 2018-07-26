Feature: Basic management of groups in Onezone GUI


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
   

  Scenario: User creates and renames group
    # create new group
    When user of browser clicks on the create button in "groups" Onezone panel
    And user of browser writes "newgroup" into group name text field
    And user of browser clicks on confirmation button

    # rename group
    And user of browser clicks on rename button in "newgroup" group menu
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
    And user of browser clicks on remove button in "group" group menu
    And user of browser clicks on "Remove" button in "REMOVE GROUP" modal
	
    Then user of browser dont see group "group" on groups list

  Scenario: User leaves group
    # create new group
    When user of browser clicks on the create button in "groups" Onezone panel
    And user of browser writes "group" into group name text field
    And user of browser clicks on confirmation button

    # leave group
    And user of browser clicks on leave button in "group" group menu
    And user of browser clicks on "Leave" button in "LEAVE GROUP" modal
	
    Then user of browser dont see group "group" on groups list


  Scenario: User tries to join group using incorrect token
    When user of browser clicks on the join button in "groups" Onezone panel
    And user of browser writes "aaa" into group token text field
    And user of browser clicks on confirmation button
    
    Then user of browser see that error modal with "joining the group failed" text appeared



    
    










