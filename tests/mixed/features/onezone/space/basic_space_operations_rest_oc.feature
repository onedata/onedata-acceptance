Feature: Basic management
  Basic management of space in Onezone using REST and Oneclient

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
    And oneclient mounted using token by user1


  Scenario: User can see correct spaces in mount mount after renaming one space
    When using REST, user1 renames space named "space1" to "space2" in "onezone" Onezone service
    Then using oneclient1, user1 sees spaces "[space2]" in mount point


  Scenario: User can see correct spaces in mount mount after removing one space
    When using REST, user1 removes space named "space1" in "onezone" Onezone service
    Then using oneclient1, user1 sees spaces "[]" in mount point


  Scenario: User can see correct spaces in mount mount after adding support
    When using REST, user1 creates space "helloworld" in "onezone" Onezone service
    And using REST, user1 generates space support token for space named "helloworld" in "onezone" Onezone service and sends it to onepanel
    And using REST, onepanel supports "helloworld" space in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: posix
        size: 1000000
    Then using oneclient1, user1 sees spaces "[helloworld, space1]" in mount point


  Scenario: User can see correct spaces in mount mount after removing support
    When using REST, admin removes support from provider "oneprovider-1" for space named "space1" in "onezone" Onezone service
    Then using oneclient1, user1 sees spaces "[]" in mount point
