Feature: ACL basic tests using REST client and web GUI     
    
  Examples:
  | client1 | client2   |
  | REST    | web GUI   |
  | web GUI | REST      |

  Background:
    Given initial users configuration in "z1" Onezone service:
            - user1
            - user2
    And initial groups configuration in "z1" Onezone service:
            group1:
                owner: user1
    And initial spaces configuration in "z1" Onezone service:
        space1:
            owner: user1
            users:
                - user2
            groups:
                - group1
            providers:
                - p1:
                    storage: NFS
                    size: 1000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - file1
                    - dir1

    And opened browser with user1 logged to "z1 onezone" service
    And opened p1 Oneprovider view in web GUI by user1

  Scenario: User sets ACL with one entry
    When using <client1>, user1 sets new ACE for <item> in space "space1" with <privileges> privileges set for <subject_type> <subject_name> in p1 Oneprovider
    Then using <client2>, user1 sees that <item> in space "space1" has <privileges> privileges set for <subject_type> <subject_name> in first ACL record in p1 Oneprovider

    Examples:
    | privileges            | subject_type  | subject_name  | item  |
    | [read acl, change acl]| user          | user1         | file1 |
    | [read acl, change acl]| user          | user1         | dir1  |
#   Uncomment after resolving issue VFS-3786
#    | [read acl, change acl]| group         | group1        | file1 |


#  Scenario: User sets ACL with two entries
#    When using <client1>, user1 sets new ACE for <item> in space "space1" with [read acl, change acl] privileges set for user user1 in p1 Oneprovider
#    And using <client1>, user1 sets new ACE for <item> in space "space1" with <privileges2> privileges set for <subject_type2> <subject_name2> in p1 Oneprovider
#    Then using <client2>, user1 sees that <item> in space "space1" has <privileges> privileges set for <subject_type> <subject_name> in first ACL record in p1 Oneprovider
#
#    Examples:
#    | privileges            | subject_type  | subject_name  | item  |
#    | [read, write]         | user          | user2         | file1 |
#    | [read, write]         | user          | user2         | dir1  |
#    | [deny, read, write]   | user          | user2         | file1 |
#    | [deny, read, write]   | user          | user2         | dir1  |
