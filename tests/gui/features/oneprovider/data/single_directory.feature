Feature: Basic data tab operations on single directory in file browser


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
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
                    - dir1:
                        - file1: 11111

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User fails to create new directory because of existing directory with given name
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs is space1

    And user of browser clicks "New directory" button from file browser menu bar
    And user of browser writes "dir1" into name directory text field in modal "Create dir"
    And user of browser confirms create new directory using button
    Then user of browser sees that error modal with text "File exists" appeared


  Scenario: User removes existing directory
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs is space1

    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Delete" option in data row menu in file browser
    And user of browser clicks on "Yes" button in modal "Delete modal"

    Then user of browser sees that item named "dir1" has disappeared from files browser


  Scenario: User renames directory
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs is space1

    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Rename" option in data row menu in file browser
    And user of browser sees that "Rename" modal has appeared
    And user of browser writes "new_dir1" into name directory text field in modal "Rename modal"
    And user of browser confirms rename directory using enter

    Then user of browser sees that item named "dir1" has disappeared from files browser
    And user of browser sees that item named "new_dir1" has appeared in file browser
    And user of browser sees that item named "new_dir1" is directory in file browser

