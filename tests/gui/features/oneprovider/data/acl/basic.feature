Feature: ACL basic tests using sigle browser in Oneprovider GUI

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
    And opened oneprovider-1 Oneprovider view in web GUI by user of browser
        
        
  Scenario: User sees default ACL privileges for directory in Edit permissions modal
    When user of browser sees file browser in data tab in Oneprovider page
    And user of browser clicks once on item named "dir1" in file browser
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "ACL" permission type in active modal
    And user of browser clicks "Add" in ACL edit permissions modal
    Then user of browser sees exactly 1 ACL record in edit permissions modal
    And user of browser sees that first ACL record has user subject type in edit permissions modal
    And user of browser sees that there is no subject in first ACL record in edit permissions modal
    And user of browser sees that subject type is editable in first ACL record in edit permissions modal
    And user of browser sees that subject name is editable in first ACL record in edit permissions modal
    And user of browser sees that only [allow, list files, add files, read acl, change acl] privileges are set in first ACL record in edit permissions modal
    And user of browser sees that "OK" item displayed in modal is disabled


  Scenario: User sees default ACL privileges for file in Edit permissions modal
    When user of browser sees file browser in data tab in Oneprovider page
    And user of browser clicks once on item named "file1" in file browser
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "ACL" permission type in active modal
    And user of browser clicks "Add" in ACL edit permissions modal
    Then user of browser sees exactly 1 ACL record in edit permissions modal
    And user of browser sees that first ACL record has user subject type in edit permissions modal
    And user of browser sees that there is no subject in first ACL record in edit permissions modal
    And user of browser sees that subject type is editable in first ACL record in edit permissions modal
    And user of browser sees that subject name is editable in first ACL record in edit permissions modal
    And user of browser sees that only [allow, read, write, read acl, change acl] privileges are set in first ACL record in edit permissions modal
    And user of browser sees that "OK" item displayed in modal is disabled


  Scenario Outline: User sets one ACL record for directory in Edit permissions modal
    When user of browser sets "dir1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"               

    # Check ACL record
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "ACL" permission type in active modal
    Then user of browser sees exactly 1 ACL record in edit permissions modal
    And user of browser sees that first ACL record in edit permissions modal is set for <subject_type> <subject_name>
    And user of browser sees that only <privileges> privileges are set in first ACL record in edit permissions modal
    And user of browser sees that subject type is not editable in first ACL record in edit permissions modal

    Examples:
    |  privileges           |  subject_type |  subject_name |
    |  [allow, read acl]    |  group        |  group1       |


  Scenario Outline: User sets one ACL record for file in Edit permissions modal
    When user of browser sets "file1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"               

    # Check ACL record
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "ACL" permission type in active modal
    Then user of browser sees exactly 1 ACL record in edit permissions modal
    And user of browser sees that first ACL record in edit permissions modal is set for <subject_type> <subject_name>
    And user of browser sees that only <privileges> privileges are set in first ACL record in edit permissions modal
    And user of browser sees that subject type is not editable in first ACL record in edit permissions modal

    Examples:
    |  privileges           |  subject_type |  subject_name |
    |  [allow, read acl]    |  group        |  group1       |


  Scenario: User cancels ACL editing
    # Set ACL record
    When user of browser sees file browser in data tab in Oneprovider page
    And user of browser clicks once on item named "dir1" in file browser
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "ACL" permission type in active modal
    And user of browser adds ACE with "delete" privilege set for user user1
    And user of browser clicks "Cancel" button in displayed modal
    And user of browser sees that the modal has disappeared

    # Check ACL record
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "ACL" permission type in active modal
    Then user of browser sees exactly 0 ACL records in edit permissions modal


  Scenario Outline: User sets ACL for multiple directories 
    When user of browser sets [dir1, dir2] ACL <privileges> privileges for <subject_type> <subject_name> in "space1"               

    And user of browser clicks once on item named "dir1" in file browser
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    Then user of browser sees exactly 1 ACL record in edit permissions modal
    And user of browser sees that first ACL record in edit permissions modal is set for <subject_type> <subject_name>
    And user of browser sees that only <privileges> privileges are set in first ACL record in edit permissions modal
    And user of browser clicks "Cancel" button in displayed modal
    And user of browser sees that the modal has disappeared

    And user of browser clicks once on item named "dir2" in file browser
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser sees exactly 1 ACL record in edit permissions modal
    And user of browser sees that first ACL record in edit permissions modal is set for <subject_type> <subject_name>
    And user of browser sees that only <privileges> privileges are set in first ACL record in edit permissions modal
    And user of browser clicks "Cancel" button in displayed modal
    And user of browser sees that the modal has disappeared
    
    Examples:
    | privileges       | subject_type  | subject_name  |
    | [allow, read acl]| user          | user1         |


  Scenario Outline: User sets ACL for multiple files 
    When user of browser sets [file1, file2] ACL <privileges> privileges for <subject_type> <subject_name> in "space1"               

    And user of browser clicks once on item named "file1" in file browser
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    Then user of browser sees exactly 1 ACL record in edit permissions modal
    And user of browser sees that first ACL record in edit permissions modal is set for <subject_type> <subject_name>
    And user of browser sees that only <privileges> privileges are set in first ACL record in edit permissions modal
    And user of browser clicks "Cancel" confirmation button in displayed modal
    And user of browser sees that the modal has disappeared

    And user of browser clicks once on item named "file2" in file browser
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser sees exactly 1 ACL record in edit permissions modal
    And user of browser sees that only <privileges> privileges are set in first ACL record in edit permissions modal
    And user of browser clicks "Cancel" confirmation button in displayed modal
    And user of browser sees that the modal has disappeared
    
    Examples:
    | privileges       | subject_type  | subject_name  |
    | [allow, read acl]| user          | user1         |


  Scenario: User sets 2 ACL records 
    # Set ACL record
    When user of browser sees file browser in data tab in Oneprovider page
    And user of browser clicks once on item named "file1" in file browser
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "ACL" permission type in active modal
    And user of browser adds ACE with "read" privilege set for group group1
    And user of browser adds ACE with [delete, read acl] privileges set for user user1
    And user of browser clicks "OK" confirmation button in displayed modal
    And user of browser sees that the modal has disappeared

    # Check ACL records
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "ACL" permission type in active modal
    Then user of browser sees exactly 2 ACL records in edit permissions modal
    And user of browser sees that first ACL record in edit permissions modal is set for group group1
    And user of browser sees that second ACL record in edit permissions modal is set for user "user1"


  Scenario: User removes ACL record   
    When user of browser sets "file1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"               
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser clicks on "remove" button in first ACL record in edit permissions modal
    Then user of browser sees exactly 0 ACL records in edit permissions modal

    Examples:
    | privileges   | subject_type  | subject_name  |
    | [read acl]   | user          | user1         |


  Scenario Outline: User changes order of ACL entries
    When user of browser sees file browser in data tab in Oneprovider page
    And user of browser clicks once on item named "dir1" in file browser
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "ACL" permission type in active modal
    And user of browser adds ACE with "delete" privilege set for group group1
    And user of browser adds ACE with "delete" privilege set for user user1
    And user of browser clicks on <button> button in <numeral> ACL record in edit permissions modal                       
    Then user of browser sees that first ACL record in edit permissions modal is set for user user1
    And user of browser sees that second ACL record in edit permissions modal is set for group group1

    Examples:
    | button    | numeral|
    | move up   | second |
    | move down | first  |
