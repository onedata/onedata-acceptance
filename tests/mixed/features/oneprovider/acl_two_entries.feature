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


  Scenario Outline: User sets ACL with two entries
    When using <client1>, user1 sets new ACE for <item> in space "space1" with [acl:read acl, acl:change acl] privileges set for user user1 in oneprovider-1
    When using <client1>, user1 sets new ACE for <item> in space "space1" with <privileges> privileges set for <subject_type> <subject_name> in oneprovider-1
    Then using <client2>, user1 sees that <item> in space "space1" has <privileges> privileges set for <subject_type> <subject_name> in second ACL record in oneprovider-1
    And using <client2>, user1 sees that <item> in space "space1" has [acl:read acl, acl:change acl] privileges set for user user1 in first ACL record in oneprovider-1

    Examples:
    | privileges                                    | subject_type  | subject_name  | item  | client1    | client2    |
    | [content:read, content:write]                 | user          | user2         | file1 | REST       | web GUI    |
    | [content:list files, content:add files]       | user          | user2         | dir1  | REST       | web GUI    |
    | [deny, content:read, content:write]           | user          | user2         | file1 | REST       | web GUI    |
    | [deny, content:list files, content:add files] | user          | user2         | dir1  | REST       | web GUI    |
    | [content:read, content:write]                 | user          | user2         | file1 | web GUI    | REST       |
    | [content:list files, content:add files]       | user          | user2         | dir1  | web GUI    | REST       |
    | [deny, content:read, content:write]           | user          | user2         | file1 | web GUI    | REST       |
    | [deny, content:list files, content:add files] | user          | user2         | dir1  | web GUI    | REST       |
    | [content:read, content:write]                 | user          | user2         | file1 | oneclient1 | REST       |
    | [content:list files, content:add files]       | user          | user2         | dir1  | oneclient1 | REST       |
    | [deny, content:read, content:write]           | user          | user2         | file1 | oneclient1 | REST       |
    | [deny, content:list files, content:add files] | user          | user2         | dir1  | oneclient1 | REST       |
    | [content:read, content:write]                 | user          | user2         | file1 | REST       | oneclient1 |
    | [content:list files, content:add files]       | user          | user2         | dir1  | REST       | oneclient1 |
    | [deny, content:read, content:write]           | user          | user2         | file1 | REST       | oneclient1 |
    | [deny, content:list files, content:add files] | user          | user2         | dir1  | REST       | oneclient1 |
    | [content:read, content:write]                 | user          | user2         | file1 | oneclient1 | web GUI    |
    | [content:list files, content:add files]       | user          | user2         | dir1  | oneclient1 | web GUI    |
    | [deny, content:read, content:write]           | user          | user2         | file1 | oneclient1 | web GUI    |
    | [deny, content:list files, content:add files] | user          | user2         | dir1  | oneclient1 | web GUI    |
    | [content:read, content:write]                 | user          | user2         | file1 | web GUI    | oneclient1 |
    | [content:list files, content:add files]       | user          | user2         | dir1  | web GUI    | oneclient1 |
    | [deny, content:read, content:write]           | user          | user2         | file1 | web GUI    | oneclient1 |
    | [deny, content:list files, content:add files] | user          | user2         | dir1  | web GUI    | oneclient1 |
