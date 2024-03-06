Feature: ACL directories privileges tests on creating directories using multiple browsers in Oneprovider GUI

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


  Scenario Outline: Create subdirectory
    When user of space_owner_browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser_user1 <result> to create directory "subdir" in "dir1" in "space1"

    Examples:
    | result   |  privileges                                                        |
    | succeeds |  [data:list files, data:add subdirectory, data:traverse directory] |
    | fails    |  all except [data:add subdirectory]                                |


  Scenario: Fails to create subdirectory without data:traverse directory privilege
    When user of space_owner_browser sets "dir1" ACL all except [data:traverse directory] privileges for <subject_type> <subject_name> in "space1"
    And user of browser_user1 opens file browser for "space1" space
    And user of browser_user1 clicks and presses enter on item named "dir1" in file browser
    Then user of browser_user1 sees "PERMISSION DENIED" sign in the file browser
    And user of browser_user1 does not see button "New directory" in file browser
