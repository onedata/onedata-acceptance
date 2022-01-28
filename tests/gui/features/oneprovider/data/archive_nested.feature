Feature: Nested archives operations

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


  Scenario: User sees symbolic links on child datasets after creating nested archive on parent
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser goes to "/dir1/dir2" in file browser
    And user of browser creates dataset for item "dir3" in "space1"
    And user of browser clicks and presses enter on item named "dir3" in file browser
    And user of browser creates dataset for item "file1" in "space1"
    And user of browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: first archive
        layout: plain
        create nested archives: True

    Then user of browser sees archive browser in archives tab in Oneprovider page
    And user of browser clicks and presses enter on archive with description: "first archive" on archives list in archive browser
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser goes to "/dir1/dir2" in archive file browser
    And user of browser sees symlink status tag for "dir3" in archive file browser
    And user of browser clicks and presses enter on item named "dir3" in archive file browser
    And user of browser sees symlink status tag for "file1" in archive file browser


  Scenario: User sees that dataset has more archives than its parent after creating nested archive on child dataset
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser creates dataset for item "dir2" in "space1"
    And user of browser clicks and presses enter on item named "dir2" in file browser
    And user of browser creates dataset for item "dir3" in "space1"

    And user of browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        layout: plain
        create nested archives: True
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser sees that item "dir1" has 1 archive
    And user of browser clicks and presses enter on item named "dir1" in dataset browser
    And user of browser sees that item "dir2" has 1 archive
    And user of browser succeeds to create archive for item "dir2" in "space1" with following configuration:
        layout: plain
        create nested archives: True
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser clicks and presses enter on item named "dir2" in dataset browser
    Then user of browser sees that item "dir3" has 2 archives
    And user of browser clicks Datasets of "space1" in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser sees that item "dir1" has 1 archive


  Scenario: User sees real directory tree of downloaded tar generated for nested archive
    When user of browser creates dataset for item "dir1" in "space1"
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser creates dataset for item "dir2" in "space1"
    And user of browser clicks and presses enter on item named "dir2" in file browser
    And user of browser creates dataset for item "dir3" in "space1"
    And user of browser clicks and presses enter on item named "dir3" in file browser
    And user of browser creates dataset for item "file1" in "space1"

    And user of browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: first archive
        layout: plain
        create nested archives: True

    And user of browser sees archive browser in archives tab in Oneprovider page
    And user of browser clicks on menu for archive with description: "first archive" in archive browser
    And user of browser clicks "Copy archive ID" option in data row menu in archive browser
    And user of browser clicks on menu for archive with description: "first archive" in archive browser
    And user of browser clicks "Download (tar)" option in data row menu in archive browser
    Then user of browser sees that contents of downloaded archive TAR file (with ID from clipboard) in download directory have following structure:
          - archive:
            - dir1:
              - dir2:
                - dir3:
                  - file1: 100

