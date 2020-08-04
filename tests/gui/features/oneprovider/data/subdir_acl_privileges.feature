Feature: ACL subdirectories privileges tests using sigle browser in Oneprovider GUI

  Examples:
  | subject_type  | subject_name  |
  | user          | user1         |
  | group         | group1        |

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And initial groups configuration in "onezone" Onezone service:
            group1:
                owner: user1
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user2
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
                    - dir1:
                        - file1
                        - dir2     
            groups:
                - group1 

    And opened [browser_user1, space_owner_browser] with [user1, user2] signed in to [Onezone, Onezone] service

        
  Scenario Outline: List directory items
    When user of space_owner_browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser_user1 <result> to see [file1, dir2] in "dir1" in "space1"

    Examples:
    | result   |  privileges                                 |
    | succeeds |  [data:list files, data:traverse directory] |
    | fails    |  all except [data:traverse directory]       |
    | fails    |  all except [data:list files]               |


  Scenario Outline: Rename subdirectory
    When user of space_owner_browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser_user1 <result> to rename "dir1/dir2" to "new_name" in "space1"

    Examples:
    | result   |  privileges                                                                                  |
    | succeeds |  [data:list files, data:delete child, data:traverse directory, data:add subdirectory]        |
    | fails    |  all except [data:add subdirectory]                                                          |
    | fails    |  all except [data:delete child]                                                              |


  Scenario Outline: Rename subfile
    When user of space_owner_browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser_user1 <result> to rename "dir1/file1" to "new_name" in "space1"

    Examples:
    | result   |  privileges                                                                           |
    | succeeds |  [data:list files, data:delete child, data:traverse directory, data:add files]        |
    | fails    |  all except [data:add files]                                                          |
    | fails    |  all except [data:delete child]                                                       |


  Scenario Outline: Remove non-empty directory
    When user of space_owner_browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser_user1 <result> to remove "dir1" in "space1"

    Examples:
    | result   |  privileges                                                                       |
    | succeeds |  [general:delete, data:delete child, data:list files, data:traverse directory]    |
    | fails    |  all except [general:delete]                                                      |
    | fails    |  all except [data:delete child]                                                   |
    | fails    |  all except [data:list files]                                                     |
    | fails    |  all except [data:traverse directory]                                             |


  Scenario Outline: Remove subdirectory
    When user of space_owner_browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser_user1 <result> to remove "dir1/dir2" in "space1"

    Examples:
    | result   |  privileges                                                           |
    | succeeds |  [data:delete child, data:traverse directory, data:list files]        |
    | fails    |  all except [data:delete child]                                       |


  Scenario Outline: Remove subfile
    When user of space_owner_browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser_user1 <result> to remove "dir1/file1" in "space1"

    Examples:
    | result   |  privileges                                                      |
    | succeeds |  [data:delete child, data:traverse directory, data:list files]   |
    | fails    |  all except [data:delete child]                                  |
