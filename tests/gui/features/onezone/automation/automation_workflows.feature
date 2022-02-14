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


  Scenario: User creates new workflow
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" lambdas subpage
    And user of browser uses Add new workflow button from menu bar
    And user of browser writes "Workflow1" into workflow name text field
    And user of browser confirms create new workflow using Create button
    And user of browser opens inventory "inventory1" workflows subpage
    Then user of browser sees "workflow_upload" in workflows list in inventory workflows subpage


  Scenario: User creates new store
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" lambdas subpage
    And user of browser uses Add new workflow button from menu bar
    And user of browser writes "Workflow1" into workflow name text field
    And user of browser confirms create new workflow using Create button
    And user of browser clicks Add store button in Editor tab of Workflow
    And user of browser writes "Store1" into store name text field in create store modal
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser sees "workflow_upload" in workflows list in inventory workflows subpage

