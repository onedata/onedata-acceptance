Feature: Archives of Service mixed tests

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


  Scenario Outline: User of <client_checking> sees archive created previously via <client_creating>
    When using <client_creating>, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using <client_creating>, user1 creates archive for item "dir1" in space "space1" in oneprovider-1 with following configuration:
        description: first archive
        layout: plain
    Then using <client_checking>, user1 sees archive with description: "first archive" for item "dir1" in space "space1" in oneprovider-1

  Examples:
  | client_creating    | client_checking    |
  | REST               | web GUI            |
  | web GUI            | REST               |


  Scenario Outline: User of <client_checking> does not see archive removed previously via <client_removing>
    When using <client_checking>, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using <client_checking>, user1 creates archive for item "dir1" in space "space1" in oneprovider-1 with following configuration:
        description: first archive
        layout: plain
    And using <client_checking>, user1 creates archive for item "dir1" in space "space1" in oneprovider-1 with following configuration:
        description: second archive
        layout: plain
    Then using <client_removing>, user1 removes archive with description: "first archive" for item "dir1" in space "space1" in oneprovider-1
    And using <client_checking>, user1 does not see archive with description: "first archive" for item "dir1" in space "space1" in oneprovider-1

  Examples:
  | client_removing    | client_checking    |
  | REST               | web GUI            |
  | web GUI            | REST               |



  Scenario Outline: User of <client_checking> sees BagIt archive created previously via <client_creating>
    When using <client_creating>, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using <client_creating>, user1 creates archive for item "dir1" in space "space1" in oneprovider-1 with following configuration:
        description: first archive
        layout: BagIt
    Then using <client_checking>, user1 sees BagIt archive with description: "first archive" for dataset for item "dir1" in space "space1" in oneprovider-1
  Examples:
  | client_creating    | client_checking    |
  | REST               | web GUI            |
  | web GUI            | REST               |