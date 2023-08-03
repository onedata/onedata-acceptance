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
                    - dir2:
                    - dir3:
                  - dir4:
                    - file1
                    - file2
                  - dir_nested:

#    And using REST, user1 creates 100 empty files in directories "["space1/dir1/dir2", "space1/dir1/dir3"]" with names sorted alphabetically supported by "oneprovider-1" provider
    And using REST, user1 creates empty file in "space1/dir_nested" in "20" nested dirs supported by "oneprovider-1" provider
    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


#  Scenario: User sees logs about first number successfully archived files and directories
#    When user of browser clicks "space1" on the spaces list in the sidebar
#    And user of browser clicks "Files" of "space1" space in the sidebar
#    And user of browser sees file browser in files tab in Oneprovider page
#    And user of browser creates dataset for item "dir1" in "space1"
#    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
#    And user of browser sees dataset browser in datasets tab in Oneprovider page
#    And user of browser succeeds to create archive for item "dir1" in "space1" with following configuration:
#        description: first archive
#        layout: plain
#    And user of browser waits for "Preserved" state for archive with description "first archive" in archive browser
#    And user of browser clicks on menu for archive with description: "first archive" in archive browser
#    And user of browser clicks "Show audit log" option in data row menu in archive browser
#    And user of browser sees no empty "["creation_time", "creation_duration_time"]" info of first "203" files and dirs in archive audit log

#  Scenario: User sees details about archived file or directory
#    When user of browser clicks "space1" on the spaces list in the sidebar
#    And user of browser clicks "Files" of "space1" space in the sidebar
#    And user of browser sees file browser in files tab in Oneprovider page
#    And user of browser creates dataset for item "dir4" in "space1"
#    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
#    And user of browser sees dataset browser in datasets tab in Oneprovider page
#    And user of browser succeeds to create archive for item "dir4" in "space1" with following configuration:
#        description: second archive
#        layout: plain
#    And user of browser waits for "Preserved" state for archive with description "second archive" in archive browser
#    And user of browser clicks on menu for archive with description: "second archive" in archive browser
#    And user of browser clicks "Show audit log" option in data row menu in archive browser
#    And user of browser clicks on item "dir4" in archive audit log
#    And user of browser sees "Directory archivisation finished." in field "event_message" in archive audit log
#    And user of browser sees "dir4" in field "relative_location" in archive audit log
#    And user of browser sees message pattern "date" in field "start_time" in archive audit log
#    And user of browser sees message pattern "date" in field "end_time" in archive audit log
#    And user of browser sees message pattern "time_taken" in field "time_taken" in archive audit log
#    And user of browser sees message pattern "location_path" in field "archived_item_absolute_location" in archive audit log
#    And user of browser sees message pattern "file_id" in field "file_id" in archive audit log
#    And user of browser sees "/space1/dir4" in field "source_item_absolute_location" in archive audit log
#    And user of browser closes details in archive audit log
#
#    And user of browser clicks on item "file1" in archive audit log
#    And user of browser sees "Regular file archivisation finished." in field "event_message" in archive audit log
#    And user of browser sees "dir4/file1" in field "relative_location" in archive audit log
#    And user of browser sees message pattern "date" in field "start_time" in archive audit log
#    And user of browser sees message pattern "date" in field "end_time" in archive audit log
#    And user of browser sees message pattern "time_taken" in field "time_taken" in archive audit log
#    And user of browser sees message pattern "location_path" in field "archived_item_absolute_location" in archive audit log
#    And user of browser sees message pattern "file_id" in field "file_id" in archive audit log
#    And user of browser sees "/space1/dir4/file1" in field "source_item_absolute_location" in archive audit log

  Scenario: User sees logs about nested dirs in correct order
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser creates dataset for item "dir_nested" in "space1"
    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser succeeds to create archive for item "dir_nested" in "space1" with following configuration:
        description: nested archive
        layout: plain
    And user of browser waits for "Preserved" state for archive with description "nested archive" in archive browser
    And user of browser clicks on menu for archive with description: "nested archive" in archive browser
    And user of browser clicks "Show audit log" option in data row menu in archive browser
    And user of browser sees decreasing times in archive audit log
    And trace