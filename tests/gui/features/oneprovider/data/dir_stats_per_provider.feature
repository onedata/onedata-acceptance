Feature: Directories size statistics per providers


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
                - oneprovider-2:
                    storage: posix
                    size: 1000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1:
                        - file1: 111111111111111
                    - dir2:
                        - file2: 111111111111111
                    - dir3:
                        - file3: 111111111111111111111111111111
    And directory tree structure on local file system:
        browser:
            file4:
                size: 40 B
    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario: User sees space's size stats per provider after clicking show statistics button
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is space1
    And user of browser opens size statistics per provider view using breadcrumbs menu
    Then user of browser sees that logical_size for oneprovider-1 is "60 B"
    And user of browser sees that logical_size for oneprovider-2 is "60 B"
    And user of browser sees that physical_size for oneprovider-1 is "60 B"
    And user of browser sees that physical_size for oneprovider-2 is "0 B"
    And user of browser sees that oneprovider-1 content is "3 files, 3 directories"
    And user of browser sees that oneprovider-2 content is "3 files, 3 directories"


  Scenario: User sees space's size stats disabled after unchecking size statistics toggle for oneprovider-2
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Providers" of "space1" space in the sidebar
    And user of browser clicks on "oneprovider-2" provider on providers page
    And user of browser unchecks size statistics toggle in selected provider settings on providers page
    And user of browser clicks on "Disable" button in modal "Disable directory statistics"
    And user of browser clicks on "oneprovider-1" provider on providers page
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is space1
    And user of browser opens size statistics per provider view using breadcrumbs menu
    Then user of browser sees that logical_size for oneprovider-1 is "60 B"
    And user of browser sees that physical_size for oneprovider-1 is "60 B"
    And user of browser sees that oneprovider-1 content is "3 files, 3 directories"
    And user of browser sees that error message for oneprovider-2 is "Directory statistics are disabled."


  Scenario: User sees space's size stats per provider after clicking show statistics button and uploading 40 B file to oneprovider-2
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Providers" of "space1" space in the sidebar
    And user of browser clicks on "oneprovider-2" provider on providers page
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is space1
    And user of browser creates directory "dir4"
    And user of browser clicks and presses enter on item named "dir4" in file browser
    And user of browser uses upload button from file browser menu bar to upload local file "file4" to remote current dir
    And user of browser changes current working directory to space root using breadcrumbs
    And user of browser opens size statistics per provider view using breadcrumbs menu
    Then user of browser sees that logical_size for oneprovider-1 is "100 B"
    And user of browser sees that logical_size for oneprovider-2 is "100 B"
    And user of browser sees that physical_size for oneprovider-1 is "60 B"
    And user of browser sees that physical_size for oneprovider-2 is "40 B"
    And user of browser sees that oneprovider-1 content is "4 files, 4 directories"
    And user of browser sees that oneprovider-2 content is "4 files, 4 directories"


 Scenario: User sees space's size stats per provider after clicking show statistics button after replicating directories from oneprovider-1 to oneprovider-2
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is space1
    And user of browser replicates "dir1" to provider "oneprovider-2"
    And user of browser replicates "dir2" to provider "oneprovider-2"
    And user of browser replicates "dir3" to provider "oneprovider-2"
    And user of browser opens size statistics per provider view using breadcrumbs menu
    Then user of browser sees that logical_size for oneprovider-1 is "60 B"
    And user of browser sees that logical_size for oneprovider-2 is "60 B"
    And user of browser sees that physical_size for oneprovider-1 is "60 B"
    And user of browser sees that physical_size for oneprovider-2 is "60 B"
    And user of browser sees that oneprovider-1 content is "3 files, 3 directories"
    And user of browser sees that oneprovider-2 content is "3 files, 3 directories"
