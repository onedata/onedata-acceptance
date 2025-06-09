Feature: Basic operations on the special user root directory which is
  user's home onedata directory, parent directory of all user's spaces.
  Using REST API and oneclient.

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


  Scenario: User fails to remove the user root directory using file path
    When using REST, user1 gets ID of the user root directory from the space "space1" details in oneprovider-1
    Then using oneclient1, user1 fails to remove the user root directory using file path in oneprovider-1


  Scenario: User fails to move the user root directory using file path
    When using REST, user1 gets ID of the user root directory from the space "space1" details in oneprovider-1
    Then using oneclient1, user1 fails to move the user root directory using file path in oneprovider-1


  Scenario: User fails to create file in the user root directory using file path
    When using REST, user1 gets ID of the user root directory from the space "space1" details in oneprovider-1
    Then using oneclient1, user1 fails to create file "some_name.txt" in the user root directory using file path in oneprovider-1
