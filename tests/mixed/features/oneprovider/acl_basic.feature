Feature: ACL basic tests

  Examples:
  | client1    | client2    |
  | REST       | web GUI    |
  | web GUI	   | REST	    |
  | oneclient1 | REST       |
  | REST       | oneclient1 |
  | oneclient1 | web GUI    |
  | web GUI    | oneclient1 |

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
    And effective support for user in provider:
        oneprovider-1:
            - user1
    And oneclient mounted in /home/user1/onedata using token by user1
    And opened browser with user1 signed in to "onezone" service
    And opened oneprovider-1 Oneprovider view in web GUI by user1
    And directory structure created by user of browser in "space1" space on oneprovider-1 as follows:
            - file1
            - dir1



  Scenario: User sets ACL with one entry
    When using <client1>, user1 sets new ACE for <item> in space "space1" with <privileges> privileges set for <subject_type> <subject_name> in oneprovider-1
    Then using <client2>, user1 sees that <item> in space "space1" has <privileges> privileges set for <subject_type> <subject_name> in first ACL record in oneprovider-1

    Examples:
    | privileges            | subject_type  | subject_name  | item  |
    | [read acl, change acl]| user          | user1         | file1 |
    | [read acl, change acl]| user          | user1         | dir1  |
#   Uncomment after resolving issue VFS-3786
#    | [read acl, change acl]| group         | group1        | file1 |


#  Scenario: User sets ACL with two entries
#    When using <client1>, user1 sets new ACE for <item> in space "space1" with [read acl, change acl] privileges set for user user1 in oneprovider-1
#    And using <client1>, user1 sets new ACE for <item> in space "space1" with <privileges2> privileges set for <subject_type2> <subject_name2> in oneprovider-1
#    Then using <client2>, user1 sees that <item> in space "space1" has <privileges> privileges set for <subject_type> <subject_name> in first ACL record oneprovider-1
#
#    Examples:
#    | privileges            | subject_type  | subject_name  | item  |
#    | [read, write]         | user          | user2         | file1 |
#    | [read, write]         | user          | user2         | dir1  |
#    | [deny, read, write]   | user          | user2         | file1 |
#    | [deny, read, write]   | user          | user2         | dir1  |
