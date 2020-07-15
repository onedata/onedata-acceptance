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

    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, oneprovider-2 provider panel] page
    And user of [browser1, browser2] logged as [user1, admin] to [Onezone, emergency interface of Onepanel] service

    Scenario: Adding provider to meet quality of service requirement
      When user of browser1 creates 2 replicas of "anyStorage" quality of service for "file1"
      And user of browser1 clicks on qos status tag for "file1" in file browser
      And user of browser1 sees that all qualities of service are impossible
      And user of browser1 clicks on "Close" button in modal "Quality of Service"
      And user of browser1 clicks Overview of "space1" in the sidebar
      And user of browser1 sends support token for "space1" to user of browser2
      And user of browser2 supports "space1" space in "oneprovider-2" Oneprovider panel service with following configuration:
          storage: posix
          size: 100
          unit: MiB
      Then user of browser1 clicks Data of "space1" in the sidebar
      And user of browser1 sees file browser in data tab in Oneprovider page
      And user of browser1 clicks on qos status tag for "file1" in file browser
      And user of browser1 sees that all qualities of service are fulfilled