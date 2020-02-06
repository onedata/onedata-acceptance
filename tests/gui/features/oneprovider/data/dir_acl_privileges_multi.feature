Feature: ACL directories privileges tests using multiple browsers in Oneprovider GUI

  Examples:
  | subject_type  | subject_name  |
  | user          | user2         |
# TODO: change test because of a new gui
#  | group         | group1        |

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And initial groups configuration in "onezone" Onezone service:
            group1:
                owner: user2
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
            users:
                - user2
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

    And opened [browser1, browser2] with [user1, user2] signed in to [onezone, onezone] service


  Scenario Outline: Create subdirectory
    When user of browser1 sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser2 <result> to create directory "subdir" in "dir1" in "space1"

    Examples:
    | result   |  privileges                                                        |
    | succeeds |  [data:list files, data:add subdirectory, data:traverse directory] |
    | fails    |  all except [data:add subdirectory]                                |
    | fails    |  all except [data:traverse directory]                              |


# TODO: change test because of a new gui
#  Scenario Outline: Create file in directory
#    When user of browser1 sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
#    Then user of browser2 <result> to create file "subfile" in "dir1" in "space1"
#
#    Examples:
#    | result   |  privileges                                  |
#    | succeeds |  [list files, add files, traverse directory] |
#    | fails    |  all except [add files]                      |
#    | fails    |  all except [traverse directory]             |


  Scenario Outline: Rename directory
    When user of browser1 sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser2 <result> to rename "dir1" to "new_name" in "space1"

    Examples:
    | result   |  privileges                   |
    | succeeds |  [general:delete]             |
    | fails    |  all except [general:delete]  |


  Scenario Outline: Remove empty directory
    When user of browser1 sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser2 <result> to remove "dir1" in "space1"

    Examples:
    | result   |  privileges                              |
    | succeeds |  [general:delete, data:list files]       |
    | fails    |  all except [general:delete]             |
    | fails    |  all except [data:list files]            |


  Scenario Outline: Read directory ACL
    When user of browser1 sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser2 <result> to read "dir1" ACL in "space1"

    Examples:
    | result   |  privileges                   |
    | succeeds |  [acl:read acl]               |
    | fails    |  all except [acl:read acl]    |


  Scenario Outline: Change directory ACL
    When user of browser1 sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser2 <result> to change "dir1" ACL for <subject_name> in "space1"

    Examples:
    | result   |  privileges                   |
    | succeeds |  [acl]                        |
    | fails    |  all except [acl:change acl]  |


# TODO: change test because of a new gui
#  Scenario Outline: Write metadata to directory
#    When user of browser1 sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
#    Then user of browser2 <result> to write "dir1" basic metadata: "attr=val" in "space1"
#
#    Examples:
#    | result   |  privileges                       |
#    | succeeds |  [read metadata, write metadata]  |
#    | fails    |  all except [write metadata]      |
#    | fails    |  all except [read metadata]       |
#
#
#  Scenario Outline: Read directory metadata
#    When user of browser1 succeeds to write "dir1" basic metadata: "attr=val" in "space1"
#    And user of browser1 sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
#    Then user of browser2 <result> to read "dir1" basic metadata "attr=val" in "space1"
#
#    Examples:
#    | result   |  privileges                   |
#    | succeeds |  [read metadata]              |
#    | fails    |  all except [read metadata]   |
