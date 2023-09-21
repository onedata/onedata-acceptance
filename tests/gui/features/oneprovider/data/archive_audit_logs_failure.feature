Feature: Archive audit logs, archive creation failure

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
                  - dir2:
                    - file1: 111

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service
    And directory tree structure on local file system:
            browser:
                dir3:
                  file_1.txt:
                    size: 1 MiB


  Scenario: User sees logs about unsuccessful file archivisation
    When user of browser opens file browser for "space1" space
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser uses upload button from file browser menu bar to upload files from local directory "dir3" to remote current dir
    And user of browser changes current working directory to space1 using breadcrumbs
    And user of browser creates dataset for item "dir1" in "space1"
    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser tries to create archive for item "dir1" in "space1" with following configuration:
        description: too big archive
        layout: plain
    And user of browser waits for "Failed" state for archive with description "too big archive" in archive browser
    And user of browser clicks on menu for archive with description: "too big archive" in archive browser
    And user of browser clicks "Show audit log" option in data row menu in archive browser
    And user of browser sees non empty ["Time", "Time taken"] fields of first 2 files and directories in archive audit log
    And user of browser clicks on item "file_1.txt" in archive audit log
    And user of browser sees that details for archived item in archive audit log are as follow:
        Event: Regular file archivisation failed. No space left on device.
        Time taken:
          type: time_taken
    And user of browser clicks on field "File" in details in archive audit log
    Then user of browser sees that item named "file_1.txt" is of 0 B size in archive file browser


  Scenario: User sees error message about file verification failure
    When user of browser opens file browser for "space1" space
    And user of browser creates dataset for item "dir2" in "space1"
    And Archive verification is mocked on oneprovider-krakow Oneprovider to fail
    And user of browser clicks "Datasets, Archives" of "space1" space in the sidebar
    And user of browser sees dataset browser in datasets tab in Oneprovider page
    And user of browser tries to create archive for item "dir2" in "space1" with following configuration:
        description: archive with verification failed
        layout: plain
    And user of browser waits for "Verification failed" state for archive with description "archive with verification failed" in archive browser
    And user of browser clicks on menu for archive with description: "archive with verification failed" in archive browser
    And user of browser clicks "Show audit log" option in data row menu in archive browser
    And user of browser clicks on top item in archive audit log
    Then user of browser sees message "Verification of the archived regular file failed." at field "Event" in archive audit log
