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


  Scenario: User sees that archive's data is placed on the provider creating the archive via size statistics
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser clicks on "Choose other Oneprovider" on file browser page
    And user of browser clicks on "oneprovider-2" provider on file browser page

    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser sees that item "dir1" has 0 archives
    And user of browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: first archive
        layout: plain

    And user of browser sees archive browser in archives tab in Oneprovider page
    And user of browser clicks and presses enter on archive with description: "first archive" on archives list in archive browser
    And user of browser clicks on size statistics icon for "dir1" directory in archive browser

    Then user of browser sees that current size statistics are as follow:
        logical size: 15 B
        total physical size: 15 B
        contain counter: 1 file, 1 directory (2 elements in total)
    And user of browser clicks "Show statistics per provider" button on Size stats modal
    And user of browser sees that oneprovider-1 size statistics are as follow:
        logical size: 15 B
        physical size: 0 B
        content: 1 file, 1 directory
    And user of browser sees that oneprovider-2 size statistics are as follow:
        logical size: 15 B
        physical size: 15 B
        content: 1 file, 1 directory
