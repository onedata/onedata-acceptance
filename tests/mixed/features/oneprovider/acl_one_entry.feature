Feature: ACL basic tests


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
    And initial groups configuration in "onezone" Onezone service:
            group1:
                owner: user1
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
    And oneclient mounted using token by user1
    And opened browser with user1 signed in to "onezone" service
    And directory structure created by user1 in "space1" space on oneprovider-1 as follows:
            - file1
            - dir1


  Scenario Outline: User sets ACL with one entry
    When using <client1>, user1 sets new ACE for <item> in space "space1" with [acl:read acl, acl:change acl] privileges set for <subject_type> <subject_name> in oneprovider-1
    Then using <client2>, user1 sees that <item> in space "space1" has [acl:read acl, acl:change acl] privileges set for <subject_type> <subject_name> in first ACL record in oneprovider-1

    Examples:
    | subject_type  | subject_name  | item  | client1    | client2    |
    | user          | user1         | file1 | REST       | web GUI    |
    | user          | user1         | dir1  | REST       | web GUI    |
    | group         | group1        | file1 | REST       | web GUI    |
    | user          | user1         | file1 | web GUI    | REST       |
    | user          | user1         | dir1  | web GUI    | REST       |
    | group         | group1        | file1 | web GUI    | REST       |
    | user          | user1         | file1 | oneclient1 | REST       |
    | user          | user1         | dir1  | oneclient1 | REST       |
    | group         | group1        | file1 | oneclient1 | REST       |
    | user          | user1         | file1 | REST       | oneclient1 |
    | user          | user1         | dir1  | REST       | oneclient1 |
    | group         | group1        | file1 | REST       | oneclient1 |
    | user          | user1         | file1 | oneclient1 | web GUI    |
    | user          | user1         | dir1  | oneclient1 | web GUI    |
    | group         | group1        | file1 | oneclient1 | web GUI    |
    | user          | user1         | file1 | web GUI    | oneclient1 |
    | user          | user1         | dir1  | web GUI    | oneclient1 |
    | group         | group1        | file1 | web GUI    | oneclient1 |
