Feature: Quality of Service tests for 2 providers using sigle browser in Oneprovider GUI

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

    Scenario: Adding "anyStorage" quality of service with 2 replicas
      When user of browser creates 2 replicas of "anyStorage" quality of service for "file1"
      Then user of browser clicks on qos status tag for "file1" in file browser
      And user of browser sees that all qualities of service are fulfilled
      And user of browser clicks on "Close" button in modal "Quality of Service"
      And user of browser sees file chunks for file "file1" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely filled
