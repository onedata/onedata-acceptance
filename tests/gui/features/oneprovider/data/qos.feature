Feature: Quality of Service tests using single browser in Oneprovider GUI


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


    Scenario: User successfully adds QoS requirement
      When user of browser opens file browser for "space1" space
      And user of browser clicks once on item named "file1" in file browser
      And user of browser chooses Quality of Service option from selection menu on file browser page
      And user of browser clicks on "Add Requirement" button in modal "Quality of Service"
      And user of browser writes "geo=PL" into default text field in modal "Quality of Service"
      And user of browser clicks on "Save" button in modal "Quality of Service"
      And user of browser clicks on "Close" button in modal "Quality of Service"
      Then user of browser sees QoS status tag for "file1" in file browser


    Scenario: User successfully deletes QoS requirement
      When user of browser creates "geo=PL" QoS requirement for "file1" in space "space1"
      And user of browser sees QoS status tag for "file1" in file browser
      And user of browser clicks on QoS status tag for "file1" in file browser
      And user of browser deletes all QoS requirements
      And user of browser clicks on "CLose" button in modal "Quality of Service"
      Then user of browser does not see QoS status tag for "file1" in file browser


    Scenario: User successfully adds fulfilled QoS requirement
      When user of browser creates "anyStorage" QoS requirement for "file1" in space "space1"
      And user of browser clicks on QoS status tag for "file1" in file browser
      Then user of browser sees that all QoS requirements are fulfilled


    Scenario: User successfully adds impossible QoS requirement
      When user of browser creates "hello=WORLD" QoS requirement for "file1" in space "space1"
      Then user of browser clicks on QoS status tag for "file1" in file browser
      And user of browser sees that all QoS requirements are impossible
