Feature: Basic archives operations

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
                      - dir2:
                        - dir3:
                          - file1: 100
                    - dir4:
                      - file2: 100

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User sees archive with "Preserved" state after creating it and waiting
    When user of browser creates dataset for item "dir4" in "space1"

    # create archive with description
    And user of browser clicks Datasets, Archives of "space1" space in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser sees that item "dir4" has 0 archives
    And user of browser clicks on menu for "dir4" dataset in dataset browser
    And user of browser clicks "Create archive" option in data row menu in dataset browser
    And user of browser writes "first archive" into description text field in create archive modal
    And user of browser clicks on "Create" button in modal "Create Archive"

    Then user of browser sees archive browser in archives tab in Oneprovider page
    And user of browser sees that 1st archive in archive browser has description: "first archive"
    And user of browser sees that archive with description: "first archive" in archive browser has status: "preserved", number of files: 1, size: "3 B"
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser sees that item "dir4" has 1 archive


  Scenario: User sees that dataset does not have archive after purging archive
    When user of browser creates dataset for item "dir4" in "space1"
    And user of browser succeeds to create archive for item "dir4" in "space1" with following configuration:
        description: first archive
        layout: plain
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser sees that item "dir4" has 1 archive
    And user of browser clicks on dataset for "dir4" in dataset browser
    And user of browser sees archive browser in archives tab in Oneprovider page
    And user of browser clicks on menu for archive with description: "first archive" in archive browser
    And user of browser clicks "Delete archive" option in data row menu in archive browser
    And user of browser writes "I understand that data of the archive will be lost" into confirmation input in Delete archive modal
    And user of browser clicks on "Delete archive" button in modal "Delete archive"
    Then user of browser sees that page with text "NO ARCHIVES" appeared in archive browser
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser sees that item "dir4" has 0 archives


  Scenario: User sees directory tree in archive browser after creating plain archive
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: first archive
        layout: plain
    And user of browser sees archive browser in archives tab in Oneprovider page
    And user of browser clicks and presses enter on archive with description: "first archive" on archives list in archive browser
    And user of browser sees archive file browser in archives tab in Oneprovider page
    Then user of browser sees that the file structure for archive with description: "first archive" in archive file browser is as follow:
         - dir1:
           - dir2:
             - dir3:
               - file1: 100


  Scenario: User sees that newly created archive has new file and is different than archive created earlier after creating new plain archive
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: first archive
        layout: plain
    And user of browser sees archive browser in archives tab in Oneprovider page
    And user of browser clicks and presses enter on archive with description: "first archive" on archives list in archive browser
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser sees that the file structure for archive with description: "first archive" in archive file browser is as follow:
         - dir1:
           - dir2:
             - dir3:
               - file1: 100
    And user of browser clicks Files of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser succeeds to upload "20B-0.txt" to "/dir1/dir2/dir3" in "space1"
    And user of browser sees that item named "20B-0.txt" has appeared in file browser

    And user of browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: second archive
        layout: plain
    And user of browser sees archive browser in archives tab in Oneprovider page
    And user of browser clicks and presses enter on archive with description: "second archive" on archives list in archive browser
    And user of browser sees archive file browser in archives tab in Oneprovider page
    Then user of browser sees that the file structure for archive with description: "second archive" in archive file browser is as follow:
         - dir1:
           - dir2:
             - dir3:
               - file1: 100
               - 20B-0.txt


  Scenario: User sees information about archive in properties modal after creating archive
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        layout: plain
    And user of browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: first archive
        layout: BagIt
        include DIP: True
        incremental:
                enabled: True
        create nested archives: True
    And user of browser copies name of base archive for archive with description "first archive"
    And user of browser clicks on menu for archive with description: "first archive" in archive browser
    And user of browser clicks "Properties" option in data row menu in archive browser
    Then user of browser sees archive ID in Archive properties modal
    And user of browser sees archive description: "first archive" in Archive properties modal
    And user of browser sees archive layout: "BagIt" in Archive properties modal
    And user of browser sees that Create nested archives toggle is checked in Archive properties modal
    And user of browser sees that Incremental toggle is checked in Archive properties modal
    And user of browser sees that Include DIP toggle is checked in Archive properties modal
    And user of browser sees that Follow symbolic link toggle is checked in Archive properties modal
    And user of browser sees that base archive in Archive properties modal is the same as copied

