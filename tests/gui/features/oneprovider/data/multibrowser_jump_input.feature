Feature: Jump to file using jump input in two file browsers


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

    And using REST, user1 creates 200 empty files in "space1" with names sorted alphabetically supported by "oneprovider-1" provider
    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, Onezone] page
    And user of [browser1, browser2] logged as [user1, user1] to [Onezone, Onezone] service
    And directory tree structure on local file system:
            browser2:
                file_0011.txt:
                  size: 1 MiB


  Scenario: User sees file that was uploaded in another window after scrolling to the bottom and writing file name in jump input
    When user of browser1 clicks "Files" of "space1" space in the sidebar
    And user of browser1 sees file browser in files tab in Oneprovider page
    And user of browser1 sees that items named ["file_001", "file_002"] are currently visible in file browser
    And user of browser2 clicks "Files" of "space1" space in the sidebar
    And user of browser2 sees file browser in files tab in Oneprovider page
    And user of browser2 uses upload button from file browser menu bar to upload local file "file_0011.txt" to remote current dir
    And user of browser1 scrolls to the bottom of file browser
    And user of browser1 clicks "Refresh" button from file browser menu bar
    And user of browser1 writes "file_0011" to jump input in file browser
    Then user of browser1 sees that item named "file_0011.txt" is currently visible in file browser
