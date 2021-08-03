Feature: Uploading multiple files at once


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: space-owner-user
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service
    And directory tree structure on local file system:
          browser:
            dir1: 5
            dir2: 70
            dir3: 4
            dir4:
              file10.txt:
                content: 10
              file23.txt:
                content: 23


  Scenario: User uploads 5 files at once
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload files from local directory "dir1" to remote current dir
    Then user of browser sees that there are 5 items in file browser


  Scenario: User uploads more than 50 files and uses files list lazy loading
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar

    # upload 70 files
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload files from local directory "dir2" to remote current dir

    # check working of lazy loading
    And user of browser sees nonempty file browser in files tab in Oneprovider page
    And user of browser sees that content of current directory has been loaded
    Then user of browser scrolls to the bottom of file browser and sees there are 70 files


  Scenario: User can change directory while uploading files
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page

    # create dir1
    And user of browser creates directory "dir1"
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is /dir1

    # start uploading files in dir1 and go back to root directory
    And user of browser uses upload button from file browser menu bar to upload files from local directory "dir2" to remote current dir without waiting for upload to finish
    And user of browser changes current working directory to home using breadcrumbs
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is space1
    And user of browser waits for file upload to finish
    And user of browser sees that there is 1 item in file browser

    # go to dir and see if every file has been uploaded
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is /dir1
    Then user of browser scrolls to the bottom of file browser and sees there are 70 files


  Scenario: Files uploaded by user are ordered by name
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page

    And user of browser uses upload button from file browser menu bar to upload files from local directory "dir3" to remote current dir
    And user of browser uses upload button from file browser menu bar to upload files from local directory "dir4" to remote current dir
    Then user of browser sees items named ["file0.txt", "file1.txt", "file10.txt", "file2.txt", "file23.txt", "file3.txt"] in file browser in given order
