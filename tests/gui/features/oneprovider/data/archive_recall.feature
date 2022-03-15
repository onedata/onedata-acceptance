Feature: Archive recall tests

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 240000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1:
                        - file1: 11111

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service
    And directory tree structure on local file system:
          browser:
              file.txt:
                size: 2 MiB


  Scenario: User successfully recalls archive if there is space on device
    When user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser creates dataset for item "dir1" in "space1"
    And user of browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: first archive
        layout: plain
    And user of browser clicks on menu for archive with description: "first archive" in archive browser
    And user of browser clicks "Recall to..." option in data row menu in archive browser
    And user of browser writes "dir1_recalled" into target name input text field in modal "Recall archive"
    And user of browser clicks on "Recall" button in modal "Recall archive"
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on recalled status tag for "dir1_recalled" in file browser
    Then user of browser sees status: "Archive recall finished successfully" in archive recall information modal
    And user of browser sees files recalled: "1 / 1" in archive recall information modal
    And user of browser sees data recalled: "5 B / 5 B" in archive recall information modal
    And user of browser sees that recall has been finished at the same time or after recall has been started


  Scenario: User fails to recall archive if there is no space enough on device
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks and presses enter on item named "dir1" in file browser

    # number of files that are being recalled must be greater than number of
    # files recalled parallelly (as of 14.03.2022 it's 20 files) to make sure
    # that quota will be exceeded
    And user of browser uses upload button from file browser menu bar to upload 50 local files "file.txt" to remote current dir
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser creates dataset for item "dir1" in "space1"
    And user of browser succeeds to create archive for item "dir1" in "space1" with following configuration:
        description: first archive
        layout: plain
    And user of browser clicks on menu for archive with description: "first archive" in archive browser
    And user of browser clicks "Recall to..." option in data row menu in archive browser
    And user of browser writes "dir1_recalled" into target name input text field in modal "Recall archive"
    And user of browser clicks on "Recall" button in modal "Recall archive"
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on recalled status tag for "dir1_recalled" in file browser
    Then user of browser sees status: "Archive recall finished with errors" in archive recall information modal
    And user of browser sees that not all files were recalled
    And user of browser sees that not all data were recalled
    And user of browser sees last error: "No space left on device" in archive recall information modal
    And user of browser sees that number of items failed is greater than 0

