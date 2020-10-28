Feature: Quality of Service in directory tests for 2 providers using multiple browsers in Oneprovider GUI


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
                - oneprovider-2:
                    storage: posix
                    size: 1000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1
                    - file1: 11111111

    And users opened [browser_unified, browser_emergency] browsers' windows
    And users of [browser_unified, browser_emergency] opened [Onezone, oneprovider-2 provider panel] page
    And user of [browser_unified, browser_emergency] logged as [user1, admin] to [Onezone, emergency interface of Onepanel] service


  Scenario: User successfully uploads file to directory with QoS requirement
    When user of browser_unified clicks "space1" on the spaces list in the sidebar
    And user of browser_unified clicks Data of "space1" in the sidebar
    And user of browser_unified sees file browser in data tab in Oneprovider page

    And user of browser_emergency clicks on Storages item in submenu of "oneprovider-2" item in CLUSTERS sidebar in Onepanel
    And user of browser_emergency expands "posix" record on storages list in storages page in Onepanel
    And user of browser_emergency copies id of "posix" storage to clipboard via copy button
    And user of browser_unified creates QoS requirement with copied storageId for "dir1" from file browser
    And user of browser_unified double clicks on item named "dir1" in file browser
    And user of browser_unified uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
    And user of browser_unified clicks on QoS status tag for "20B-0.txt" in file browser
    And user of browser_unified sees that all QoS requirements are fulfilled
    And user of browser_unified clicks on "Close" button in modal "Quality of Service"
    Then user of browser_unified sees file chunks for file "20B-0.txt" as follows:
        oneprovider-1: entirely filled
        oneprovider-2: entirely filled


  Scenario: File is replicated from one storage to storage which id was set as QoS requirement
    When user of browser_unified clicks "space1" on the spaces list in the sidebar
    And user of browser_unified clicks Data of "space1" in the sidebar
    And user of browser_unified sees file browser in data tab in Oneprovider page
    And user of browser_unified sees file chunks for file "file1" as follows:
          oneprovider-1: entirely filled
          oneprovider-2: never synchronized

    And user of browser_emergency clicks on Storages item in submenu of "oneprovider-2" item in CLUSTERS sidebar in Onepanel
    And user of browser_emergency expands "posix" record on storages list in storages page in Onepanel
    And user of browser_emergency copies id of "posix" storage to clipboard via copy button
    And user of browser_unified creates QoS requirement with copied storageId for "file1" from file browser
    And user of browser_unified clicks on QoS status tag for "file1" in file browser
    And user of browser_unified sees that all QoS requirements are fulfilled
    And user of browser_unified clicks on "Close" button in modal "Quality of Service"
    Then user of browser_unified sees file chunks for file "file1" as follows:
          oneprovider-1: entirely filled
          oneprovider-2: entirely filled
