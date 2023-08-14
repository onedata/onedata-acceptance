Feature: Archive audit logs symbolic links

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
                  - dir-root-1:
                    - file1: 111
                    - dir-internal-1:
                  - dir-root-2:
                    - file2: 222
                    - dir-internal-2:

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User sees archivisation logs correctly show data with or without option "Follow Symlinks"
    When user of browser opens file browser for "space1" space

    # create symlinks in dir-root-1
    And user of browser clicks on menu for "dir-root-2" file in file browser
    And user of browser clicks "Create symbolic link" option in data row menu in file browser
    And user of browser clicks and presses enter on item named "dir-root-1" in file browser
    And user of browser clicks "Place symbolic link" button from file browser menu bar
    And user of browser succeeds to rename "dir-root-2" to "symlink-dir-root-2" in "space1"
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Create symbolic link" option in data row menu in file browser
    And user of browser clicks and presses enter on item named "dir-internal-1" in file browser
    And user of browser clicks "Place symbolic link" button from file browser menu bar
    And user of browser succeeds to rename "file1" to "symlink-file1" in "space1"
    And user of browser changes current working directory to space1 using breadcrumbs

    # create symlinks in dir-root-2
    And user of browser clicks on menu for "dir-root-1" file in file browser
    And user of browser clicks "Create symbolic link" option in data row menu in file browser
    And user of browser clicks and presses enter on item named "dir-root-2" in file browser
    And user of browser clicks "Place symbolic link" button from file browser menu bar
    And user of browser succeeds to rename "dir-root-1" to "symlink-dir-root-1" in "space1"
    And user of browser clicks on menu for "file2" file in file browser
    And user of browser clicks "Create symbolic link" option in data row menu in file browser
    And user of browser clicks and presses enter on item named "dir-internal-2" in file browser
    And user of browser clicks "Place symbolic link" button from file browser menu bar
    And user of browser succeeds to rename "file2" to "symlink-file2" in "space1"
    And user of browser changes current working directory to space1 using breadcrumbs

    # create and test archive with option follow symbolic links: true
    And user of browser creates dataset for item "dir-root-1" in "space1"
    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser succeeds to create archive for item "dir-root-1" in "space1" with following configuration:
        description: symlinks archive
        layout: plain
        follow symbolic links: true
    And user of browser waits for "Preserved" state for archive with description "symlinks archive" in archive browser
    And user of browser clicks on menu for archive with description: "symlinks archive" in archive browser
    And user of browser clicks "Show audit log" option in data row menu in archive browser
    And user of browser sees that items "[dir-root-1, symlink-dir-root-2, file2, dir-internal-2, symlink-file2, file1, dir-internal-1, symlink-file1]" are visible in archive audit log
    And user of browser sees that 8 items are visible in archive audit log
    And user of browser clicks on item "symlink-file2" in archive audit log
    And user of browser sees message "Symbolic link archivisation finished." at field "event_message" in archive audit log
    And user of browser sees message "dir-root-1/symlink-dir-root-2/dir-internal-2/symlink-file2" at field "relative_location" in archive audit log
    And user of browser sees message "/space1/dir-root-2/dir-internal-2/symlink-file2" at field "source_item_absolute_location" in archive audit log

    # create and test archive with option follow symbolic links: false
    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser succeeds to create archive for item "dir-root-1" in "space1" with following configuration:
        description: symlinks archive2
        layout: plain
        follow symbolic links: false
    And user of browser waits for "Preserved" state for archive with description "symlinks archive2" in archive browser
    And user of browser clicks on menu for archive with description: "symlinks archive2" in archive browser
    And user of browser clicks "Show audit log" option in data row menu in archive browser
    And user of browser sees that items "[dir-root-1, file1, dir-internal-1, symlink-file1, symlink-dir-root-2]" are visible in archive audit log
    Then user of browser sees that 5 items are visible in archive audit log
