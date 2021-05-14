Feature: Quality of Service in directory tests for 2 providers with 1 supporting in Oneprovider GUI


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
          storage:
            defaults:
              provider: oneprovider-1
            directory tree:
              - file1: 11111111

    And users opened [browser_unified, browser_emergency] browsers' windows
    And users of [browser_unified, browser_emergency] opened [Onezone, oneprovider-2 provider panel] page
    And user of [browser_unified, browser_emergency] logged as [user1, admin] to [Onezone, emergency interface of Onepanel] service


  Scenario: User sees QoS requirement met after a new support is added
    When user of browser_unified creates 2 replicas of "anyStorage" QoS requirement for "file1" in space "space1"
    And user of browser_unified clicks on QoS status tag for "file1" in file browser
    And user of browser_unified sees that all QoS requirements are impossible
    And user of browser_unified sees that 1 storage matches condition in modal "Quality of Service"
    And user of browser_unified sees that matching storage is "posix provided by oneprovider-1"
    And user of browser_unified clicks on "Close" button in modal "Quality of Service"
    And user of browser_unified clicks Overview of "space1" in the sidebar
    And user of browser_unified sends support token for "space1" to user of browser_emergency
    And user of browser_emergency supports "space1" space in "oneprovider-2" Oneprovider panel service with following configuration:
        storage: posix
        size: 100
        unit: MiB
    And user of browser_unified clicks Files of "space1" in the sidebar
    And user of browser_unified sees file browser in data tab in Oneprovider page
    And user of browser_unified clicks on QoS status tag for "file1" in file browser
    Then user of browser_unified sees that all QoS requirements are fulfilled
    And user of browser_unified sees that 2 storages match condition in modal "Quality of Service"
    And user of browser_unified sees that matching storages are ["posix provided by oneprovider-1", "posix provided by oneprovider-2"]


  Scenario: User can select one of supporting providers in QoS graphical editor and it causes to match its storage
    When user of browser_unified opens file browser for "space1" space
    And user of browser_unified opens "Quality of Service" modal for "file1" file
    And user of browser_unified clicks on "Add Requirement" button in modal "Quality of Service"

    And user of browser_unified clicks on add query block icon in modal "Quality of Service"
    And user of browser_unified chooses "provider" property in "Add QoS condition" popup

    And user of browser_unified sees "oneprovider-1" provider on values list in "Add QoS condition" popup
    And user of browser_unified chooses value of "oneprovider-1" provider in "Add QoS condition" popup
    And user of browser_unified clicks "Add" in "Add QoS condition" popup
    And user of browser_unified sees that 1 storage matches condition in modal "Quality of Service"
    And user of browser_unified sees that matching storage is "posix provided by oneprovider-1"

    And user of browser_unified clicks on "Save" button in modal "Quality of Service"
    Then user of browser_unified sees [provider is oneprovider-1] QoS requirement in modal "Quality of Service"
    And user of browser_unified sees that all QoS requirements are fulfilled
