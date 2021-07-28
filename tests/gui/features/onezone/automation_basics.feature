Feature: Basic inventories management


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
    And initial inventories configuartion in "onezone" Onezone service:


    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario: User creates inventory
    When user of browser clicks on Automation in the main menu
    And user of browser clicks on Create automation inventory button in automation sidebar
    And user of browser writes "inventory2" into inventory name text field
    And user of browser clicks on confirmation button on automation page
    And user of browser sees inventory "inventory2" on inventory list


  Scenario: User renames inventory
    When user of browser clicks on Automation in the main menu

    And user of browser clicks on "Rename" button in inventory "inventory1" menu in the sidebar
    And user of browser writes "inventory2" into rename inventory text field
    And user of browser confirms inventory rename with confirmation button
    Then user of browser sees inventory "inventory2" on inventory list


  Scenario: User removes inventory
    When user of browser clicks on Automation in the main menu

    And user of browser clicks on "Remove" button in inventory "inventory1" menu in the sidebar
    And user of browser clicks on "Remove" button in modal "remove_inventory"
    Then user of browser does not see inventory "inventory1" on inventory list


  Scenario: User leaves inventory
    When user of browser clicks on Automation in the main menu

    And user of browser clicks on "Leave" button in inventory "inventory1" menu in the sidebar
    And user of browser clicks on "Leave" button in modal "leave_inventory"
    Then user of browser does not see inventory "inventory1" on inventory list
