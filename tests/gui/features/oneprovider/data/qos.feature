Feature: Quality of Service tests using sigle browser in Oneprovider GUI

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
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - file1

    And opened browser with user1 signed in to "onezone" service

    Scenario: Adding quality of service
      When user of browser creates "geo=PL" quality of service for "file1"
      Then user of browser sees qos status tag for "file1" in file browser

    Scenario: Deleting quality of service
      When user of browser creates "geo=PL" quality of service for "file1"
      And user of browser sees qos status tag for "file1" in file browser
      And user of browser clicks on qos status tag for "file1" in file browser
      And user of browser deletes all qualities of service
      And user of browser clicks on "CLose" button in modal "Quality of Service"
      Then user of browser does not see qos status tag for "file1" in file browser

    Scenario: Adding fulfilled qos
      When user of browser creates "anyStorage" quality of service for "file1"
      Then user of browser clicks on qos status tag for "file1" in file browser
      And user of browser sees all qualities of service are fulfilled

    Scenario: Adding impossible qos
      When user of browser creates "hello=WORLD" quality of service for "file1"
      Then user of browser clicks on qos status tag for "file1" in file browser
      And user of browser sees all qualities of service are impossible
