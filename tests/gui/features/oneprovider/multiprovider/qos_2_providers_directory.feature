Feature: Quality of Service in directory tests for 2 providers using sigle browser in Oneprovider GUI


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
                    - dir1:
                        - file1: 11111

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service

  Scenario: Inheriting quality of service after directory
    When user of browser creates 2 replicas of "anyStorage" quality of service for "dir1"
    Then user of browser double clicks on item named "dir1" in file browser
    And user of browser sees qos status tag for "file1" in file browser
    And user of browser clicks on qos status tag for "file1" in file browser
    And user of browser sees that all qualities of service are fulfilled
    And user of browser clicks on "Close" button in modal "Quality of Service"
    And user of browser sees file chunks for file "file1" as follows:
          oneprovider-1: entirely filled
          oneprovider-2: entirely filled