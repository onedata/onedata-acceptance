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
                size: 200000000
          storage:
            defaults:
              provider: oneprovider-1
            directory tree:
              - dir1:
                - dir2:
                  - dir4
                  - file1: 11111
              - dir5:
                - file1: 11111
                - file2: 11111
                - file3: 11111
                - file4: 11111
                - file5: 11111
                - file6: 11111
                - file7: 11111
                - file8: 11111


    And opened browser with user1 signed in to "onezone" service
    And directory tree structure on local file system:
          user1:
            large_file.txt:
              size: 40 MiB


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


  Scenario Outline: User of <client_checking> sees new "preserved" callback URL after changing it using REST
    When using web GUI, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using web GUI, user1 succeeds to create archive for item "dir1" in space "space1" in oneprovider-1 with following configuration:
        description: first archive
        layout: plain
    And using <client_checking>, user1 sees that preserved callback is "None" for archive with description "first archive" for item "dir1" in space "space1" in oneprovider-1
    And using REST, user1 changes archive preserved callback to "https://archives.org/preserved_archives" for archive with description "first archive" for item "dir1" in space "space1" in oneprovider-1
    And if <client_checking> is web GUI, user1 is idle for 10 seconds
    Then using <client_checking>, user1 sees that preserved callback is "https://archives.org/preserved_archives" for archive with description "first archive" for item "dir1" in space "space1" in oneprovider-1

  Examples:
  | client_checking    |
  | REST               |
  | web GUI            |


  Scenario Outline: User of <client_checking> sees new "deleted" callback URL after changing it using REST
    When using web GUI, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using web GUI, user1 succeeds to create archive for item "dir1" in space "space1" in oneprovider-1 with following configuration:
        description: first archive
        layout: plain
    And using <client_checking>, user1 sees that deleted callback is "None" for archive with description "first archive" for item "dir1" in space "space1" in oneprovider-1
    And using REST, user1 changes archive deleted callback to "https://archives.org/purged_archives" for archive with description "first archive" for item "dir1" in space "space1" in oneprovider-1
    And if <client_checking> is web GUI, user1 is idle for 10 seconds
    Then using <client_checking>, user1 sees that deleted callback is "https://archives.org/purged_archives" for archive with description "first archive" for item "dir1" in space "space1" in oneprovider-1

  Examples:
  | client_checking    |
  | REST               |
  | web GUI            |


  Scenario Outline: User of <client_checking> sees that archive has been recalled after <client_recalling> recalled archive
    When using <client_recalling>, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using <client_recalling>, user1 succeeds to create archive for item "dir1" in space "space1" in oneprovider-1 with following configuration:
        description: first archive
        layout: plain
    And using <client_recalling>, user1 recalls archive to "dir1_recalled" for archive with description "first archive" for item "dir1" in space "space1" in oneprovider-1
    Then using <client_checking>, user1 succeeds to see item named "dir1_recalled" in "space1" in oneprovider-1

    And user1 is idle for 5 seconds
    And using <client_checking>, user1 sees "dir1_recalled" archive recalled details in "space1" in oneprovider-1:
        status: Finished successfully
        dataset: dir1
        files_recalled: 1 / 1
        data_recalled: 5 B / 5 B
        time: finish_time >= start_time

  Examples:
  | client_recalling   | client_checking    |
  | REST               | web GUI            |
  | web GUI            | REST               |


  Scenario: Using REST user sees progress of archive recall after using web GUI user recalled archive.
    When using web GUI, user1 creates dataset for item "dir5" in space "space1" in oneprovider-1
    And using web GUI, user1 succeeds to create archive for item "dir5" in space "space1" in oneprovider-1 with following configuration:
        description: first archive
        layout: plain
    And using web GUI, user1 recalls archive to "dir5_recalled" for archive with description "first archive" for item "dir5" in space "space1" in oneprovider-1
    Then using REST, user1 sees progress of archive recall for "dir5_recalled" in "space1" in oneprovider-1:
        bytes copied: <= 40
        files copied: <= 8
    And using REST, user1 succeeds to see item named "dir5_recalled" in "space1" in oneprovider-1
    And user1 is idle for 5 seconds
    And using REST, user1 sees "dir5_recalled" archive recalled details in "space1" in oneprovider-1:
        status: Finished successfully
        dataset: dir5
        files_recalled: 8 / 8
        data_recalled: 40 B / 40 B
        time: finish_time >= start_time


  Scenario: Using REST user cancels archive recall after using <client_recalling> user recalled archive.
    When using web GUI, user1 uploads local file "large_file.txt" to "space1"
    When using web GUI, user1 creates dataset for item "large_file.txt" in space "space1" in oneprovider-1
    And using web GUI, user1 succeeds to create archive for item "large_file.txt" in space "space1" in oneprovider-1 with following configuration:
        description: first archive
        layout: plain
    And using web GUI, user1 recalls archive to "large_file_recalled.txt" for archive with description "first archive" for item "large_file.txt" in space "space1" in oneprovider-1
    And using REST, user1 cancels archive recall for "large_file_recalled.txt" for archive with description "first archive" for item "large_file.txt" in space "space1" in oneprovider-1
    Then using web GUI, user1 succeeds to see item named "large_file_recalled.txt" in "space1" in oneprovider-1
    And user1 is idle for 5 seconds
    And using web GUI, user1 sees "large_file_recalled.txt" archive recalled details in "space1" in oneprovider-1:
        status: Cancelled
        dataset: large_file.txt
        files_recalled: <= 1
        data_recalled: <= 40 MiB
        time: finish_time >= cancelled_time >= start_time

