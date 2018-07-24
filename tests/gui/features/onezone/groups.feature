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
    When user of browser clicks on the CREATE button in "groups" Onezone panel
    And user of browser writes "newgroup" into group name text field
    And user of browser confirms group name
    Then user of browser sees group "newgroup"


  Scenario: User renames group
    # create new group
    When user of browser clicks on the CREATE button in "groups" Onezone panel
    And user of browser writes "newgroup" into group name text field
    And user of browser confirms group name

    # rename group
    And user of browser clicks on RENAME button in "newgroup" group options menu
    
    










