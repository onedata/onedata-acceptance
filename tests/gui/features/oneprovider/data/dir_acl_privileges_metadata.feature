Feature: ACL directories privileges metadata tests using single browser in Oneprovider GUI

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


  Scenario Outline: Write metadata to directory
    When user of space_owner_browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser_user1 <result> to write "dir1" directory basic metadata: "attr=val" in "space1"

    Examples:
    | result   |  privileges                                         |
    | succeeds |  [metadata:read metadata, metadata:write metadata]  |
    | fails    |  all except [metadata:write metadata]               |
    | succeeds |  all except [metadata:read metadata]                |


  Scenario Outline: Read directory metadata
    When user of space_owner_browser succeeds to write "dir1" directory basic metadata: "attr=val" in "space1"
    And user of space_owner_browser sets "dir1" directory ACL <privileges> privileges for <subject_type> <subject_name>
    Then user of browser_user1 <result> to read "dir1" directory basic metadata: "attr=val" in "space1"

    Examples:
    | result   |  privileges                            |
    | succeeds |  [metadata:read metadata]              |
    | fails    |  all except [metadata:read metadata]   |