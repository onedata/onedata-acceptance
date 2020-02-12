Feature: ACL files privileges tests using sigle browser in Oneprovider GUI

  Examples:
  | subject_type  | subject_name  |
  | user          | user1         |
# TODO: change test because of a new gui
#  | group         | group1        |

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial groups configuration in "onezone" Onezone service:
            group1:
                owner: user1
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
            groups:
                - group1 
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


#  Scenario Outline: Rename file
#    When user of browser sets "file1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
#    Then user of browser <result> to rename "file1" to "new_name" in "space1"
#
#    Examples:
#    | result   |  privileges                   |
#    | succeeds |  [general:delete]             |
#    | fails    |  all except [general:delete]  |
#
#
#  Scenario Outline: Remove file
#    When user of browser sets "file1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
#    Then user of browser <result> to remove "file1" in "space1"
#
#    Examples:
#    | result   |  privileges                   |
#    | succeeds |  [general:delete]             |
#    | fails    |  all except [general:delete]  |


# TODO: change test because of a new gui
#  Scenario Outline: Read files ACL
#    When user of browser sets "file1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
#    Then user of browser <result> to read "file1" ACL in "space1"
#
#    Examples:
#    | result   |  privileges           |
#    | succeeds |  [read acl]           |
#    | fails    |  all except [read acl]|
#
#
#  Scenario Outline: Change files ACL
#    When user of browser sets "file1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
#    Then user of browser <result> to change "file1" ACL in "space1"
#
#    Examples:
#    | result   |  privileges               |
#    | succeeds |  [change acl]             |
#    | fails    |  all except [change acl]  |
#
#
#  Scenario Outline: Write metadata to file
#    When user of browser sets "file1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
#    Then user of browser <result> to write "file1" basic metadata: "attr=val" in "space1"
#
#    Examples:
#    | result   |  privileges                       |
#    | succeeds |  [read metadata, write metadata]  |
#    | fails    |  all except [write metadata]      |
#
#
#  Scenario Outline: Read files metadata
#    When user of browser succeeds to write "file1" basic metadata: "attr=val" in "space1"
#    And user of browser sets "file1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
#    Then user of browser <result> to read "file1" basic metadata "attr=val" in "space1"
#
#    Examples:
#    | result   |  privileges                   |
#    | succeeds |  [read metadata]              |
#    | fails    |  all except [read metadata]   |
