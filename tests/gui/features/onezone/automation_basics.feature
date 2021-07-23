Feature: Basic workflow management


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: space-owner-user
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
#            storage:
#                defaults:
#                    provider: oneprovider-1
#                directory tree:
#                    - dir1
#                    - dir2:
#                        - file1: 100
#                        - file2: 200


    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario: User creates and renames inventory
    When user of browser clicks on Automation in the main menu
    And user of browser clicks on Create automation inventory button in automation sidebar
    And user of browser writes "inventory1" into inventory name text field
    And user of browser clicks on confirmation button

    And user of browser clicks on "Rename" button in inventory "inventory1" menu in the sidebar
    And user of browser writes "inventory2" into rename inventory text field
    And user of browser confirms inventory rename using <confirmation_method>
    Then user of browser sees inventory "inventory2" on inventory list


  Scenario: User removes inventory
    When user of browser clicks on Automation in the main menu
    And user of browser clicks on Create automation inventory button in automation sidebar
    And user of browser writes "inventory1" into inventory name text field
    And user of browser clicks on confirmation button

    And user of browser clicks on "Remove" button in inventory "inventory1" menu in the sidebar
    And user of browser clicks on "Remove" button in modal "remove_inventory"
    Then user of browser does not see inventory "inventory1" on inventory list


  Scenario: User leaves inventory
    When user of browser clicks on Automation in the main menu
    And user of browser clicks on Create automation inventory button in automation sidebar
    And user of browser writes "inventory1" into inventory name text field
    And user of browser clicks on confirmation button

    And user of browser clicks on "Leave" button in inventory "inventory1" menu in the sidebar
    And user of browser clicks on "Leave" button in modal "leave_inventory"
    Then user of browser does not see inventory "inventory1" on inventory list
