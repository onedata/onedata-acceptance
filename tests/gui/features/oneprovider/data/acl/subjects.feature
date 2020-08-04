Feature: ACL basic subjects tests in Oneprovider GUI

  Background:        
    Given initial users configuration in "onezone" Onezone service:
            - user1
            - user2
            - user3
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
            owner: user1
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

    And opened browser with user1 signed in to "onezone" service
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser clicks once on item named "file1" in file browser
    And user of browser clicks on menu for "file1" directory in file browser
    And user of browser clicks "Permissions" option in data row menu in file browser
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "ACL" permission type in edit permissions modal
    Then user of browser sees that [user1, user2, user3] are in subject list in ACL record
    And user of browser sees that [group1, group2, group3] are in subject list in ACL record


  Scenario Outline: User sets ACL for parent group of a group (child group belongs to space)
    Given initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user3
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

    And opened [browser_user1, space_owner_browser] with [user1, user3] signed in to [Onezone, Onezone] service
    When user of space_owner_browser sets "file1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser_user1 <result> to remove "file1" in "space1"

    Examples:
    | privileges                    | subject_type  | subject_name  | result    |
    | all except [general:delete]   | group         | group2        | fails     |
    | [general:delete]              | group         | group2        | succeeds  |


  Scenario Outline: User sets ACL for parent group of a group (child group does not belong to space)
    Given initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user3
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

    And opened [browser_user1, space_owner_browser] with [user1, user3] signed in to [Onezone, Onezone] service
    When user of space_owner_browser sets "file1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser_user1 <result> to remove "file1" in "space1"

    Examples:
    | privileges                    | subject_type  | subject_name  | result    |
    | all except [general:delete]   | group         | group2        | fails     |
    | [general:delete]              | group         | group2        | succeeds  |


  Scenario Outline: User sets excluding ACL records for group and parent group in specified order
    Given initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
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

    And opened [space_owner_browser, browser_user3] with [user1, user3] signed in to [Onezone, Onezone] service
    When user of space_owner_browser clicks "space1" on the spaces list in the sidebar
    And user of space_owner_browser clicks Data of "space1" in the sidebar
    And user of space_owner_browser sees file browser in data tab in Oneprovider page
    And user of space_owner_browser clicks once on item named "file1" in file browser

    And user of space_owner_browser clicks on menu for "file1" directory in file browser
    And user of space_owner_browser clicks "Permissions" option in data row menu in file browser
    And user of space_owner_browser sees that "Edit permissions" modal has appeared
    And user of space_owner_browser selects "ACL" permission type in edit permissions modal
    And user of space_owner_browser adds ACE with <child_privileges> privileges set for group group3
    And user of space_owner_browser adds ACE with <parent_privileges> privileges set for group group1
    And user of space_owner_browser clicks "Save" confirmation button in displayed modal
    Then user of browser_user3 <result> to remove "file1" in "space1"

    Examples:
    | child_privileges          | parent_privileges         | result    |
    | [general:delete]          | [deny, general:delete]    | succeeds  |
    | [deny, general:delete]    | [general:delete]          | fails     |


