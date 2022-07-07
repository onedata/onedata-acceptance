Feature: Archives recall mixed tests

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
                  - dir3
                  - file1: 11111
              - dir4:
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


  Scenario Outline: User of <client_checking> sees that archive has been recalled after <client_recalling> recalled archive
    When using <client_recalling>, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using <client_recalling>, user1 succeeds to create archive for item "dir1" in space "space1" in oneprovider-1 with following configuration:
        description: first archive
        layout: plain
    And using <client_recalling>, user1 recalls archive with description "first archive" into "dir1" parent directory with target name "dir1_recalled" in space "space1" in oneprovider-1
    Then using <client_checking>, user1 succeeds to see item named "dir1_recalled" in "space1" in oneprovider-1
    And user1 is idle for 5 seconds
    And using <client_checking>, user1 checks "dir1_recalled" archive recalled details in "space1" in oneprovider-1 and sees following:
        status: Finished successfully
        dataset: dir1
        files_recalled: 1 / 1
        data_recalled: 5 B / 5 B
        time: finished >= started

  Examples:
  | client_recalling   | client_checking    |
  | REST               | web GUI            |
  | web GUI            | REST               |


  Scenario: User of REST sees progress of archive recall after user of web GUI recalled archive
    When using web GUI, user1 creates dataset for item "dir4" in space "space1" in oneprovider-1
    And using web GUI, user1 succeeds to create archive for item "dir4" in space "space1" in oneprovider-1 with following configuration:
        description: first archive
        layout: plain
    And using web GUI, user1 recalls archive with description "first archive" into "dir4" parent directory with target name "dir4_recalled" in space "space1" in oneprovider-1
    Then using REST, user1 sees progress of archive recall for "dir4_recalled" in "space1" in oneprovider-1:
        bytes copied: <= 40
        files copied: <= 8
    And using REST, user1 succeeds to see item named "dir4_recalled" in "space1" in oneprovider-1
    And user1 is idle for 5 seconds
    And using REST, user1 checks "dir4_recalled" archive recalled details in "space1" in oneprovider-1 and sees following:
        status: Finished successfully
        dataset: dir4
        files_recalled: 8 / 8
        data_recalled: 40 B / 40 B
        time: finished >= started


  Scenario: User of REST cancels archive recall after user of web GUI recalled archive
    When using web GUI, user1 uploads local file "large_file.txt" to "space1"
    When using web GUI, user1 creates dataset for item "large_file.txt" in space "space1" in oneprovider-1
    And using web GUI, user1 succeeds to create archive for item "large_file.txt" in space "space1" in oneprovider-1 with following configuration:
        description: first archive
        layout: plain
    And using web GUI, user1 recalls archive with description "first archive" into "large_file.txt" parent directory with target name "large_file_recalled.txt" in space "space1" in oneprovider-1
    And using REST, user1 cancels archive recall for "large_file_recalled.txt" for archive with description "first archive" for item "large_file.txt" in space "space1" in oneprovider-1
    Then using web GUI, user1 succeeds to see item named "large_file_recalled.txt" in "space1" in oneprovider-1
    And user1 is idle for 5 seconds
    And using web GUI, user1 checks "large_file_recalled.txt" archive recalled details in "space1" in oneprovider-1 and sees following:
        status: Cancelled
        dataset: large_file.txt
        files_recalled: <= 1
        data_recalled: <= 40 MiB
        time: finished >= cancelled >= started
