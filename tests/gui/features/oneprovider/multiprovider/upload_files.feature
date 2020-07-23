Feature: uploading files to multiple providers


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial spaces configuration in "onezone" Onezone service:
          space1:
              owner: user1
              providers:
                  - oneprovider-1:
                      storage: posix
                      size: 100000000
                  - oneprovider-2:
                      storage: posix
                      size: 100000000

    And user opened browser window
    And user of browser opened Onezone page
    And user of browser logged as user1 to Onezone service
    And directory tree structure on local file system:
          browser:
              - dir2: 200


  Scenario: User successfully uploads different files to two oneproviders and sees that they are accessible.
    When user of browser opens file browser for "space1" space

    # uploads file to first provider and chooses another
    And user of browser uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
    And user of browser clicks on Choose other Oneprovider on file browser page
    And user of browser sees provider named "oneprovider-1" on file browser page
    And user of browser sees provider named "oneprovider-2" on file browser page
    And user of browser clicks on "oneprovider-2" provider on file browser page

    # upload different file to different provider
    And user of browser uses upload button from file browser menu bar to upload file "20B-1.txt" to current dir

    Then user of browser clicks on Uploads in the main menu

    # check all uploads number
    And user of browser clicks on "All uploads" in uploads sidebar
    And user of browser sees that number of uploads is equal 2
    And user of browser sees that file "20B-0.txt" is uploaded
    And user of browser sees that file "20B-1.txt" is uploaded

    # check uploads number and file names in uploads from providers
    And user of browser clicks on provider "oneprovider-1" in uploads sidebar
    And user of browser sees that number of uploads is equal 1
    And user of browser sees that file "20B-0.txt" is uploaded

    And user of browser clicks on provider "oneprovider-2" in uploads sidebar
    And user of browser sees that number of uploads is equal 1
    And user of browser sees that file "20B-1.txt" is uploaded


  Scenario: User uploads a large file to provider and cancels uploading, sees that file is not uploaded
    When user of browser opens file browser for "space1" spacer page

    # upload file and cancel
    And user of browser uses upload button from file browser menu bar to upload files from local directory "dir2" to remote current dir
    And user of browser uses upload button from file browser menu bar to upload file "large_file.txt" to current dir
    And user of browser clicks cancel button on upload popup number 2
    And user of browser confirms canceling the upload
    And user of browser is idle for 15 seconds

    # Go to uploads and see that there is only 200 files
    Then user of browser clicks on Uploads in the main menu
    And user of browser clicks on "All uploads" in uploads sidebar
    And user of browser sees that number of uploads is equal 201
    And user of browser clicks on Data in the main menu
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser scrolls to the bottom of file browser and sees there are 200 files
