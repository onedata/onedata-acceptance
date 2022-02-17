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
    Then user of browser sees "Store1" in the stores list in workflow visualizer


  Scenario: User sees new lane after creating it
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses Add new workflow button from menu bar
    And user of browser writes "Workflow1" into workflow name text field
    And user of browser confirms create new workflow using Create button
    And user of browser clicks Add store button in workflow visualizer
    And user of browser writes "Store1" into store name text field in modal "Create new store"
    And user of browser clicks on "Create" button in modal "Create new store"
    And user of browser sees "Store1" in the stores list in workflow visualizer
    And user of browser clicks on create lane button in the middle of workflow visualizer
    And user of browser writes "Lane1" into lane name text field in modal "Create new lane"
    And user of browser clicks on "Create" button in modal "Create new lane"
    Then user of browser sees "Lane1" in the workflow visualizer


  Scenario: User adds lambda  to uploaded workflow
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" lambdas subpage
    And user of browser uses Add new lambda button from menu bar
    And user of browser writes "Lambda1" into lambda name text field
    And user of browser writes "docker_image_example" into docker image text field
    And user of browser confirms lambda creation by clicking Create button
    And user of browser sees "Lambda1" in lambdas list in inventory lambdas subpage
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses Upload (json) button from menu bar to upload workflow "workflow_empty_lane.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"
    And user of browser clicks on add parallel box button in "Lane1"
    And user of browser clicks on empty parallel box in "Lane1" to add lambda
    And user of browser writes "Task1" into name text field
    And user of browser confirms task creation by clicking Create button
    Then user of browser sees task named "Task1" in "Lane1"


  Scenario: User changes name of lambda in uploaded workflow
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses Upload (json) button from menu bar to upload workflow "workflow_upload.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"
    And user of browser clicks on "Modify" button in task "inventory1" menu in "Lane1"
    And user of browser writes "Task1" into name text field
    And user of browser confirms task creation by clicking Create button
    Then user of browser sees task named "Task1" in "Lane1"


  Scenario: User removes parallel box in uploaded workflow
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses Upload (json) button from menu bar to upload workflow "workflow_upload.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"
    And user of browser clicks on "Modify" button in task "inventory1" menu in "Lane1"
    And user of browser writes "Task1" into name text field
    And user of browser confirms task creation by clicking Create button
    Then user of browser sees task named "Task1" in "Lane1"


