Feature: ACL directories privileges tests on changing directory and uploading to directory using multiple browsers in Oneprovider GUI


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
    | result   |  privileges                                                          |  subject_type  | subject_name  |
    | succeeds |  [content:list files, content:add files, content:traverse directory] |  user          | user1         |
    | fails    |  all except [content:add files]                                      |  user          | user1         |
    | fails    |  all except [content:traverse directory]                             |  user          | user1         |
    | succeeds |  [content:list files, content:add files, content:traverse directory] |  group         | group1        |
    | fails    |  all except [content:add files]                                      |  group         | group1        |
    | fails    |  all except [content:traverse directory]                             |  group         | group1        |

  Scenario Outline: Change directory ACL
    When user of space_owner_browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser_user1 <result> to change "dir1" ACL for <subject_name> in "space1"

    Examples:
    | result   |  privileges                   | subject_type  | subject_name  |
    | succeeds |  [acl]                        | user          | user1         |
    | fails    |  all except [acl:change acl]  | user          | user1         |
    | succeeds |  [acl]                        | group         | group1        |
    | fails    |  all except [acl:change acl]  | group         | group1        |

