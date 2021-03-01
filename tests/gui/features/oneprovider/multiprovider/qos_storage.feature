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
    And user of browser_unified sees that no storage matches condition in modal "Quality of Service"
    And user of browser_emergency clicks on "Modify" button for "posix" storage record in Storages page in Onepanel
    And user of browser_emergency adds key="type2" value="posix2" in storage edit page
    Then user of browser_unified sees that all QoS requirements are fulfilled
    And user of browser_unified sees that 1 storage matches condition in modal "Quality of Service"
    And user of browser_unified sees that matching storage is "posix provided by oneprovider-1"


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


  Scenario: A QoS requirement with "or" operator is met only if minimum one of these QoS parameters is in storage
    When user of browser_unified creates "type=posix | geo=PL" QoS requirement for "file1" in space "space1"
    And user of browser_unified clicks on QoS status tag for "file1" in file browser
    And user of browser_unified sees that all QoS requirements are impossible
    And user of browser_emergency clicks on "Modify" button for "posix" storage record in Storages page in Onepanel
    And user of browser_emergency adds key="type" value="posix" in storage edit page
    And user of browser_unified sees that all QoS requirements are fulfilled
    And user of browser_emergency deletes all additional params in storage edit page
    And user of browser_unified sees that all QoS requirements are impossible
    And user of browser_emergency clicks on "Modify" button for "posix" storage record in Storages page in Onepanel
    And user of browser_emergency adds key="geo" value="PL" in storage edit page
    Then user of browser_unified sees that all QoS requirements are fulfilled


  Scenario: A QoS requirement with "or" operator is met after adding one of these QoS parameters to storage
    When user of browser_unified creates "type=posix | geo=PL" QoS requirement for "file1" in space "space1"
    And user of browser_unified clicks on QoS status tag for "file1" in file browser
    And user of browser_unified sees that all QoS requirements are impossible
    And user of browser_emergency clicks on "Modify" button for "posix" storage record in Storages page in Onepanel
    And user of browser_emergency adds key="type" value="posix" in storage edit page
    Then user of browser_unified sees that all QoS requirements are fulfilled


  Scenario: User can select one of storages of supporting providers in QoS graphical editor and it causes to match this storage
    When user of browser_unified opens file browser for "space1" space
    And user of browser_unified opens "Quality of Service" modal for "file1" file
    And user of browser_unified clicks on "Add Requirement" button in modal "Quality of Service"

    And user of browser_unified clicks on add query block icon in modal "Quality of Service"
    And user of browser_unified chooses "storage" property in "Add QoS condition" popup

    And user of browser_unified sees ["posix @oneprovider-1", "posix @oneprovider-2"] storages on values list in "Add QoS condition" popup
    And user of browser_unified chooses value of "posix" at "oneprovider-1" in "Add QoS condition" popup
    And user of browser_unified clicks "Add" in "Add QoS condition" popup

    And user of browser_unified clicks on "Save" button in modal "Quality of Service"
    Then user of browser_unified sees [storage is posix @oneprovider-1] QoS requirement in modal "Quality of Service"
    And user of browser_unified sees that all QoS requirements are fulfilled
    And user of browser_unified sees that 1 storage matches condition in modal "Quality of Service"
    And user of browser_unified sees that matching storage is "posix provided by oneprovider-1"


  Scenario: Every possible storage matches when "any storage" condition is chosen
    When user of browser_unified opens file browser for "space1" space
    And user of browser_unified opens "Quality of Service" modal for "file1" file
    And user of browser_unified clicks on "Add Requirement" button in modal "Quality of Service"

    And user of browser_unified clicks on add query block icon in modal "Quality of Service"
    And user of browser_unified chooses "any storage" property in "Add QoS condition" popup
    And user of browser_unified clicks "Add" in "Add QoS condition" popup

    And user of browser_unified clicks on "Save" button in modal "Quality of Service"
    Then user of browser_unified sees [any storage] QoS requirement in modal "Quality of Service"
    And user of browser_unified sees that all QoS requirements are fulfilled
    And user of browser_unified sees that 2 storages match condition in modal "Quality of Service"
    And user of browser_unified sees that matching storages are ["posix provided by oneprovider-1", "posix provided by oneprovider-2"]


  Scenario: User sees matching storages count changing while editing nested expression in QoS visual editor and submits the expression successfully
    When user of browser_emergency adds "test_storage" storage in "oneprovider-1" Oneprovider panel service with following configuration:
          storage type: POSIX
          mount point: /volumes/persistence/storage
    And user of browser_unified opens file browser for "space1" space
    And user of browser_unified opens "Quality of Service" modal for "file1" file
    And user of browser_unified clicks on "Add Requirement" button in modal "Quality of Service"

    # (provider is oneprovider-1) AND (storage is posix @oneprovider-2 OR storage is posix @oneprovider-1) AND
    # (any storage EXCEPT storage is posix @oneprovider-1)
    And user of browser_unified clicks on add query block icon in modal "Quality of Service"
    And user of browser_unified chooses "AND" operator in "Add QoS condition" popup

    # provider is oneprovider-1
    And user of browser_unified clicks on add query block icon in modal "Quality of Service"
    And user of browser_unified chooses "provider" property in "Add QoS condition" popup
    And user of browser_unified chooses value of "oneprovider-1" provider in "Add QoS condition" popup
    And user of browser_unified clicks "Add" in "Add QoS condition" popup

    And user of browser_unified sees that 1 storage matches condition in modal "Quality of Service"

    # (storage is posix @oneprovider-1 OR storage is posix @oneprovider-2)
    And user of browser_unified clicks on add query block icon in modal "Quality of Service"
    And user of browser_unified chooses "OR" operator in "Add QoS condition" popup

    # storage is posix @oneprovider-2
    And user of browser_unified clicks on add query block icon in modal "Quality of Service"
    And user of browser_unified chooses "storage" property in "Add QoS condition" popup
    And user of browser_unified chooses value of "posix" at "oneprovider-2" in "Add QoS condition" popup
    And user of browser_unified clicks "Add" in "Add QoS condition" popup

    And user of browser_unified sees that no storage matches condition in modal "Quality of Service"

    # storage is posix @oneprovider-1
    And user of browser_unified clicks on add query block icon in modal "Quality of Service"
    And user of browser_unified chooses "storage" property in "Add QoS condition" popup
    And user of browser_unified chooses value of "posix" at "oneprovider-1" in "Add QoS condition" popup
    And user of browser_unified clicks "Add" in "Add QoS condition" popup

    And user of browser_unified sees that 1 storage matches condition in modal "Quality of Service"

    # (any storage EXCEPT storage is posix @oneprovider-1)
    And user of browser_unified clicks on 2 nd from the left add query block icon in modal "Quality of Service"
    And user of browser_unified chooses "EXCEPT" operator in "Add QoS condition" popup

    # any storage
    And user of browser_unified clicks on 2 nd from the left add query block icon in modal "Quality of Service"
    And user of browser_unified chooses "any storage" property in "Add QoS condition" popup
    And user of browser_unified clicks "Add" in "Add QoS condition" popup

    # storage is posix @oneprovider-1
    And user of browser_unified clicks on 2 nd from the left add query block icon in modal "Quality of Service"
    And user of browser_unified chooses "storage" property in "Add QoS condition" popup
    And user of browser_unified chooses value of "posix" at "oneprovider-1" in "Add QoS condition" popup
    And user of browser_unified clicks "Add" in "Add QoS condition" popup

    And user of browser_unified sees that no storage matches condition in modal "Quality of Service"

    And user of browser_unified clicks on "Save" button in modal "Quality of Service"
    Then user of browser_unified sees nested QoS requirement in modal "Quality of Service":
           [[provider is oneprovider-1] AND [storage is posix @oneprovider-2 OR storage is posix @oneprovider-1] AND [any storage EXCEPT storage is posix @oneprovider-1]]
