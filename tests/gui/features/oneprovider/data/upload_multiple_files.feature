Feature: Uploading multiple files at once


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

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service
    And directory tree structure on local file system:
          browser:
              - dir1: 5
              - dir2: 70


  Scenario: User uploads 5 files at once
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload files from local directory "dir1" to remote current dir
    And user of browser is idle for 1 second
    And user of browser waits for file upload to finish
    Then user of browser sees that there are 5 items in file browser


# TODO: change test because of a new gui
#  Scenario: User uploads more than 50 files and uses files list lazy loading
#    # upload 70 files
#    When user of browser clicks "space1" on the spaces list in the sidebar
#    And user of browser clicks Data of "space1" in the sidebar
#    And user of browser sees file browser in data tab in Oneprovider page
#    And user of browser uses upload button from file browser menu bar to upload files from local directory "dir2" to remote current dir
#    And user of browser waits for file upload to finish
#    And user of browser sees that there are 70 items in file browser
#
#    # refresh site and check working of lazy loading
#    And user of browser refreshes site
#    And user of browser sees nonempty file browser in data tab in Oneprovider page
#    And user of browser sees that content of current directory has been loaded
#    And user of browser sees that there are 50 items in file browser
#    And user of browser scrolls to the bottom of file browser
#    And user of browser is idle for 10 seconds
#    Then user of browser sees that there are 70 items in file browser
#
#
#  Scenario: User changes directory while uploading bunch of files
#    When user of browser uses spaces select to change data space to "space1"
#    And user of browser sees that current working directory displayed in breadcrumbs is space1
#    And user of browser sees file browser in data tab in Oneprovider page
#
#    # create dir1
#    And user of browser clicks the button from top menu bar with tooltip "Create directory"
#    And user of browser sees that "New directory" modal has appeared
#    And user of browser clicks on input box in active modal
#    And user of browser types "dir1" on keyboard
#    And user of browser presses enter on keyboard
#    And user of browser sees that the modal has disappeared
#    And user of browser sees that item named "dir1" has appeared in file browser
#    And user of browser double clicks on item named "dir1" in file browser
#    And user of browser sees that current working directory displayed in breadcrumbs is space1/dir1
#
#    # start uploading files in dir1 and go back to root directory
#    And user of browser uses upload button in toolbar to upload files from local directory "dir2" to remote current dir
#    And user of browser is idle for 0.02 seconds
#    And user of browser changes current working directory to space1 using breadcrumbs
#    And user of browser sees that current working directory displayed in breadcrumbs is space1
#    And user of browser is idle for 5 seconds
#    And user of browser sees that there is 1 item in file browser
#
#    # go to dir 10 and see if every file has benn uploaded
#    And user of browser double clicks on item named "dir1" in file browser
#    And user of browser sees that current working directory displayed in breadcrumbs is space1/dir1
#    Then user of browser sees that there are 70 items in file browser
#
#
#  Scenario: User uploads files and sees their ordering (uploads a bunch of files at once)
#    When user of browser uses spaces select to change data space to "space1"
#    And user of browser sees that current working directory displayed in breadcrumbs is space1
#    And user of browser sees file browser in data tab in Oneprovider page
#
#    # create file10
#    And user of browser clicks the button from top menu bar with tooltip "Create file"
#    And user of browser sees that "New file" modal has appeared
#    And user of browser clicks on input box in active modal
#    And user of browser types "file10" on keyboard
#    And user of browser clicks "Create" confirmation button in displayed modal
#    And user of browser sees that the modal has disappeared
#    And user of browser sees that item named "file10" has appeared in file browser
#
#    # create file20
#    And user of browser clicks the button from top menu bar with tooltip "Create file"
#    And user of browser sees that "New file" modal has appeared
#    And user of browser clicks on input box in active modal
#    And user of browser types "file20" on keyboard
#    And user of browser clicks "Create" confirmation button in displayed modal
#    And user of browser sees that the modal has disappeared
#    And user of browser sees that item named "file20" has appeared in file browser
#
#    And user of browser uses upload button in toolbar to upload files from local directory "dir1" to remote current dir
#    And user of browser waits for file upload to finish
#    And user of browser sees items named ["file0.txt", "file20", "file10"] in file browser in given order
#    And user of browser sees items named ["file1.txt", "file20", "file10"] in file browser in given order
#    And user of browser sees items named ["file2.txt", "file20", "file10"] in file browser in given order
#    And user of browser sees items named ["file3.txt", "file20", "file10"] in file browser in given order
#    And user of browser sees items named ["file4.txt", "file20", "file10"] in file browser in given order
#    And user of browser refreshes site
#    And user of browser sees nonempty file browser in data tab in Oneprovider page
#    Then user of browser sees items named ["file0.txt", "file1.txt", "file10", "file2.txt", "file20", "file3.txt", "file4.txt"] in file browser in given order
