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
                  - dir_nested

    And using REST, user1 creates 100 empty files in directories "[space1/dir1/dir2, space1/dir1/dir3]" with names sorted alphabetically supported by "oneprovider-1" provider
    And using REST, user1 creates empty file in "space1/dir_nested" in "20" nested dirs supported by "oneprovider-1" provider
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
    Then user of browser sees no empty fields "[time, time_taken]" of first 203 files and dirs in archive audit log


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
        event_message: Directory archivisation finished.
        relative_location: dir4
        start_time:
          type: date
        end_time:
          type: date
        time_taken:
          type: time_taken
        archived_item_absolute_location:
          type: location_path
        file_id:
          type: file_id
        source_item_absolute_location: /space1/dir4
    And user of browser closes details in archive audit log

    # check logs about file creation
    And user of browser clicks on item "file1" in archive audit log
    And user of browser sees that details for archived item in archive audit log are as follow:
        event_message: Regular file archivisation finished.
        relative_location: dir4/file1
        start_time:
          type: date
        end_time:
          type: date
        time_taken:
          type: time_taken
        archived_item_absolute_location:
          type: location_path
        file_id:
          type: file_id
        source_item_absolute_location: /space1/dir4/file1


  Scenario: User sees logs about nested dirs in correct order after creating archive
    When user of browser opens file browser for "space1" space
    And user of browser creates dataset for item "dir_nested" in "space1"
    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser succeeds to create archive for item "dir_nested" in "space1" with following configuration:
        description: nested archive
        layout: plain
    And user of browser waits for "Preserved" state for archive with description "nested archive" in archive browser
    And user of browser clicks on menu for archive with description: "nested archive" in archive browser
    And user of browser clicks "Show audit log" option in data row menu in archive browser
    Then user of browser sees decreasing times in archive audit log
