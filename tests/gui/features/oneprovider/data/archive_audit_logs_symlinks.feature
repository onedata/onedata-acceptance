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
                    - dir-internal-1
                  - dir-root-2:
                    - file2: 222
                    - dir-internal-2

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User sees log entries correctly describing events for archivisation with enabled "Follow symbolic links" option
    When user of browser opens file browser for "space1" space
    
    # Create symbolic links in space1
    And user of browser creates symbolic links of files in space "space1" according to the following table:
      - name: symlink-dir-root-2
        source: dir-root-2
        location: dir-root-1
      - name: symlink-dir-root-1
        source: dir-root-1
        location: dir-root-2
      - name: symlink-file1
        source: dir-root-1/file1
        location: dir-root-1/dir-internal-1
      - name: symlink-file2
        source: dir-root-2/file2
        location: dir-root-2/dir-internal-2

    And user of browser changes current working directory to space1 using breadcrumbs

    # Create a dataset and an archive with enabled "Follow symbolic links" option
    And user of browser creates dataset for item "dir-root-1" in "space1"
    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page

    And user of browser succeeds to create archive for item "dir-root-1" in "space1" with following configuration:
        description: symlinks archive
        layout: plain
        follow symbolic links: true

    And user of browser waits for "Preserved" state for archive with description "symlinks archive" in archive browser

    # View audit log and check if all files and directories are archived
    And user of browser clicks on menu for archive with description: "symlinks archive" in archive browser
    And user of browser clicks "Show audit log" option in data row menu in archive browser

    Then user of browser sees that entries in archive audit log contain following File and Event data:
        dir-root-1: Directory archivisation finished.
        symlink-dir-root-2: Directory archivisation finished.
        file2: Regular file archivisation finished.
        dir-internal-2: Directory archivisation finished.
        symlink-file2: Symbolic link archivisation finished.
        file1: Regular file archivisation finished.
        dir-internal-1: Directory archivisation finished.
        symlink-file1: Symbolic link archivisation finished.

    And user of browser sees that exactly 8 items are visible in archive audit log

    # Verify that symlink is resolved during archivisation and archived under its resolved target path
    And user of browser clicks on item "symlink-file2" in archive audit log
    And user of browser sees that details for archived item in archive audit log are as follow:
        Event: Symbolic link archivisation finished.
        Relative location: dir-root-1/symlink-dir-root-2/dir-internal-2/symlink-file2
        Source item absolute location: /space1/dir-root-2/dir-internal-2/symlink-file2


  Scenario: User sees log entries correctly describing events for archivisation with disabled "Follow symbolic links" option
    When user of browser opens file browser for "space1" space

    # Create symbolic links in space1
    And user of browser creates symbolic links of files in space "space1" according to the following table:
      - name: symlink-dir-root-2
        source: dir-root-2
        location: dir-root-1
      - name: symlink-dir-root-1
        source: dir-root-1
        location: dir-root-2
      - name: symlink-file1
        source: dir-root-1/file1
        location: dir-root-1/dir-internal-1
      - name: symlink-file2
        source: dir-root-2/file2
        location: dir-root-2/dir-internal-2

    And user of browser changes current working directory to space1 using breadcrumbs

    # Create a dataset and an archive with disabled "Follow symbolic links" option
    And user of browser creates dataset for item "dir-root-1" in "space1"
    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page

    And user of browser succeeds to create archive for item "dir-root-1" in "space1" with following configuration:
        description: symlinks archive2
        layout: plain
        follow symbolic links: false

    And user of browser waits for "Preserved" state for archive with description "symlinks archive2" in archive browser

    # View audit log and check if all files and directories are archived
    And user of browser clicks on menu for archive with description: "symlinks archive2" in archive browser
    And user of browser clicks "Show audit log" option in data row menu in archive browser

    Then user of browser sees that entries in archive audit log contain following File and Event data:
        dir-root-1: Directory archivisation finished.
        symlink-dir-root-2: Symbolic link archivisation finished.
        file1: Regular file archivisation finished.
        dir-internal-1: Directory archivisation finished.
        symlink-file1: Symbolic link archivisation finished.

    And user of browser sees that exactly 5 items are visible in archive audit log

    And user of browser clicks on "X" button in modal "Archive Details"

    # Verify that an external symlink opens target location outside the archive in the source file space
    And user of browser clicks and presses enter on archive with description: "symlinks archive2" on archives list in archive browser
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser goes to "/dir-root-1" in archive file browser

    And user of browser clicks and presses enter on item named "symlink-dir-root-2" in archive file browser
    And user of browser clicks on "Open" button in modal "External Symbolic Link"

    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is "space1/dir-root-2"

    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page

    And user of browser clicks on dataset for "dir-root-1" in dataset browser
    And user of browser sees archive browser in archives tab in Oneprovider page

    # Verify that an internal symlink inside the archive resolves to the corresponding archived target file
    And user of browser clicks and presses enter on archive with description: "symlinks archive2" on archives list in archive browser
    And user of browser sees archive file browser in archives tab in Oneprovider page
    And user of browser goes to "/dir-root-1/dir-internal-1" in archive file browser
    And user of browser downloads item "symlink-file1" in archive file browser by clicking and pressing enter and then sees that content of downloaded file is equal to: "111"