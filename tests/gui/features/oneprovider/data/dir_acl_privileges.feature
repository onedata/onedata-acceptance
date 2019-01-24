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

    And opened browser with user1 logged to "onezone" service
    And opened oneprovider-1 Oneprovider view in web GUI by user of browser

        
  Scenario Outline: Create subdirectory
    When user of browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser <result> to create directory "subdir" in "dir1" in "space1"

    Examples:
    | result   |  privileges                                         |
    | succeeds |  [list files, add subdirectory, traverse directory] |
    | fails    |  all except [add subdirectory]                      |
    | fails    |  all except [traverse directory]                    |


  Scenario Outline: Create file in directory
    When user of browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser <result> to create file "subfile" in "dir1" in "space1"

    Examples:
    | result   |  privileges                                  |
    | succeeds |  [list files, add files, traverse directory] |
    | fails    |  all except [add files]                      |
    | fails    |  all except [traverse directory]             |


  Scenario Outline: Rename directory
    When user of browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser <result> to rename "dir1" to "new_name" in "space1"

    Examples:
    | result   |  privileges           |                        
    | succeeds |  [delete]             |
    | fails    |  all except [delete]  |
        
        
  Scenario Outline: Remove empty directory
    When user of browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser <result> to remove "dir1" in "space1"

    Examples:
    | result   |  privileges                 |               
    | succeeds |  [delete, list files]       |
    | fails    |  all except [delete]        |
    | fails    |  all except [list files]    |
        
        
  Scenario Outline: Read directory ACL
    When user of browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser <result> to read "dir1" ACL in "space1"

    Examples:
    | result   |  privileges               | 
    | succeeds |  [read acl]               |
    | fails    |  all except [read acl]    |
        
        
  Scenario Outline: Change directory ACL
    When user of browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser <result> to change "dir1" ACL in "space1"

    Examples:
    | result   |  privileges               |                        
    | succeeds |  [change acl]             |
    | fails    |  all except [change acl]  |
        
        
  Scenario Outline: Write metadata to directory
    When user of browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser <result> to write "dir1" basic metadata: "attr=val" in "space1"

    Examples:
    | result   |  privileges                       |            
    | succeeds |  [read metadata, write metadata]  |
    | fails    |  all except [write metadata]      |
    | fails    |  all except [read metadata]       |
        
        
  Scenario Outline: Read directory metadata
    When user of browser succeeds to write "dir1" basic metadata: "attr=val" in "space1"
    And user of browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser <result> to read "dir1" basic metadata "attr=val" in "space1"

    Examples:
    | result   |  privileges                   |            
    | succeeds |  [read metadata]              |
    | fails    |  all except [read metadata]   |
