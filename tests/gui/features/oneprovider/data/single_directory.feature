Feature: Basic files tab operations on single directory in file browser


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: space-owner-user
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
    And user of browser logged as space-owner-user to Onezone service


  Scenario: User fails to create new directory because of existing directory with given name
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is "space1"

    And user of browser clicks "New directory" button from file browser menu bar
    And user of browser writes "dir1" into text field in modal "Create dir"
    And user of browser confirms create new directory using button
    Then user of browser sees that error modal with text "File exists" appeared


  Scenario: User removes existing directory
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is "space1"

    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Delete" option in data row menu in file browser
    And user of browser clicks on "Yes" button in modal "Delete modal"

    Then user of browser sees that item named "dir1" has disappeared from file browser


  Scenario: User renames directory
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is "space1"

    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Rename" option in data row menu in file browser
    And user of browser sees that "Rename" modal has appeared
    And user of browser writes "new_dir1" into text field in modal "Rename modal"
    And user of browser confirms rename directory using enter

    Then user of browser sees that item named "dir1" has disappeared from file browser
    And user of browser sees that item named "new_dir1" has appeared in file browser
    And user of browser sees that item named "new_dir1" is directory in file browser


  Scenario: User fails to rename directory into incorrect name
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is "space1"

    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Rename" option in data row menu in file browser
    And user of browser sees that "Rename" modal has appeared
    And user of browser writes ".." into text field in modal "Rename modal"
    And user of browser clicks "Rename" button in displayed modal
    Then user of browser sees that error modal with text "Renaming the file failed!" appeared
    And user of browser refreshes site
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that item named "dir1" is directory in file browser


  Scenario: User uploads file into directory and sees that date time in modified column is updated
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser enables only "modified" column in columns configuration popover in file browser table
    And user of browser saves content of "modified" column for "dir1" in file browser
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
    And user of browser changes current working directory to space1 using breadcrumbs
    Then user of browser sees that date time in "modified" column for "dir1" has become more current in file browser


  Scenario: User removes file in directory and sees that date time in modified column is updated
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser enables only "modified" column in columns configuration popover in file browser table
    And user of browser saves content of "modified" column for "dir1" in file browser
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Delete" option in data row menu in file browser
    And user of browser clicks on "Yes" button in modal "Delete modal"
    And user of browser changes current working directory to space1 using breadcrumbs
    Then user of browser sees that date time in "modified" column for "dir1" has become more current in file browser


  Scenario: User renames file in directory and sees that date time in modified column is updated
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser enables only "modified" column in columns configuration popover in file browser table
    And user of browser saves content of "modified" column for "dir1" in file browser
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser succeeds to rename "file1" to "file2" in "space1/dir1"
    And user of browser changes current working directory to space1 using breadcrumbs
    Then user of browser sees that date time in "modified" column for "dir1" has become more current in file browser
