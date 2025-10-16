Feature: Basic management of space in Onezone using REST and Oneclient

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
    When using oneclient1, user1 sees spaces "[space1]" in mount point
    And using REST, user1 removes space named "space1" in "onezone" Onezone service
    Then using oneclient1, user1 sees spaces "[]" in mount point


  Scenario: User can see correct spaces in mount mount after adding support
    When using REST, user1 creates space "helloworld" in "onezone" Onezone service
    And using REST, user1 generates space support token for space named "helloworld" in "onezone" Onezone service and sends it to onepanel
    And using REST, onepanel supports "helloworld" space in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: posix
        size: 1000000
    Then using oneclient1, user1 sees spaces "[helloworld, space1]" in mount point


  Scenario: User can see correct spaces content after removing a space and creating a new one with the same name
    Given initial spaces configuration in "onezone" Onezone service:
        space3:
            owner: user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
    When using oneclient1, user1 sees spaces "[space1, space3]" in mount point
    And using REST, user1 removes space named "space3" in "onezone" Onezone service
    And using oneclient1, user1 sees spaces "[space1]" in mount point

    And using REST, user1 creates space "space3" in "onezone" Onezone service
    And using REST, user1 generates space support token for space named "space3" in "onezone" Onezone service and sends it to onepanel
    And using REST, onepanel supports "space3" space in "oneprovider-1" Oneprovider panel service with following configuration:
        storage: posix
        size: 1000000
    And using REST, user1 waits for space "space3" support in oneprovider-1
    And using REST, user1 succeeds to create file named "file1.txt" in "space3" in oneprovider-1
    And using REST, user1 writes "TEST TEXT" to file named "file1.txt" in "space3" in oneprovider-1

    Then using oneclient1, user1 sees spaces "[space1, space3]" in mount point
    And using oneclient1, user1 reads "TEST TEXT" from file named "file1.txt" in "space3" in oneprovider-1


  Scenario: User can see correct spaces in mount mount after removing support
    When using oneclient1, user1 sees spaces "[space1]" in mount point
    And using REST, admin removes support from provider "oneprovider-1" for space named "space1" in "onezone" Onezone service
    Then using oneclient1, user1 sees spaces "[]" in mount point
