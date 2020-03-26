Feature: ACL directories privileges tests using sigle browser in Oneprovider GUI

  Examples:
  | subject_type  | subject_name  |
  | user          | user1         |
  | group         | group1        |

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial groups configuration in "onezone" Onezone service:
            group1:
                owner: user1
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
            groups:
                - group1 

    And opened browser with user1 signed in to "onezone" service

        
  Scenario Outline: Create subdirectory
    When user of browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser <result> to create directory "subdir" in "dir1" in "space1"

    Examples:
    | result   |  privileges                                                        |
    | succeeds |  [data:list files, data:add subdirectory, data:traverse directory] |
    | fails    |  all except [data:add subdirectory]                                |
    | fails    |  all except [data:traverse directory]                              |


  Scenario Outline: Upload file to directory
    When user of browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser <result> to upload "20B-0.txt" to "dir1" in "space1"

    Examples:
    | result   |  privileges                                                 |
    | succeeds |  [data:list files, data:add files, data:traverse directory] |
    | fails    |  all except [data:add files]                                |
    | fails    |  all except [data:traverse directory]                       |


  Scenario Outline: Rename directory
    When user of browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser <result> to rename "dir1" to "new_name" in "space1"

    Examples:
    | result   |  privileges                   |
    | succeeds |  [general:delete]             |
    | fails    |  all except [general:delete]  |


  Scenario Outline: Remove empty directory
    When user of browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser <result> to remove "dir1" in "space1"

    Examples:
    | result   |  privileges                              |
    | succeeds |  [general:delete, data:list files]       |
    | fails    |  all except [general:delete]             |
    | fails    |  all except [data:list files]            |


  Scenario Outline: Read directory ACL
    When user of browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser <result> to read "dir1" ACL in "space1"

    Examples:
    | result   |  privileges                   |
    | succeeds |  [acl:read acl]               |
    | fails    |  all except [acl:read acl]    |


  Scenario Outline: Change directory ACL
    When user of browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser <result> to change "dir1" ACL for <subject_name> in "space1"

    Examples:
    | result   |  privileges                   |
    | succeeds |  [acl]                        |
    | fails    |  all except [acl:change acl]  |


# TODO: change test because of a new gui (metadata)
#  Scenario Outline: Write metadata to directory
#    When user of browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
#    Then user of browser <result> to write "dir1" basic metadata: "attr=val" in "space1"
#
#    Examples:
#    | result   |  privileges                       |
#    | succeeds |  [read metadata, write metadata]  |
#    | fails    |  all except [write metadata]      |
#    | fails    |  all except [read metadata]       |
#
#
#  Scenario Outline: Read directory metadata
#    When user of browser succeeds to write "dir1" basic metadata: "attr=val" in "space1"
#    And user of browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
#    Then user of browser <result> to read "dir1" basic metadata "attr=val" in "space1"
#
#    Examples:
#    | result   |  privileges                   |
#    | succeeds |  [read metadata]              |
#    | fails    |  all except [read metadata]   |
