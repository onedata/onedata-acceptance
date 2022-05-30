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
                    size: 10000000000

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
            dir5: 300
            dir6:
            file1MiB.txt:
              size: 1 MiB

  Scenario: User uploads 5 files at once
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload files from local directory "dir1" to remote current dir
    Then user of browser sees that there are 5 items in file browser


  Scenario: User uploads more than 50 files and uses files list lazy loading
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" space in the sidebar

    # upload 70 files
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload files from local directory "dir2" to remote current dir

    # check working of lazy loading
    And user of browser sees nonempty file browser in files tab in Oneprovider page
    And user of browser sees that content of current directory has been loaded
    Then user of browser scrolls to the bottom of file browser and sees there are 70 files


  Scenario: User can change directory while uploading files
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page

    # create dir1
    And user of browser creates directory "dir1"
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is /dir1

    # start uploading files in dir1 and go back to root directory
    And user of browser uses upload button from file browser menu bar to upload files from local directory "dir2" to remote current dir without waiting for upload to finish
    And user of browser changes current working directory to space root using breadcrumbs
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is space1
    And user of browser waits for file upload to finish
    And user of browser sees that there is 1 item in file browser

    # go to dir and see if every file has been uploaded
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser sees that current working directory displayed in breadcrumbs on file browser is /dir1
    Then user of browser scrolls to the bottom of file browser and sees there are 70 files


  Scenario: Files uploaded by user are ordered by name
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page

    And user of browser uses upload button from file browser menu bar to upload files from local directory "dir3" to remote current dir
    And user of browser uses upload button from file browser menu bar to upload files from local directory "dir4" to remote current dir
    Then user of browser sees items named ["file0.txt", "file1.txt", "file10.txt", "file2.txt", "file23.txt", "file3.txt"] in file browser in given order


# TODO: Some uploaded files are not visible in file browser right after upload (VFS-8436)
  Scenario: User successfully uploads 300 files (stress test)
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" space in the sidebar

    # upload 300 files
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload files from local directory "dir5" to remote current dir and waits extended time for upload to finish
# TODO: Uncomment when "Some uploaded files are not visible in file browser right after upload (VFS-8436)" will be fixed
#    Then user of browser scrolls to the bottom of file browser and sees there are 300 files


  Scenario: User successfully uploads 1 GB file (stress test)
    Given user of browser creates file named "file1GB.txt" sized: 1 GiB in "/dir6" on local file system
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" space in the sidebar

    # upload 1GB file
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload files from local directory "dir6" to remote current dir and waits extended time for upload to finish
    Then user of browser sees that there is 1 item in file browser

    # deleting file from file browser and local file system
    And user of browser removes file1GB.txt from provider's storage mount point
    And user of browser removes "/dir6/file1GB.txt" from local file system


  Scenario: User with weak connection uploads 1 MB file
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" space in the sidebar

    # upload one larger file
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload local file "file1MiB.txt" to remote current dir with slow connection
    Then user of browser sees that there is 1 item in file browser