Feature: Basic workflows management


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


  Scenario: User sees that new workflow has been added after uploading it as json file
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses Upload (json) button from menu bar to upload workflow "workflow_upload.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"
    And user of browser opens inventory "inventory1" workflows subpage
    Then user of browser sees "Workflow1" in workflows list in inventory workflows subpage


  Scenario: User sees new workflow after creating it
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses Add new workflow button from menu bar in workflows subpage
    And user of browser writes "Workflow1" into workflow name text field
    And user of browser confirms create new workflow using Create button
    And user of browser opens inventory "inventory1" workflows subpage
    Then user of browser sees "Workflow1" in workflows list in inventory workflows subpage


  Scenario: User sees new store after creating it
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser creates workflow "Workflow1"
    And user of browser clicks Add store button in workflow visualizer
    And user of browser writes "Store1" into store name text field in modal "Create new store"
    And user of browser clicks on "Create" button in modal "Create new store"
    Then user of browser sees "Store1" in the stores list in workflow visualizer


  Scenario: User sees new lane after creating it
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser creates workflow "Workflow1"
    And user of browser clicks Add store button in workflow visualizer
    And user of browser writes "Store1" into store name text field in modal "Create new store"
    And user of browser clicks on "Create" button in modal "Create new store"
    And user of browser sees "Store1" in the stores list in workflow visualizer
    And user of browser clicks on create lane button in the middle of workflow visualizer
    And user of browser writes "Lane1" into lane name text field in modal "Create new lane"
    And user of browser clicks on "Create" button in modal "Create new lane"
    Then user of browser sees "Lane1" lane in workflow visualizer


  Scenario: User sees task after adding it to uploaded workflow
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses Upload (json) button from menu bar to upload workflow "workflow_empty_lane.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"
    And user of browser clicks on add parallel box button in the middle of "Lane1" lane
    And user of browser clicks create task button in empty parallel box in "Lane1" lane
    And user of browser uses Add new lambda button from menu bar in lambdas subpage
    And user of browser writes "Lambda1" into lambda name text field
    And user of browser writes "docker_image_example" into docker image text field
    And user of browser confirms create new lambda using Create button
    And user of browser confirms create new task using Create button
    Then user of browser sees task named "Lambda1" in "Lane1" lane


  Scenario: User changes name of task in uploaded workflow
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses Upload (json) button from menu bar to upload workflow "workflow_upload.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"
    And user of browser clicks on "Modify" button in task "Task1" menu in "Lane1" lane in workflow visualizer
    And user of browser writes "Task2" into name text field in task creation subpage
    And user of browser confirms edition of task using Modify button
    Then user of browser sees task named "Task2" in "Lane1" lane


  Scenario: User does not see task in uploaded workflow after removing it
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses Upload (json) button from menu bar to upload workflow "workflow_upload.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"
    And user of browser clicks on "Remove" button in task "Task1" menu in "Lane1" lane in workflow visualizer
    And user of browser clicks on "Remove" button in modal "Remove task"
    Then user of browser does not see task named "Task1" in "Lane1" lane