Feature: Quality of Service tests for 2 providers using multiple browsers where second is provider panel of the same provider that supports space in Oneprovider GUI


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
    And users of [browser_unified, browser_emergency] opened [Onezone, oneprovider-1 provider panel] page
    And user of [browser_unified, browser_emergency] logged as [user1, admin] to [Onezone, emergency interface of Onepanel] service
    And user of browser_emergency clicks on Storages item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And there are no additional params in storage edit page used by browser_emergency


  Scenario: File is replicated after migration from one storage with QoS requirement
    When user of browser_unified opens "oneprovider-1" Oneprovider file browser for "space1" space
    And user of browser_emergency expands "posix" record on storages list in storages page in Onepanel
    And user of browser_emergency copies id of "posix" storage to clipboard via copy button
    And user of browser_unified creates QoS requirement with copied storageId for "file1" from file browser
    And user of browser_unified clicks on QoS status tag for "file1" in file browser
    And user of browser_unified sees that all QoS requirements are fulfilled
    And user of browser_unified clicks on "Close" button in modal "Quality of Service"
    And user of browser_unified migrates "file1" from provider "oneprovider-1" to provider "oneprovider-2"
    Then user of browser_unified sees file chunks for file "file1" as follows:
          oneprovider-1: entirely filled
          oneprovider-2: entirely filled


  Scenario: User successfully adds "anyStorage - storageId" QoS requirement
    When user of browser_unified opens "oneprovider-1" Oneprovider file browser for "space1" space
    And user of browser_emergency expands "posix" record on storages list in storages page in Onepanel
    And user of browser_emergency copies id of "posix" storage to clipboard via copy button
    And user of browser_unified creates "anyStorage \ storageId=" QoS requirement and pastes storage id from clipboard for "file1" from file browser
    And user of browser_unified clicks on QoS status tag for "file1" in file browser
    And user of browser_unified sees that all QoS requirements are fulfilled
    And user of browser_unified clicks on "Close" button in modal "Quality of Service"
    Then user of browser_unified sees file chunks for file "file1" as follows:
          oneprovider-2: entirely filled


  Scenario: A single key-value based QoS requirement is met after adding this QoS parameter to storage
    When user of browser_unified creates "type2=posix2" QoS requirement for "file1" in space "space1"
    And user of browser_unified clicks on QoS status tag for "file1" in file browser
    And user of browser_unified sees that all QoS requirements are impossible
    And user of browser_emergency clicks on "Modify" button for "posix" storage record in Storages page in Onepanel
    And user of browser_emergency adds key="type2" value="posix2" in storage edit page
    Then user of browser_unified sees that all QoS requirements are fulfilled


  Scenario: A QoS requirement with "and" operator is met after adding this QoS parameter to storage
    When user of browser_unified creates "type=posix & geo=PL" QoS requirement for "file1" in space "space1"
    And user of browser_unified clicks on QoS status tag for "file1" in file browser
    And user of browser_unified sees that all QoS requirements are impossible
    And user of browser_emergency clicks on "Modify" button for "posix" storage record in Storages page in Onepanel
    And user of browser_emergency adds key="type" value="posix" in storage edit page
    And user of browser_unified is idle for 8 seconds
    And user of browser_unified sees that all QoS requirements are impossible
    And user of browser_emergency clicks on "Modify" button for "posix" storage record in Storages page in Onepanel
    And user of browser_emergency adds key="geo" value="PL" in storage edit page
    Then user of browser_unified sees that all QoS requirements are fulfilled


  Scenario: A QoS requirement with "or" operator is met after adding this QoS parameter to storage
    When user of browser_unified creates "type=posix | geo=PL" QoS requirement for "file1" in space "space1"
    And user of browser_unified clicks on QoS status tag for "file1" in file browser
    And user of browser_unified sees that all QoS requirements are impossible
    And user of browser_emergency clicks on "Modify" button for "posix" storage record in Storages page in Onepanel
    And user of browser_emergency adds key="type" value="posix" in storage edit page
    And user of browser_unified sees that all QoS requirements are fulfilled
    And user of browser_emergency deletes all additional params in storage edit page
    And user of browser_emergency clicks on "Modify" button for "posix" storage record in Storages page in Onepanel
    And user of browser_emergency adds key="geo" value="PL" in storage edit page
    Then user of browser_unified sees that all QoS requirements are fulfilled
