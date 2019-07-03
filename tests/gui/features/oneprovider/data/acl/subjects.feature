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
    And opened oneprovider-1 Oneprovider view in web GUI by user of browser
    When user of browser sees file browser in data tab in Oneprovider page
    And user of browser clicks once on item named "file1" in file browser
    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "ACL" permission type in active modal
    And user of browser clicks "Add" in ACL edit permissions modal
    Then user of browser sees that [user1, user2, user3] are in subject list in first ACL record
    And user of browser selects group as subject type in first ACL record in edit permissions modal
    And user of browser sees that [group1, group2, group3] are in subject list in first ACL record


  Scenario Outline: User sets ACL for parent group of a group that belogs to space
    Given initial spaces configuration in "onezone" Onezone service:
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
                    - file1
            groups:
                - group1
                - group2

    And opened browser with user1 signed in to "onezone" service
    And opened oneprovider-1 Oneprovider view in web GUI by user of browser
    When user of browser sets "file1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser <result> to remove "file1" in "space1"

    Examples:
    | privileges            | subject_type  | subject_name  | result    |
    | all except [delete]   | group         | group2        | fails     |
    | [delete]              | group         | group2        | succeeds  |


  Scenario Outline: User sets ACL for parent group of a group that does not belong to space
    Given initial spaces configuration in "onezone" Onezone service:
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
                    - file1
            groups:
                - group2

    And opened browser with user1 signed in to "onezone" service
    And opened oneprovider-1 Oneprovider view in web GUI by user of browser
    When user of browser sets "file1" ACL <privileges> privileges for <subject_type> <subject_name> in "space1"
    Then user of browser <result> to remove "file1" in "space1"

    Examples:
    | privileges            | subject_type  | subject_name  | result    |
    | all except [delete]   | group         | group2        | fails     |
    | [delete]              | group         | group2        | succeeds  |


  Scenario Outline: User sets excluding ACL records for group and parent group in specified order
    Given initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user3
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

    And opened browser with user3 signed in to "onezone" service
    And opened oneprovider-1 Oneprovider view in web GUI by user of browser
    When user of browser sees file browser in data tab in Oneprovider page
    And user of browser clicks once on item named "file1" in file browser

    And user of browser clicks the button from top menu bar with tooltip "Change element permissions"
    And user of browser sees that "Edit permissions" modal has appeared
    And user of browser selects "ACL" permission type in active modal
    And user of browser adds ACE with <child_privileges> privileges set for group group3
    And user of browser adds ACE with <parent_privileges> privileges set for group group1
    And user of browser clicks "OK" confirmation button in displayed modal
    Then user of browser <result> to remove "file1" in "space1"

    Examples:
    | child_privileges  | parent_privileges | result    |
    | [delete]          | [deny, delete]    | succeeds  |
    | [deny, delete]    | [delete]          | fails     |


