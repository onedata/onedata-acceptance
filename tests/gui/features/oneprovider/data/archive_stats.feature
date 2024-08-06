Feature: Size statistics of directories in archives


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
                        - dir2
                        - file1: 111111111111111

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario: User sees archive's size stats and size stats per provider after clicking show statistics button
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser clicks on "Choose other Oneprovider" on file browser page
    And user of browser clicks on "oneprovider-2" provider on file browser page

    # create archive with description
    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser sees that item "dir1" has 0 archives
    And user of browser clicks on menu for "dir1" dataset in dataset browser
    And user of browser clicks "Create archive" option in data row menu in dataset browser
    And user of browser writes "first archive" into description text field in create archive modal
    And user of browser clicks on "Create" button in modal "Create Archive"

    And user of browser sees archive browser in archives tab in Oneprovider page
    And user of browser clicks and presses enter on archive with description: "first archive" on archives list in archive browser
    And user of browser clicks on size statistics icon for "dir1" directory in archive browser
    And user of browser opens size statistics per provider view in directory details

    Then user of browser sees that logical_size for oneprovider-1 is "15 B"
    And user of browser sees that logical_size for oneprovider-2 is "15 B"
    And user of browser sees that physical_size for oneprovider-1 is "0 B"
    And user of browser sees that physical_size for oneprovider-2 is "15 B"
    And user of browser sees that oneprovider-1 content is "1 file, 1 directory"
    And trace
    And user of browser sees that oneprovider-2 content is "1 file, 1 directory"