Feature: Quality of Service tests using single storage and single browser in Oneprovider GUI


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


  Scenario: User sees QoS file status and entries after adding QoS requirements to file
    When user of browser opens file browser for "space1" space
    And user of browser clicks once on item named "file1" in file browser
    And user of browser chooses Quality of Service option from selection menu on file browser page
    And user of browser clicks on "Add Requirement" button in modal "Quality of Service"
    And user of browser clicks "enter as text" label in "Quality of Service" modal
    And user of browser writes "geo=PL" into expression text field in modal "Quality of Service"
    And user of browser confirms entering expression in expression text field in modal "Quality of Service"
    And user of browser sees that replicas number is equal 1 in modal "Quality of Service"
    And user of browser clicks on "Save" button in modal "Quality of Service"
    And user of browser clicks on "Close" button in modal "Quality of Service"
    Then user of browser sees QoS status tag for "file1" in file browser
    And user of browser chooses Quality of Service option from selection menu on file browser page
    And user of browser sees [geo="PL"] QoS requirement in modal "Quality of Service"


  Scenario: User sees that there is no QoS file status and entries after deleting QoS requirements from file
    When user of browser creates "geo=PL" QoS requirement for "file1" in space "space1"
    And user of browser sees QoS status tag for "file1" in file browser
    And user of browser clicks on QoS status tag for "file1" in file browser
    And user of browser deletes all QoS requirements
    And user of browser clicks on "Close" button in modal "Quality of Service"
    Then user of browser does not see QoS status tag for "file1" in file browser
    And user of browser doesn't see any QoS requirement in modal "Quality of Service"


  Scenario: User sees that QoS becomes fulfilled shortly after adding already fulfilled requirement
    When user of browser creates "anyStorage" QoS requirement for "file1" in space "space1"
    And user of browser clicks on QoS status tag for "file1" in file browser
    Then user of browser sees that all QoS requirements are fulfilled


  Scenario: User sees that QoS becomes impossible shortly after adding impossible to fulfill requirement
    When user of browser creates "hello=WORLD" QoS requirement for "file1" in space "space1"
    Then user of browser clicks on QoS status tag for "file1" in file browser
    And user of browser sees that all QoS requirements are impossible
