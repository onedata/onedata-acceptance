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
    And initial inventories configuration in "onezone" Onezone service:
          inventory1:
            owner: space-owner-user

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario: User sees new workflow after creating it
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses Add new workflow button from menu bar
    And user of browser writes "Workflow1" into workflow name text field
    And user of browser confirms create new workflow using Create button
    And user of browser opens inventory "inventory1" workflows subpage
    Then user of browser sees "Workflow1" in workflows list in inventory workflows subpage


  Scenario: User sees new store after creating it
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses Add new workflow button from menu bar
    And user of browser writes "Workflow1" into workflow name text field
    And user of browser confirms create new workflow using Create button
    And user of browser clicks Add store button in workflow visualizer
    And user of browser writes "Store1" into store name text field in modal "Create new store"
    And user of browser clicks on "Create" button in modal "Create new store"
    And user of browser sees "Store1" in the stores list in workflow visualizer
#
#
#  Scenario: User sees new lane after creating it
#    When user of browser clicks on Automation in the main menu
#    And user of browser opens inventory "inventory1" lambdas subpage
#    And user of browser uses Add new workflow button from menu bar
#    And user of browser writes "Workflow1" into workflow name text field
#    And user of browser confirms create new workflow using Create button
#    And user of browser clicks Add store button in Editor tab of Workflow
#    And user of browser writes "Store1" into store name text field in create store modal
#    And user of browser clicks on "Create" button in modal "Create new store"
#    And user of browser sees "Store1" in the stores list in Editor tab of Workflow
#    And user of browser clicks on create lane button in "Store1 store
#    And user of browser writes "Lane1" into lane name text field in create lane modal
#    And user of browser clicks on "Create" button in modal "Create new lane"
#    Then user of browser sees "Lane1" in the workflow visualizer


