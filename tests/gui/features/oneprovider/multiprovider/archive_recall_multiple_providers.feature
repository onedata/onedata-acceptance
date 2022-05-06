Feature: Archive recall tests using multiple providers

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
          space1:
              owner: space-owner-user
              providers:
                  - oneprovider-1:
                      storage: posix
                      size: 110000000
                  - oneprovider-2:
                      storage: posix
                      size: 110000000
              storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1
    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service
    And directory tree structure on local file system:
          browser:
              large_file.txt:
                size: 20 MiB


  Scenario: User sees that recall has been cancelled after cancelling it on remote provider
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload local file "large_file.txt" to remote current dir
    And user of browser creates dataset for item "large_file.txt" in "space1"
    And user of browser succeeds to create archive for item "large_file.txt" in "space1" with following configuration:
        description: first archive
        layout: plain
    And user of browser waits for "Preserved" state for archive with description "first archive" in archive browser

    And user of browser clicks on menu for archive with description: "first archive" in archive browser
    And user of browser clicks "Recall to..." option in data row menu in archive browser
    And user of browser writes "file_recalled.txt" into target name input text field in modal "Recall archive"
    And user of browser clicks on "Recall" button in modal "Recall archive"
    And user of browser clicks on Choose other Oneprovider on file browser page
    And user of browser clicks on "oneprovider-2" provider on file browser page
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on recalling status tag for "file_recalled.txt" in file browser
    And user of browser clicks on "Cancel recall" button in modal "Archive recall information"
    And user of browser clicks on "Yes" button in modal "Cancel recall"

    Then user of browser waits for status "Cancelled" in archive recall information modal
    And user of browser sees status: "Cancelled" in archive recall information modal
    And user of browser sees that recall has been cancelled at the same time or after recall has been started
    And user of browser sees that recall has been finished at the same time or after recall has been cancelled
    And user of browser sees Recalling Oneprovider: "dev-oneprovider-krakow" in archive recall information modal
    And user of browser fails to see statistics of files recalled in archive recall information modal
    And user of browser fails to see statistics of data recalled in archive recall information modal
