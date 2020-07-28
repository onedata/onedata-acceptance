Feature: Quality of Service tests for 2 providers using single browser in Oneprovider GUI


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
                    - file1: 11111111

    And opened browser with user1 signed in to "onezone" service


  Scenario: User successfully adds "anyStorage" QoS requirement with 2 replicas
    When user of browser creates 2 replicas of "anyStorage" QoS requirement for "file1" in space "space1"
    Then user of browser clicks on QoS status tag for "file1" in file browser
    And user of browser sees that all QoS requirements are fulfilled
    And user of browser clicks on "Close" button in modal "Quality of Service"
    And user of browser sees file chunks for file "file1" as follows:
          oneprovider-1: entirely filled
          oneprovider-2: entirely filled


  Scenario: User successfully evicts from storage with QoS requirement with 2 replicas
    When user of browser creates 2 replicas of "anyStorage" QoS requirement for "file1" in space "space1"
    And user of browser clicks on QoS status tag for "file1" in file browser
    And user of browser sees that all QoS requirements are fulfilled
    And user of browser clicks on "Close" button in modal "Quality of Service"
    And user of browser sees file chunks for file "file1" as follows:
          oneprovider-1: entirely filled
          oneprovider-2: entirely filled
    And user of browser evicts "file1" from provider "oneprovider-2"
    And user of browser waits until eviction is done

    Then user of browser sees file chunks for file "file1" as follows:
          oneprovider-1: entirely filled
          oneprovider-2: entirely filled
    And user of browser clicks on Choose other Oneprovider on file browser page
    And user of browser clicks on "oneprovider-2" provider on file browser page
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser sees only items named "file1" in file browser
