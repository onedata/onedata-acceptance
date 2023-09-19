Feature: Archive audit logs

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
                    - dir2
                    - dir3
                  - dir4:
                    - file1
                    - file2

    And using REST, user1 creates 100 empty files in directories ["space1/dir1/dir2", "space1/dir1/dir3"] named file_001, file_002, ..., file_N supported by "oneprovider-1" provider
    And using REST, user1 creates a path with 20 nested directories named "dir_0/.../dir_19" in "space1" supported by "oneprovider-1" provider
    And using REST, user1 creates "file_20" file in the last of 20 nested directories "dir_0/.../dir_19" in "space1" supported by "oneprovider-1" provider
    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User sees logs about first 200 successfully archived files and 3 directories after creating archive
    When user of browser opens file browser for "space1" space
    And user of browser creates dataset for item "dir1" in "space1"
    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: first archive
        layout: plain
    And user of browser waits for "Preserved" state for archive with description "first archive" in archive browser
    And user of browser clicks on menu for archive with description: "first archive" in archive browser
    And user of browser clicks "Show audit log" option in data row menu in archive browser
    Then user of browser sees no empty ["Time", "Time taken"] fields of first 203 files and directories in archive audit log


  Scenario: User sees details about archived file or directory
    When user of browser opens file browser for "space1" space
    And user of browser creates dataset for item "dir4" in "space1"
    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser succeeds to create archive for item "dir4" in "space1" with following configuration:
        description: second archive
        layout: plain
    And user of browser waits for "Preserved" state for archive with description "second archive" in archive browser
    And user of browser clicks on menu for archive with description: "second archive" in archive browser
    And user of browser clicks "Show audit log" option in data row menu in archive browser

    # check logs about directory creation
    And user of browser clicks on item "dir4" in archive audit log
    And user of browser sees that details for archived item in archive audit log are as follow:
        Event: Directory archivisation finished.
        Relative location: dir4
        Started at:
          type: date
        Finished at:
          type: date
        Time taken:
          type: time_taken
        Archived item absolute location:
          type: location_path
        File ID:
          type: file_id
        Source item absolute location: /space1/dir4
    And user of browser closes "Details archive audit log" modal

    # check logs about file creation
    And user of browser clicks on item "file1" in archive audit log
    Then user of browser sees that details for archived item in archive audit log are as follow:
        Event: Regular file archivisation finished.
        Relative location: dir4/file1
        Started at:
          type: date
        Finished at:
          type: date
        Time taken:
          type: time_taken
        Archived item absolute location:
          type: location_path
        File ID:
          type: file_id
        Source item absolute location: /space1/dir4/file1


  Scenario: User sees logs about nested dirs in correct order after creating archive
    When user of browser opens file browser for "space1" space
    And user of browser creates dataset for item "dir_0" in "space1"
    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser succeeds to create archive for item "dir_0" in "space1" with following configuration:
        description: nested archive
        layout: plain
    And user of browser waits for "Preserved" state for archive with description "nested archive" in archive browser

    And user of browser clicks on menu for archive with description: "nested archive" in archive browser
    And user of browser clicks "Show audit log" option in data row menu in archive browser
    And user of browser sees logs about directories or files ordered ascendingly by name index with prefix dir_ or file_ in archive audit log
    And user of browser closes "Archive audit log" modal

    And user of browser clicks on menu for archive with description: "nested archive" in archive browser
    And user of browser clicks "Show audit log" option in data row menu in archive browser
    And user of browser sees entries ordered from newest to oldest in column "Time" in archive audit log
    And user of browser closes "Archive audit log" modal

    And user of browser clicks on menu for archive with description: "nested archive" in archive browser
    And user of browser clicks "Show audit log" option in data row menu in archive browser
    And user of browser sees that 21 first logs contain events about archivisation finished of files, directories or symbolic links in archive audit log
    And user of browser closes "Archive audit log" modal

    And user of browser clicks on menu for archive with description: "nested archive" in archive browser
    And user of browser clicks "Show audit log" option in data row menu in archive browser
    Then user of browser sees entries ordered from newest to oldest in column "Time taken" in archive audit log
