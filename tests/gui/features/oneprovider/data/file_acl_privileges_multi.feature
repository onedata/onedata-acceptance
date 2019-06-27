Feature: ACL files privileges tests using multiple browsers in Oneprovider GUI

  Examples:
  | subject_type  | subject_name  |
  | user          | user2         |
  | group         | group1        |

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

    And opened [browser1, browser2] with [user1, user2] signed in to [onezone, onezone] service
    And opened oneprovider-1 Oneprovider view in web GUI by users of [browser1, browser2]


  Scenario Outline: Rename file
    When user of browser1 sets "file1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser2 <result> to rename "file1" to "new_name" in "space1"

    Examples:
    | result   |  privileges           |                        
    | succeeds |  [delete]             |
    | fails    |  all except [delete]  |
        
        
  Scenario Outline: Remove file
    When user of browser1 sets "file1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser2 <result> to remove "file1" in "space1"

    Examples:
    | result   |  privileges           |                        
    | succeeds |  [delete]             |
    | fails    |  all except [delete]  |
        
        
  Scenario Outline: Read files ACL
    When user of browser1 sets "file1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser2 <result> to read "file1" ACL in "space1"

    Examples:
    | result   |  privileges           |                        
    | succeeds |  [read acl]           |
    | fails    |  all except [read acl]|
        
        
  Scenario Outline: Change files ACL
    When user of browser1 sets "file1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser2 <result> to change "file1" ACL in "space1"

    Examples:
    | result   |  privileges               |                        
    | succeeds |  [change acl]             |
    | fails    |  all except [change acl]  |
        
        
  Scenario Outline: Write metadata to file
    When user of browser1 sets "file1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser2 <result> to write "file1" basic metadata: "attr=val" in "space1"

    Examples:
    | result   |  privileges                       |            
    | succeeds |  [read metadata, write metadata]  |
    | fails    |  all except [write metadata]      |
        
        
  Scenario Outline: Read files metadata
    When user of browser1 succeeds to write "file1" basic metadata: "attr=val" in "space1"
    And user of browser1 sets "file1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser2 <result> to read "file1" basic metadata "attr=val" in "space1"

    Examples:
    | result   |  privileges                   |            
    | succeeds |  [read metadata]              |
    | fails    |  all except [read metadata]   |
