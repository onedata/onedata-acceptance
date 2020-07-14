Feature: Quality of Service tests for 2 providers using multiple browsers in Oneprovider GUI

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And there are no spaces supported by oneprovider-2 in Onepanel
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000000
                - oneprovider-2:
                    storage: posix
                    size: 1000000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - file1: 11111111

    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, oneprovider-2 provider panel] page
    And user of [browser1, browser2] logged as [user1, admin] to [Onezone, emergency interface of Onepanel] service


    Scenario: Adding storage id as quality of service
      When user of browser1 clicks "space1" on the spaces list in the sidebar
      And user of browser1 clicks Data of "space1" in the sidebar
      And user of browser1 sees file browser in data tab in Oneprovider page
      And user of browser1 sees file chunks for file "file1" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: never synchronized

      And user of browser2 clicks on Storages item in submenu of "oneprovider-2" item in CLUSTERS sidebar in Onepanel
      And user of browser2 expands "posix" record on storages list in storages page in Onepanel
      And user of browser2 copies id of "posix" storage to clipboard via copy button
      And user of browser1 copies storageId quality of service from clipboard for "file1" from file browser
      Then user of browser1 clicks on qos status tag for "file1" in file browser
      And user of browser1 sees that all qualities of service are fulfilled
      And user of browser1 clicks on "Close" button in modal "Quality of Service"
      And user of browser1 sees file chunks for file "file1" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely filled


    Scenario: Auto-cleaning with quality of service set
      When user of browser2 clicks on Spaces item in submenu of "oneprovider-2" item in CLUSTERS sidebar in Onepanel
      And user of browser2 opens "space1" record on spaces list in Spaces page in Onepanel
      And user of browser2 clicks on File popularity navigation tab in space "space1"
      And user of browser2 enables file-popularity in "space1" space in Onepanel
      And user of browser2 is idle for 8 seconds
      And user of browser2 clicks on "Auto cleaning" navigation tab in space "space1"
      And user of browser2 enables auto-cleaning in "space1" space in Onepanel
      And user of browser1 uploads "20B-0.txt" to the root directory of "space1"
      And user of browser1 uses upload button from file browser menu bar to upload file "large_file.txt" to current dir
      And user of browser1 clicks on Data in the main menu
      And user of browser1 creates 2 replicas of "anyStorage" quality of service for "large_file.txt"
      And user of browser1 replicates "20B-0.txt" to provider "oneprovider-2"
      And user of browser2 is idle for 8 seconds

      And user of browser2 clicks change soft quota button in auto-cleaning tab in Onepanel
      And user of browser2 types "0.1" to soft quota input field in auto-cleaning tab in Onepanel
      And user of browser2 confirms changing value of soft quota in auto-cleaning tab in Onepanel
      And user of browser2 clicks change hard quota button in auto-cleaning tab in Onepanel
      And user of browser2 types "0.2" to hard quota input field in auto-cleaning tab in Onepanel
      And user of browser2 confirms changing value of hard quota in auto-cleaning tab in Onepanel
      And user of browser2 clicks on "Start cleaning now" button in auto-cleaning tab in Onepanel
      And user of browser2 is idle for 25 seconds

      Then user of browser2 sees 20 B released size in cleaning report in Onepanel
      And user of browser1 sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely filled
      And user of browser1 sees file chunks for file "20B-0.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely empty