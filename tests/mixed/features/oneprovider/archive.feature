Feature: Archives mixed tests

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
              - dir1:
                - dir2:
                  - dir4
                  - file1
                - dir3

    And opened browser with user1 signed in to "onezone" service


  Scenario Outline: User of <client_checking> sees archive created previously via <client_creating>
    When using <client_creating>, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using <client_creating>, user1 succeeds to create archive for item "dir1" in space "space1" in oneprovider-1 with following configuration:
        description: first archive
        layout: plain
    Then using <client_checking>, user1 sees archive with description: "first archive" for item "dir1" in space "space1" in oneprovider-1

  Examples:
  | client_creating    | client_checking    |
  | REST               | web GUI            |
  | web GUI            | REST               |


  Scenario Outline: User of <client_checking> does not see archive removed previously via <client_removing>
    When using <client_checking>, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using <client_checking>, user1 succeeds to create archive for item "dir1" in space "space1" in oneprovider-1 with following configuration:
        description: first archive
        layout: plain
    And using <client_checking>, user1 succeeds to create archive for item "dir1" in space "space1" in oneprovider-1 with following configuration:
        description: second archive
        layout: plain
    Then using <client_removing>, user1 succeeds to remove archive with description: "first archive" for item "dir1" in space "space1" in oneprovider-1
    And using <client_checking>, user1 does not see archive with description: "first archive" for item "dir1" in space "space1" in oneprovider-1

  Examples:
  | client_removing    | client_checking    |
  | REST               | web GUI            |
  | web GUI            | REST               |


  Scenario Outline: User of <client_checking> sees BagIt archive created previously via <client_creating>
    When using <client_creating>, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using <client_creating>, user1 succeeds to create archive for item "dir1" in space "space1" in oneprovider-1 with following configuration:
        description: first archive
        layout: BagIt
    Then using <client_checking>, user1 sees BagIt archive with description: "first archive" for dataset for item "dir1" in space "space1" in oneprovider-1

  Examples:
  | client_creating    | client_checking    |
  | REST               | web GUI            |
  | web GUI            | REST               |


  Scenario Outline: User of <client_checking> sees that dataset has more archives than its parent after user of <client_creating> created nested archive on child dataset
    When using <client_creating>, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using <client_creating>, user1 creates dataset for item "dir1/dir2" in space "space1" in oneprovider-1
    And using <client_creating>, user1 creates dataset for item "dir1/dir2/dir4" in space "space1" in oneprovider-1
    And using <client_creating>, user1 succeeds to create archive for item "dir1" in space "space1" in oneprovider-1 with following configuration:
        description: first archive
        layout: plain
        create nested archives: True
    And using <client_checking>, user1 sees archive with description: "first archive" for item "dir1" in space "space1" in oneprovider-1
    And  using <client_checking>, user1 sees that dataset for item "dir1/dir2" has 1 archive in space "space1" in oneprovider-1
    And  using <client_checking>, user1 sees that dataset for item "dir1/dir2/dir4" has 1 archive in space "space1" in oneprovider-1
    And using <client_creating>, user1 succeeds to create archive for item "dir1/dir2" in space "space1" in oneprovider-1 with following configuration:
        description: second archive
        layout: plain
        create nested archives: True
    Then using <client_checking>, user1 sees that dataset for item "dir1" has 1 archive in space "space1" in oneprovider-1
    And using <client_checking>, user1 sees archive with description: "second archive" for item "dir1/dir2" in space "space1" in oneprovider-1
    And  using <client_checking>, user1 sees that dataset for item "dir1/dir2" has 2 archive in space "space1" in oneprovider-1
    And  using <client_checking>, user1 sees that dataset for item "dir1/dir2/dir4" has 2 archive in space "space1" in oneprovider-1

  Examples:
  | client_creating    | client_checking    |
  | REST               | web GUI            |
  | web GUI            | REST               |


  Scenario Outline: User of <client_checking> sees DIP archive created previously via <client_creating>
    When using <client_creating>, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using <client_creating>, user1 succeeds to create archive for item "dir1" in space "space1" in oneprovider-1 with following configuration:
        description: first archive
        layout: plain
        include DIP: True
    Then using <client_checking>, user1 sees DIP archive with description: "first archive" for dataset for item "dir1" in space "space1" in oneprovider-1

  Examples:
  | client_creating    | client_checking    |
  | REST               | web GUI            |
  | web GUI            | REST               |


  Scenario Outline: User of <client_checking> sees that archive has base archive after <client_creating> created incremental archive
    When using <client_creating>, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using <client_creating>, user1 succeeds to create archive for item "dir1" in space "space1" in oneprovider-1 with following configuration:
        description: first archive
        layout: plain
    And using <client_creating>, user1 succeeds to create archive for item "dir1" in space "space1" in oneprovider-1 with following configuration:
        description: second archive
        layout: plain
        incremental:
            enabled: True
            basedOn: first archive
    Then using <client_checking>, user1 sees that archive with description "second archive" has base archive with description "first archive" for item "dir1" in space "space1" in oneprovider-1

  Examples:
  | client_creating    | client_checking    |
  | REST               | web GUI            |
  | web GUI            | REST               |


  Scenario: Using web GUI, user1 sees that archive description has been changed after user1 changed it using REST
    When using web GUI, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using web GUI, user1 succeeds to create archive for item "dir1" in space "space1" in oneprovider-1 with following configuration:
        description: first archive
        layout: plain
    And using REST, user1 changes archive description to "new archive description" for archive with description "first archive" for item "dir1" in space "space1" in oneprovider-1
    Then using web GUI, user1 sees archive with description: "new archive description" for item "dir1" in space "space1" in oneprovider-1
    And using web GUI, user1 does not see archive with description: "first archive" for item "dir1" in space "space1" in oneprovider-1


  Scenario: User of REST sees new "preserved" callback URL after changing it
    When using web GUI, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using web GUI, user1 succeeds to create archive for item "dir1" in space "space1" in oneprovider-1 with following configuration:
        description: first archive
        layout: plain
    And using REST, user1 sees that preserved callback is "None" for archive with description "first archive" for item "dir1" in space "space1" in oneprovider-1
    And using REST, user1 changes archive preserved callback to "https://archives.org/preserved_archives" for archive with description "first archive" for item "dir1" in space "space1" in oneprovider-1
    Then using REST, user1 sees that preserved callback is "https://archives.org/preserved_archives" for archive with description "first archive" for item "dir1" in space "space1" in oneprovider-1


  Scenario: User of REST sees new "purged" callback URL after changing it
    When using web GUI, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using web GUI, user1 succeeds to create archive for item "dir1" in space "space1" in oneprovider-1 with following configuration:
        description: first archive
        layout: plain
    And using REST, user1 sees that purged callback is "None" for archive with description "first archive" for item "dir1" in space "space1" in oneprovider-1
    And using REST, user1 changes archive purged callback to "https://archives.org/purged_archives" for archive with description "first archive" for item "dir1" in space "space1" in oneprovider-1
    Then using REST, user1 sees that purged callback is "https://archives.org/purged_archives" for archive with description "first archive" for item "dir1" in space "space1" in oneprovider-1



