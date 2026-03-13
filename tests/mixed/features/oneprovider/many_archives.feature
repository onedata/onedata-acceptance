Feature: Management of a great number of archives

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
                    - dir1
    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User can see correct number of created archives in archive browser
    When using REST, user1 creates 10 empty files in "space1/dir1" named "file_001", "file_002", ..., "file_N" supported by "oneprovider-1" provider
    And using REST, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using REST, user1 creates 100 archives for dataset "dir1" in space "space1" in host oneprovider-1 with following configuration:
        layout: plain
    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser clicks on dataset for "dir1" in dataset browser
    And user of browser sees archive browser in archives tab in Oneprovider page
    Then user of browser can see 100 of archives in archive browser


  Scenario: User can see correct number of files in archive file browser
    When using REST, user1 creates 100 empty files in "space1/dir1" named "file_001", "file_002", ..., "file_N" supported by "oneprovider-1" provider
    And using REST, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using REST, user1 succeeds to create archive for item "dir1" in space "space1" in oneprovider-1 with following configuration:
        description: first archive
        layout: plain

    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser clicks on dataset for "dir1" in dataset browser
    And user of browser sees archive browser in archives tab in Oneprovider page

    And user of browser clicks and presses enter on archive with description: "first archive" on archives list in archive browser
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser clicks and presses enter on item named "dir1" in archive file browser
    Then user of browser scrolls to the bottom of archive file browser and sees there are 100 files


  Scenario: User can see correct number of files in dataset archive browser
    When using REST, user1 creates 100 empty files in "space1/dir1" named "file_001", "file_002", ..., "file_N" supported by "oneprovider-1" provider
    And using REST, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using REST, user1 succeeds to create archive for item "dir1" in space "space1" in oneprovider-1 with following configuration:
        description: first archive
        layout: plain
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in archives tab in Oneprovider page
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks on archives tab in datasets modal
    And user of browser sees dataset archive browser in archives tab in Oneprovider page

    And user of browser clicks and presses enter on archive with description: "first archive" on archives list in dataset archive browser
    And user of browser clicks and presses enter on item named "dir1" in dataset archive browser
    Then user of browser scrolls to the bottom of dataset archive browser and sees there are 100 files


  Scenario: User can see correct number of created archives in dataset archive browser
    When using REST, user1 creates 10 empty files in "space1/dir1" named "file_001", "file_002", ..., "file_N" supported by "oneprovider-1" provider
    And using REST, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using REST, user1 creates 100 archives for dataset "dir1" in space "space1" in host oneprovider-1 with following configuration:
        layout: plain

    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in archives tab in Oneprovider page
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks on archives tab in datasets modal
    And user of browser sees dataset archive browser in archives tab in Oneprovider page

    Then user of browser can see 100 of archives in dataset archive browser


  Scenario: User can see correct number of files in archive recall browser
    When using REST, user1 creates 100 empty files in "space1/dir1" named "file_001", "file_002", ..., "file_N" supported by "oneprovider-1" provider
    And using REST, user1 creates dataset for item "dir1" in space "space1" in oneprovider-1
    And using REST, user1 succeeds to create archive for item "dir1" in space "space1" in oneprovider-1 with following configuration:
        description: first archive
        layout: plain

    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in archives tab in Oneprovider page
    And user of browser clicks on menu for "dir1" directory in file browser
    And user of browser clicks "Datasets" option in data row menu in file browser
    And user of browser clicks on archives tab in datasets modal
    And user of browser sees dataset archive browser in archives tab in Oneprovider page

    And user of browser clicks on menu for archive with description: "first archive" in dataset archive browser
    And user of browser clicks "Recall to..." option in data row menu in dataset archive browser
    And user of browser sees archive recall browser in archives tab in Oneprovider page
    And user of browser clicks and presses enter on item named "dir1" in archive recall browser

    Then user of browser scrolls to the bottom of archive recall browser and sees there are 100 files

