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
                    size: 1000000
    And initial inventories configuration in "onezone" Onezone service:
        inventory1:
            owner: space-owner-user

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service
    And directory tree structure on local file system:
          browser:
            large_file.txt:
              size: 50 MiB


  Scenario: User executes inout workflow
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses Upload (json) button from menu bar to upload workflow "workflow_upload.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Automation of "space1" in the sidebar
    And user of browser clicks Run workflow in the navigation bar
    And user of browser chooses to run "Workflow1" revision of "Workflow1" workflow
    And user of browser chooses "large_file.txt" file as initial value for workflow in modal "Select files"
    And user of browser confirms Workflow deployment by clicking Run workflow button
    And user of browser waits for all workflows to start
    And user of browser waits for all workflows to finish
    And user of browser sees workflow in ended workflows:
            name: workflow_upload
            inventory: oneprovider-2
            status: completed

    And user of browser clicks on first executed workflow
    Then user of browser sees Finished status in status bar in workflow visualizer
    And user of browser clicks on "Task1" task in "Lane1" lane in workflow visualizer
    And user of browser clicks on "Pods activity" link in "Task1" task in "Lane1" lane in workflow visualizer
    And user of browser waits for all pods to finish




