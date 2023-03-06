Feature: Workflow rerun tests


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: space-owner-user
            providers:
                - oneprovider-1:
                    storage: s3
                    size: 10000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - file1: 100
    And initial inventories configuration in "onezone" Onezone service:
        inventory1:
            owner: space-owner-user

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario: User sees that workflow, task, lane statuses are "Finished" after execution of uploaded "Workflow1" workflow finishes
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses "Upload (json)" button from menu bar to upload workflow "checksum-counting-different-lambdas.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"
    And user of browser executes 2nd revision of "checksum-counting-different-lambdas", using "file1" as initial value, in "space1" space

    And user of browser clicks "Cancel" button on "checksum-counting-different-lambdas" workflow status bar

    And user of browser clicks "Rerun all items" option in latest run menu for "calculate-checksums" lane
    And trace
