Feature: ACL basic tests using single browser in Oneprovider GUI

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
                    - dir2
                    - file1
                    - file2
            groups:     
                - group1  

    And opened browser with user1 signed in to "onezone" service


  Scenario Outline: User sets one ACL record for directory in Edit permissions modal
    When user of browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"

    # Check ACL record
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Permissions" option in data row menu in file browser
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "ACL" permission type in edit permissions modal
    Then user of browser sees exactly 1 ACL record in edit permissions modal
    And user of browser sees that first ACL record in edit permissions modal is set for <subject_type> <subject_name>
    And user of browser sees that only <privileges> privileges are set in first ACL record in edit permissions modal

    Examples:
    |  privileges               |  subject_type |  subject_name |
    |  [allow, acl:read acl]    |  group        |  group1       |


  Scenario Outline: User sets one ACL record for file in Edit permissions modal
    When user of browser sets "file1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"

    # Check ACL record
    And user of browser clicks on menu for "file1" directory in file browser
    And user of browser clicks "Permissions" option in data row menu in file browser
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "ACL" permission type in edit permissions modal
    Then user of browser sees exactly 1 ACL record in edit permissions modal

    And user of browser sees that first ACL record in edit permissions modal is set for <subject_type> <subject_name>
    And user of browser sees that only <privileges> privileges are set in first ACL record in edit permissions modal

    Examples:
    |  privileges               |  subject_type |  subject_name |
    |  [allow, acl:read acl]    |  group        |  group1       |


  Scenario: User cancels ACL editing
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page

    # Set ACL record
    And user of browser clicks once on item named "dir1" in file browser
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Permissions" option in data row menu in file browser
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "ACL" permission type in edit permissions modal
    And user of browser adds ACE with general:delete privilege set for user user1
    And user of browser clicks "Cancel" button in displayed modal

    # Check ACL record
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Permissions" option in data row menu in file browser
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "ACL" permission type in edit permissions modal
    Then user of browser sees exactly 0 ACL records in edit permissions modal


  Scenario Outline: User sets ACL for multiple directories
    When user of browser sets [dir1, dir2] ACL <privileges> privileges for <subject_type> <subject_name> in "space1"

    And user of browser clicks once on item named "dir1" in file browser
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Permissions" option in data row menu in file browser
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "ACL" permission type in edit permissions modal
    Then user of browser sees exactly 1 ACL record in edit permissions modal
    And user of browser sees that first ACL record in edit permissions modal is set for <subject_type> <subject_name>
    And user of browser sees that only <privileges> privileges are set in first ACL record in edit permissions modal
    And user of browser clicks "Cancel" button in displayed modal

    And user of browser clicks once on item named "dir2" in file browser
    And user of browser clicks on menu for "dir2" directory in file browser
    And user of browser clicks "Permissions" option in data row menu in file browser
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser sees exactly 1 ACL record in edit permissions modal
    And user of browser sees that first ACL record in edit permissions modal is set for <subject_type> <subject_name>
    And user of browser sees that only <privileges> privileges are set in first ACL record in edit permissions modal
    And user of browser clicks "Cancel" button in displayed modal

    Examples:
    | privileges            | subject_type  | subject_name  |
    | [allow, acl:read acl] | user          | user1         |


  Scenario Outline: User sets ACL for multiple files
    When user of browser sets [file1, file2] ACL <privileges> privileges for <subject_type> <subject_name> in "space1"

    And user of browser clicks once on item named "file1" in file browser
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Permissions" option in data row menu in file browser
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "ACL" permission type in edit permissions modal
    Then user of browser sees exactly 1 ACL record in edit permissions modal
    And user of browser sees that first ACL record in edit permissions modal is set for <subject_type> <subject_name>
    And user of browser sees that only <privileges> privileges are set in first ACL record in edit permissions modal
    And user of browser clicks "Cancel" confirmation button in displayed modal

    And user of browser clicks once on item named "file2" in file browser
    And user of browser clicks on menu for "file2" file in file browser
    And user of browser clicks "Permissions" option in data row menu in file browser
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser sees exactly 1 ACL record in edit permissions modal
    And user of browser sees that only <privileges> privileges are set in first ACL record in edit permissions modal
    And user of browser clicks "Cancel" confirmation button in displayed modal

    Examples:
    | privileges            | subject_type  | subject_name  |
    | [allow, acl:read acl] | user          | user1         |


  Scenario: User saves ACL entries for user and group
    # Set ACL record
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser clicks once on item named "file1" in file browser
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Permissions" option in data row menu in file browser
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "ACL" permission type in edit permissions modal

    And user of browser adds ACE with "attributes:read attributes" privilege set for group group1
    And user of browser adds ACE with [general:delete, acl:read acl] privileges set for user user1
    And user of browser clicks "Save" confirmation button in displayed modal

    # Check ACL records
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Permissions" option in data row menu in file browser
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "ACL" permission type in edit permissions modal
    Then user of browser sees exactly 2 ACL records in edit permissions modal
    And user of browser sees that first ACL record in edit permissions modal is set for group group1
    And user of browser sees that second ACL record in edit permissions modal is set for user "user1"


  Scenario Outline: User removes ACL record
    When user of browser sets "file1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Permissions" option in data row menu in file browser
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser clicks on "remove" button in first ACL record in edit permissions modal
    Then user of browser sees exactly 0 ACL records in edit permissions modal

    Examples:
    | privileges       | subject_type  | subject_name  |
    | [acl:read acl]   | user          | user1         |


  Scenario Outline: User changes order of ACL entries
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Permissions" option in data row menu in file browser
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "ACL" permission type in edit permissions modal

    And user of browser adds ACE with "general:delete" privilege set for group group1
    And user of browser adds ACE with "acl:read acl" privilege set for user user1
    And user of browser clicks on "<button>" button in <numeral> ACL record in edit permissions modal
    Then user of browser sees that first ACL record in edit permissions modal is set for user user1
    And user of browser sees that second ACL record in edit permissions modal is set for group group1
    And user of browser clicks "Save" confirmation button in displayed modal

    # check order after close and open modal again
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Permissions" option in data row menu in file browser
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "ACL" permission type in edit permissions modal
    And user of browser sees that first ACL record in edit permissions modal is set for user user1
    And user of browser sees that second ACL record in edit permissions modal is set for group group1


    Examples:
    | button    | numeral|
    | move up   | second |
    | move down | first  |
