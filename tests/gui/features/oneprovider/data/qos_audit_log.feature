Feature: Audit log for QoS


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
                        - file1
                        - file2
    And opened browser with user1 signed in to "onezone" service

  Scenario: sssds
    When user of browser clicks on Providers in the main menu
    And user of browser clicks on provider "oneprovider-2" in providers sidebar
    And user of browser opens file browser for "space1" space

    And user of browser opens "File details" modal on "QoS" tab for "dir1" file using context menu
    And user of browser clicks on "Add Requirement" button in QoS panel

    And user of browser clicks on add query block icon in QoS panel
    And user of browser chooses "provider" property in "Add QoS condition" popup

    And user of browser sees ["oneprovider-1", "oneprovider-2"] provider on values list in "Add QoS condition" popup
    And user of browser chooses value of "oneprovider-2" provider in "Add QoS condition" popup
    And user of browser clicks "Add" in "Add QoS condition" popup
    And user of browser clicks on "Save" button in QoS panel

    #And user of browser clicks on QoS status tag for "dir1" in file browser
    And user of browser sees that all QoS requirements are fulfilled
