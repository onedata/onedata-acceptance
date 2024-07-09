Feature: Basic management
  Basic management of space in Onezone using GUI and REST API

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
    And opened browser with user1 signed in to "onezone" service


  Scenario: User fails to remove space root dir
    When using REST, user1 gets root dir ID of space "space1" in oneprovider-1
    Then using REST, user1 fails to remove root dir of space "space1" in oneprovider-1


  Scenario: Admin user fails to remove space root dir
    When using REST, user1 gets root dir ID of space "space1" in oneprovider-1
    Then using REST, admin fails to remove root dir of space "space1" in oneprovider-1, because user is not space owner

#
#  TODO VFS- uncomment after enabling setting attrs using rest
#  Scenario Outline: User fails to set attribute
#    When using REST, user1 gets root dir ID of space "space1" in oneprovider-1
#    Then using REST, user1 fails to set "<attr_type>" attribute into "<attr_val>" of root dir of "space1" in oneprovider-1
#
#    Examples:
#    | attr_type | attr_val  |
#    | name      | some_name |


  Scenario: User fails to create file in space root dir
    When using REST, user1 gets root dir ID of space "space1" in oneprovider-1
    Then using REST, user1 fails to create file "some_name.txt" in root dir of "space1" in oneprovider-1
