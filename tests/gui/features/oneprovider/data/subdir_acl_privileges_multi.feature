Feature: ACL subdirectories privileges tests using multiple browsers in Oneprovider GUI

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
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1:
                        - file1
                        - dir2     
            groups:
                - group1 

    And opened [browser1, browser2] with [user1, user2] signed in to [onezone, onezone] service
    And opened oneprovider-1 Oneprovider view in web GUI by users of [browser1, browser2]

        
  Scenario Outline: List directory items
    When user of browser1 sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser2 <result> to see [file1, dir2] in "dir1" in "space1"

    Examples:
    | result   |  privileges                       |                        
    | succeeds |  [list files, traverse directory] |
    | fails    |  all except [traverse directory]  |
    | fails    |  all except [list files]          |


  Scenario Outline: Rename subdirectory
    When user of browser1 sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser2 <result> to rename "dir1/dir2" to "new_name" in "space1"

    Examples:
    | result   |  privileges                                                              |
    | succeeds |  [list files, delete child, traverse directory, add subdirectory]        |
    | fails    |  all except [add subdirectory]                                           |
    | fails    |  all except [delete child]                                               |
    | fails    |  all except [traverse directory]                                         |
        
        
  Scenario Outline: Rename subfile
    When user of browser1 sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser2 <result> to rename "dir1/file1" to "new_name" in "space1"

    Examples:
    | result   |  privileges                                                       |
    | succeeds |  [list files, delete child, traverse directory, add files]        |
    | fails    |  all except [add files]                                           |
    | fails    |  all except [delete child]                                        |
    | fails    |  all except [traverse directory]                                  |
        
        
  Scenario Outline: Remove non-empty directory
    When user of browser1 sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser2 <result> to remove "dir1" in "space1"

    Examples:
    | result   |  privileges                                                   |
    | succeeds |  [delete, delete child, list files, traverse directory]       |
    | fails    |  all except [delete]                                          |
    | fails    |  all except [delete child]                                    |
    | fails    |  all except [list files]                                      |
    | fails    |  all except [traverse directory]                              |
        
        
  Scenario Outline: Remove subdirectory
    When user of browser1 sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser2 <result> to remove "dir1/dir2" in "space1"

    Examples:
    | result   |  privileges                                            |
    | succeeds |  [delete child, traverse directory, list files]        |
    | fails    |  all except [traverse directory]                       |
    | fails    |  all except [delete child]                             |

        
  Scenario Outline: Remove subfile
    When user of browser1 sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser2 <result> to remove "dir1/file1" in "space1"

    Examples:
    | result   |  privileges                                            |
    | succeeds |  [delete child, traverse directory, list files]        |
    | fails    |  all except [traverse directory]                       |
    | fails    |  all except [delete child]                             |
