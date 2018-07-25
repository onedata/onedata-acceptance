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
    And user of browser confirms group name
    And user of browser do see group "newgroup" on groups list
   

  Scenario: User creates and renames group
    # create new group
    When user of browser clicks on the create button in "groups" Onezone panel
    And user of browser writes "newgroup" into group name text field
    And user of browser confirms group name

    # rename group
    And user of browser clicks on "newgroup" group menu button
    And user of browser clicks on rename button in active menu
    And user of browser writes "newname" into rename group text field
    And user of browser confirms group rename
    
    Then user of browser do see group "newname" on groups list
    And user of browser dont see group "newgroup" on groups list


#  Scenario: User joins group
    #TODO


#  Scenario: User tries to join nonexisting group
    #TODO


#  Scenario: User tries to create unnamed group
#    When user of browser clicks on the create button in "groups" Onezone panel
#    And user of browser 
    
    










