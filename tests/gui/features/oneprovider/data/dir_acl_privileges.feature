Feature: ACL directories privileges tests using single browser in Oneprovider GUI

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

    And opened [browser_user1, space_owner_browser] with [user1, space-owner-user] signed in to [Onezone, Onezone] service


  Scenario Outline: Upload file to directory
    When user of space_owner_browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser_user1 <result> to upload "20B-0.txt" to "dir1" in "space1"

    Examples:
    | result   |  privileges                                                 |
    | succeeds |  [data:list files, data:add files, data:traverse directory] |
    | fails    |  all except [data:add files]                                |
    | fails    |  all except [data:traverse directory]                       |


  Scenario Outline: Rename directory
    When user of space_owner_browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser_user1 <result> to rename "dir1" to "new_name" in "space1"

    Examples:
    | result   |  privileges                   |
    | succeeds |  [general:delete]             |
    | fails    |  all except [general:delete]  |


  Scenario Outline: Read directory ACL
    When user of space_owner_browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser_user1 <result> to read "dir1" ACL in "space1"

    Examples:
    | result   |  privileges                   |
    | succeeds |  [acl:read acl]               |
    | fails    |  all except [acl:read acl]    |


  Scenario Outline: Change directory ACL
    When user of space_owner_browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser_user1 <result> to change "dir1" ACL for <subject_name> in "space1"

    Examples:
    | result   |  privileges                   |
    | succeeds |  [acl]                        |
    | fails    |  all except [acl:change acl]  |


