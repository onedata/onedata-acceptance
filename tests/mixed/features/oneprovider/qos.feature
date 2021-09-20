Feature: Quality of Service mixed tests

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
        storage:
          defaults:
            provider: oneprovider-1
          directory tree:
            - file1

  And opened browser with user1 signed in to "onezone" service


  Scenario Outline: User adds QoS requirements to file using <client1> and using <client2> sees QoS file status
    When using <client1>, user1 creates "anyStorage" QoS requirement for "file1" in space "space1" in oneprovider-1
    Then using <client2>, user1 sees that file "file1" has some QoS requirements in space "space1" in oneprovider-1

  Examples:
  | client1    | client2    |
  | REST       | web GUI    |
  | web GUI    | REST       |


  Scenario Outline: User deletes QoS requirements to file using <client2> and using <client1> sees that there is no QoS requirements to file
    When using <client1>, user1 creates "anyStorage" QoS requirement for "file1" in space "space1" in oneprovider-1
    And using <client2>, user1 deletes all QoS requirements for "file1" in space "space1" in oneprovider-1
    Then using <client1>, user1 sees that file "file1" has not QoS requirements in space "space1" in oneprovider-1

  Examples:
  | client1    | client2    |
  | REST       | web GUI    |
  | web GUI    | REST       |