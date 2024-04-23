Feature: ACL files privileges tests using multiple browsers in Oneprovider GUI

  Examples:
  | subject_type  | subject_name  |
  | user          | user1         |
  | group         | group1        |

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - space-owner-user
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

    And opened [browser_user1, space_owner_browser] with [user1, space-owner-user] signed in to [Onezone, Onezone] service


  Scenario Outline: Rename file
    When user of space_owner_browser sets "file1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser_user1 <result> to rename "file1" to "new_name" in "space1"

    Examples:
    | result   |  privileges                   |
    | succeeds |  [deletion:delete]             |
    | fails    |  all except [deletion:delete]  |


  Scenario Outline: Read files ACL
    When user of space_owner_browser sets "file1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser_user1 <result> to read "file1" ACL in "space1"

    Examples:
    | result   |  privileges                |
    | succeeds |  [acl:read acl]            |
    | fails    |  all except [acl:read acl] |





