Feature: File list polling


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
    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, Onezone] page
    And user of [browser1, browser2] logged as [user1, user1] to [Onezone, Onezone] service
    And directory tree structure on local file system:
          browser2:
            test1.txt:
              content: 13
            dir2: 200


  Scenario: User sees file that was uploaded in another window after waiting a while without using refresh
    When user of browser1 opens file browser for "space1" space
    And user of browser2 opens file browser for "space1" space
    And user of browser2 uses upload button from file browser menu bar to upload local file "test1.txt" to remote current dir
    Then user of browser1 sees that item named "test1.txt" is currently visible in file browser


  Scenario: User sees 100 files from 200 uploaded at the beginning, without refresh, after 100 of them were deleted in another window
    When user of browser1 opens file browser for "space1" space
    And user of browser2 opens file browser for "space1" space
    And user of browser2 uses upload button from file browser menu bar to upload files from local directory "dir2" to remote current dir
    And user of browser1 sees that content of current directory has been loaded
    And user of browser1 scrolls to the bottom of file browser and sees there are 200 files
    And user of browser1 scrolls to the top in file browser

    And user of browser2 deletes first 100 files from current directory
    And user of browser1 is idle for 2 seconds
    Then user of browser1 scrolls to the bottom of file browser and sees there are 100 files


  Scenario: User sees renamed file in another window after waiting a while without using refresh
    When user of browser1 opens file browser for "space1" space
    And user of browser2 opens file browser for "space1" space
    And user of browser2 uses upload button from file browser menu bar to upload local file "test1.txt" to remote current dir
    And user of browser2 clicks on menu for "test1.txt" file in file browser
    And user of browser2 succeeds to rename "test1.txt" to "new_file1.txt" in "space1"
    Then user of browser1 sees that item named "new_file1.txt" is currently visible in file browser
