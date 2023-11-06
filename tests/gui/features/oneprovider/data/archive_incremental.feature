Feature: Incremental archives operations

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


  Scenario: User sees that files that did not change since creating last archive have 2 hardlinks tag after creating new incremental archive
    When user of browser creates dataset for item "dir4" in "space1"
    And user of browser succeeds to create archive for item "dir4" in "space1" with following configuration:
        layout: plain

    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser succeeds to upload "20B-0.txt" to "dir4" in "space1"
    And user of browser sees that item named "20B-0.txt" has appeared in file browser

    And user of browser succeeds to create archive for item "dir4" in "space1" with following configuration:
        description: second archive
        layout: plain
        incremental:
            enabled: True

    Then user of browser sees archive browser in archives tab in Oneprovider page
    And user of browser clicks and presses enter on archive with description: "second archive" on archives list in archive browser
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser clicks and presses enter on item named "dir4" in archive file browser
    And user of browser sees hardlink status tag with "2 hard links" text for "file2" in archive file browser
    And user of browser does not see hardlink status tag for "20B-0.txt" in archive file browser


  Scenario: User sees that files that did not change since creating last two base archives have 3 hardlinks tag after creating new incremental archive
    When user of browser creates dataset for item "dir4" in "space1"
    And user of browser succeeds to create archive for item "dir4" in "space1" with following configuration:
        layout: plain
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser succeeds to create archive for item "dir4" in "space1" with following configuration:
        layout: plain
        incremental:
            enabled: True
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser succeeds to create archive for item "dir4" in "space1" with following configuration:
        description: third archive
        layout: plain
        incremental:
            enabled: True

    Then user of browser sees archive browser in archives tab in Oneprovider page
    And user of browser clicks and presses enter on archive with description: "third archive" on archives list in archive browser
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser clicks and presses enter on item named "dir4" in archive file browser
    And user of browser sees hardlink status tag with "3 hard links" text for "file2" in archive file browser


  Scenario: User sees name of base archive after creating incremental archive
    When user of browser creates dataset for item "dir4" in "space1"
    And user of browser succeeds to create archive for item "dir4" in "space1" with following configuration:
        description: first archive
        layout: plain
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser succeeds to create archive for item "dir4" in "space1" with following configuration:
        description: second archive
        layout: plain
        incremental:
            enabled: True
    Then user of browser sees archive browser in archives tab in Oneprovider page
    And user of browser sees that base archive for archive with description: "second archive" is archive with description: "first archive" on archives list in archive browser


  Scenario: User sees that the base archive in create archive modal is the latest created archive after enabling incremental toggle
    When user of browser creates dataset for item "dir4" in "space1"
    And user of browser succeeds to create archive for item "dir4" in "space1" with following configuration:
        layout: plain
    And user of browser sees archive browser in archives tab in Oneprovider page
    And user of browser clicks on "Create Archive" button in archive browser
    And user of browser checks "Incremental" toggle in modal "Create Archive"
    Then user of browser sees that base archive name in Create Archive modal is the same as latest created archive name


  Scenario: User creates incremental archive that has chosen base archive
    When user of browser creates dataset for item "dir4" in "space1"
    And user of browser succeeds to create archive for item "dir4" in "space1" with following configuration:
        description: first archive
        layout: plain
    And user of browser sees archive browser in archives tab in Oneprovider page

    # create archive
    And user of browser is idle for 61 seconds
    And user of browser clicks on "Create Archive" button in archive browser
    And user of browser clicks on "Create" button in modal "Create Archive"

    And user of browser clicks on menu for archive with description: "first archive" in archive browser
    And user of browser clicks "Create incremental archive" option in data row menu in archive browser
    And user of browser clicks on "Create" button in modal "Create Archive"
    And user of browser sees archive browser in archives tab in Oneprovider page
    Then user of browser sees that base archive for latest created archive is archive with description: "first archive" on archives list in archive browser

