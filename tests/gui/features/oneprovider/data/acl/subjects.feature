Feature: ACL basic subjects tests in Oneprovider GUI

  Background:        
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
            - user3
            - user4
            - space-owner-user
    And initial groups configuration in "onezone" Onezone service:
            group1:
                owner: user1
                groups:
                    - group3
            group2:
                owner: user2
                groups: 
                    - group1
                    - group3
            group3:
                owner: user3


  Scenario: User sees eligible subjects for ACL record
    Given initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: space-owner-user
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
                    - file1
            groups:
                - group2
                - group3

    And opened browser with space-owner-user signed in to "onezone" service
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks once on item named "file1" in file browser
    And user of browser clicks on "Permissions" in context menu for "file1"
    And user of browser sees that "File details" modal is opened on "Permissions" tab
    And user of browser selects "ACL" permission type in edit permissions panel
    Then user of browser sees that [user1, user2, user3] are in subject list in ACL record
    And user of browser sees that [group1, group2, group3] are in subject list in ACL record


  Scenario Outline: User sets ACL for parent group of a group (child group belongs to space)
    Given initial spaces configuration in "onezone" Onezone service:
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
                    - file1
            groups:
                - group1
                - group2

    And opened [browser_user1, space_owner_browser] with [user1, space-owner-user] signed in to [Onezone, Onezone] service
    When user of space_owner_browser sets "file1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser_user1 <result> to remove "file1" in "space1"

    Examples:
    | privileges                    | subject_type  | subject_name  | result    |
    | all except [deletion:delete]   | group         | group2        | fails     |
    | [deletion:delete]              | group         | group2        | succeeds  |


  Scenario Outline: User sets ACL for parent group of a group (child group does not belong to space)
    Given initial spaces configuration in "onezone" Onezone service:
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
                    - file1
            groups:
                - group2

    And opened [browser_user1, space_owner_browser] with [user1, space-owner-user] signed in to [Onezone, Onezone] service
    When user of space_owner_browser sets "file1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser_user1 <result> to remove "file1" in "space1"

    Examples:
    | privileges                    | subject_type  | subject_name  | result    |
    | all except [deletion:delete]   | group         | group2        | fails     |
    | [deletion:delete]              | group         | group2        | succeeds  |


  Scenario Outline: User sets excluding ACL records for group and parent group in specified order
    Given initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: space-owner-user
            users:
                - user3
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - file1
            groups:
                - group1
                - group3

    And opened [space_owner_browser, browser_user3] with [space-owner-user, user3] signed in to [Onezone, Onezone] service
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks "Files" of "space1" space in the sidebar
    And user of space_owner_browser sees file browser in files tab in Oneprovider page
    And user of space_owner_browser clicks once on item named "file1" in file browser
    And user of space_owner_browser clicks on "Permissions" in context menu for "file1"
    And user of space_owner_browser sees that "File details" modal is opened on "Permissions" tab
    And user of space_owner_browser selects "ACL" permission type in edit permissions panel
    And user of space_owner_browser adds ACE with <child_privileges> privileges set for group group3
    And user of space_owner_browser adds ACE with <parent_privileges> privileges set for group group1
    And user of space_owner_browser clicks on "Save" button in edit permissions panel
    And user of space_owner_browser clicks on "Proceed" button in modal "Warning"
    Then user of browser_user3 <result> to remove "file1" in "space1"

    Examples:
    | child_privileges          | parent_privileges         | result    |
    | [deletion:delete]          | [deny, deletion:delete]    | succeeds  |
    | [deny, deletion:delete]    | [deletion:delete]          | fails     |


  Scenario: User sees ACL record for user removed from space
    Given initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: space-owner-user
            users:
                - user4
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - file1

    And opened browser with space-owner-user signed in to "onezone" service
    When user of browser sets "file1" ACL [acl] privileges for user user4 in "space1"
    And user of browser sets "file1" ACL [acl] privileges for user space-owner-user in "space1"
    And user of browser clicks on Data in the main menu
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser removes "user4" user from "space1" space members
    Then user of browser sees that "file1" in space "space1" has [acl] privileges set for unknown user in first ACL record
    And user of browser sees that "file1" in space "space1" contains id of user "user4" in first ACL record
    And user of browser sees that "file1" in space "space1" has [acl] privileges set for user space-owner-user in second ACL record
