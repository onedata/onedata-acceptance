Feature: Datasets mixed tests

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
              - dir1

    And opened browser with user1 signed in to "onezone" service


  Scenario Outline: Using <client1>, user creates dataset for item then using <client2> user sees that dataset was created
    When using <client1>, user1 creates dataset for item "dir1"  in space "space1" in oneprovider-1


  Examples:
  | client1    |
  | REST       |

#  Examples:
#  | client1    | client2    |
#  | REST       | web GUI    |
#  | web GUI    | REST       |