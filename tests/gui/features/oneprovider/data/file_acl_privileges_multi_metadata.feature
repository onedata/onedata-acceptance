Feature: ACL files privileges metadata tests using multiple browsers in Oneprovider GUI

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


  Scenario Outline: Write metadata to file
    When user of space_owner_browser sets "file1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser1 <result> to write "file1" file basic metadata: "attr=val" in "space1"

    Examples:
    | result   |  privileges                                         |
    | succeeds |  [metadata:read metadata, metadata:write metadata]  |
    | fails    |  all except [metadata:write metadata]               |
    | succeeds |  all except [metadata:read metadata]                 |


  Scenario Outline: Read files metadata
    When user of space_owner_browser succeeds to write "file1" file basic metadata: "attr=val" in "space1"
    And user of space_owner_browser sets selected items ACL <privileges> privileges for <subject_type> <subject_name>
    Then user of browser1 <result> to read "file1" file basic metadata: "attr=val" in "space1"

    Examples:
    | result   |  privileges                           |
    | succeeds |  [metadata:read metadata]             |
    | fails    |  all except [metadata:read metadata]  |
