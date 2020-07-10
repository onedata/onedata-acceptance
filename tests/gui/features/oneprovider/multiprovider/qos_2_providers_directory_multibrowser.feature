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

    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, oneprovider-2 provider panel] page
    And user of [browser1, browser2] logged as [user1, admin] to [Onezone, emergency interface of Onepanel] service

    Scenario: Uploading file to directory with quality of service
      When user of browser1 clicks "space1" on the spaces list in the sidebar
      And user of browser1 clicks Data of "space1" in the sidebar
      And user of browser1 sees file browser in data tab in Oneprovider page

      And user of browser2 clicks on Storages item in submenu of "oneprovider-2" item in CLUSTERS sidebar in Onepanel
      And user of browser2 expands "posix" record on storages list in storages page in Onepanel
      And user of browser2 copies id of "posix" storage to clipboard via copy button
      And user of browser1 copies storageId quality of service from clipboard for "dir1" from file browser
      And user of browser1 double clicks on item named "dir1" in file browser
      And user of browser1 uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
      Then user of browser1 clicks on qos status tag for "20B-0.txt" in file browser
      And user of browser1 sees that all qualities of service are fulfilled
      And user of browser1 clicks on "Close" button in modal "Quality of Service"
      And user of browser1 sees file chunks for file "20B-0.txt" as follows:
          oneprovider-1: entirely filled
          oneprovider-2: entirely filled