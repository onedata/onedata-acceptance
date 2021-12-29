Feature: ACL files privileges tests using multiple browsers in Oneprovider GUI

  Examples:
  | subject_type  | subject_name  |
  | user          | user1         |
  | group         | group1        |

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
            - user1
    And initial groups configuration in "onezone" Onezone service:
            group1:
                owner: user1
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: space-owner-user
            users:
                - user1
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

    And opened [space_owner_browser, browser1] with [space-owner-user, user1] signed in to [onezone, onezone] service


  Scenario Outline: Rename file
    When user of space_owner_browser sets "file1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser1 <result> to rename "file1" to "new_name" in "space1"

    Examples:
    | result   |  privileges                   |
    | succeeds |  [general:delete]             |
    | fails    |  all except [general:delete]  |


  Scenario Outline: Remove file
    When user of space_owner_browser sets "file1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser1 <result> to remove "file1" in "space1"

    Examples:
    | result   |  privileges                   |
    | succeeds |  [general:delete]             |
    | fails    |  all except [general:delete]  |


  Scenario Outline: Read files ACL
    When user of space_owner_browser sets "file1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser1 <result> to read "file1" ACL in "space1"

    Examples:
    | result   |  privileges                 |
    | succeeds |  [acl:read acl]             |
    | fails    |  all except [acl:read acl]  |


  Scenario Outline: Change files ACL
    When user of space_owner_browser sets "file1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser1 <result> to change "file1" ACL for <subject_name> in "space1"

    Examples:
    | result   |  privileges                   |
    | succeeds |  [acl]                        |
    | fails    |  all except [acl:change acl]  |

