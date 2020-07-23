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

    And users opened [browser_unified, browser_emergency] browsers' windows
    And users of [browser_unified, browser_emergency] opened [Onezone, oneprovider-2 provider panel] page
    And user of [browser_unified, browser_emergency] logged as [user1, admin] to [Onezone, emergency interface of Onepanel] service


    Scenario: Adding storage id as qos requirement
      When user of browser_unified clicks "space1" on the spaces list in the sidebar
      And user of browser_unified clicks Data of "space1" in the sidebar
      And user of browser_unified sees file browser in data tab in Oneprovider page
      And user of browser_unified sees file chunks for file "file1" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: never synchronized

      And user of browser_emergency clicks on Storages item in submenu of "oneprovider-2" item in CLUSTERS sidebar in Onepanel
      And user of browser_emergency expands "posix" record on storages list in storages page in Onepanel
      And user of browser_emergency copies id of "posix" storage to clipboard via copy button
      And user of browser_unified copies storageId quality of service from clipboard for "file1" from file browser
      Then user of browser_unified clicks on qos status tag for "file1" in file browser
      And user of browser_unified sees that all qos requirements are fulfilled
      And user of browser_unified clicks on "Close" button in modal "Quality of Service"
      And user of browser_unified sees file chunks for file "file1" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely filled


    Scenario: Auto-cleaning with qos requirement set
      When user of browser_emergency clicks on Spaces item in submenu of "oneprovider-2" item in CLUSTERS sidebar in Onepanel
      And user of browser_emergency opens "space1" record on spaces list in Spaces page in Onepanel
      And user of browser_emergency clicks on File popularity navigation tab in space "space1"
      And user of browser_emergency enables file-popularity in "space1" space in Onepanel
      And user of browser_emergency is idle for 8 seconds
      And user of browser_emergency clicks on "Auto cleaning" navigation tab in space "space1"
      And user of browser_emergency enables auto-cleaning in "space1" space in Onepanel
      And user of browser_unified uploads "20B-0.txt" to the root directory of "space1"
      And user of browser_unified uses upload button from file browser menu bar to upload file "large_file.txt" to current dir
      And user of browser_unified clicks on Data in the main menu
      And user of browser_unified creates 2 replicas of "anyStorage" qos requirement for "large_file.txt"
      And user of browser_unified replicates "20B-0.txt" to provider "oneprovider-2"
      And user of browser_emergency is idle for 8 seconds

      And user of browser_emergency clicks change soft quota button in auto-cleaning tab in Onepanel
      And user of browser_emergency types "0.1" to soft quota input field in auto-cleaning tab in Onepanel
      And user of browser_emergency confirms changing value of soft quota in auto-cleaning tab in Onepanel
      And user of browser_emergency clicks change hard quota button in auto-cleaning tab in Onepanel
      And user of browser_emergency types "0.2" to hard quota input field in auto-cleaning tab in Onepanel
      And user of browser_emergency confirms changing value of hard quota in auto-cleaning tab in Onepanel
      And user of browser_emergency clicks on "Start cleaning now" button in auto-cleaning tab in Onepanel
      And user of browser_emergency is idle for 25 seconds

      Then user of browser_emergency sees 20 B released size in cleaning report in Onepanel
      And user of browser_unified sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely filled
      And user of browser_unified sees file chunks for file "20B-0.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely empty