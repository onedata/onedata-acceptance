Feature: Workflows execution


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: space-owner-user
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 10000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1:
                      - file1: 100
    And initial inventories configuration in "onezone" Onezone service:
        inventory1:
            owner: space-owner-user

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario: User executes inout workflow
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses Upload (json) button from menu bar to upload workflow "workflow_upload.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Automation of "space1" in the sidebar
    And user of browser clicks Run workflow in the navigation bar
    And user of browser chooses to run "Workflow1" revision of "Workflow1" workflow
    And user of browser chooses "dir1" file as initial value for workflow in modal "Select files"
    And user of browser confirms Workflow deployment by clicking Run workflow button
    And user of browser waits for all workflows to start
    And user of browser waits for all workflows to finish
    And user of browser clicks on first executed workflow
    Then user of browser sees Finished status in status bar in workflow visualizer
    And user of browser clicks on "inout" task in "Lane1" lane in workflow visualizer
    And user of browser clicks on "Pods activity" link in "inout" task in "Lane1" lane in workflow visualizer
    And user of browser waits for all pods to finish execution in in modal "Function pods activity"




