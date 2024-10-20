Feature: Workflow execution statuses tests


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
    And user of browser uploads "echo" workflow from automation-examples repository to "inventory1" inventory
    And user of browser executes 1st revision of "echo", using file as initial value: "file1" in "space1" space
    And user of browser awaits for status of "echo" workflow to be "Finished"
    Then user of browser sees that status of task "echo" in 1st parallel box in "lane 1" lane is "Finished"
    And user of browser sees that status of "lane 1" lane in "echo" is "Finished"
    And user of browser sees that status of "echo" workflow is "Finished"


  Scenario: User sees that lane, task and workflow statuses are "Preparing", "Pending" and "Active" in turn, during execution of uploaded "workflow-with-sleep-one-lane" workflow
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses "Upload (json)" button from menu bar to upload workflow "automation/workflow/workflow-with-sleep-one-lane.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"
    And user of browser executes 1st revision of "workflow-with-sleep-one-lane", using file as initial value: "file1" in "space1" space
    Then user of browser sees that status of "Lane1" lane in "Workflow1" is "Preparing"
    And user of browser sees that status of "workflow-with-sleep-one-lane" workflow is "Active"
    And user of browser sees that status of task "20s sleep" in 1st parallel box in "Lane1" lane is one of "Pending" or "Finished"
    And user of browser sees that status of task "15s sleep" in 2nd parallel box in "Lane1" lane is one of "Pending" or "Finished"


  Scenario: User does not see workflow on list after removing uploaded "inout" workflow
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads "echo" workflow from automation-examples repository to "inventory1" inventory
    And user of browser executes 1st revision of "echo" and waits extended time for workflow to finish, using file as initial value: "file1" in "space1" space

    And user of browser clicks on "Ended" tab in automation subpage
    And user of browser sees "echo" on workflow executions list
    And user of browser clicks on "echo" menu on workflow executions list
    And user of browser clicks "Remove" option in data row menu in automation workflows page
    And user of browser clicks on "Remove" button in modal "Remove Workflow Execution"
    # User waits for workflow to be removed
    And user of browser is idle for 2 seconds
    Then user of browser does not see "echo" on workflow executions list


  Scenario: User can not remove uploaded "workflow-with-sleep-one-lane.json" workflow while it is still running
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses "Upload (json)" button from menu bar to upload workflow "automation/workflow/workflow-with-sleep-one-lane.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"
    And user of browser executes 1st revision of "workflow-with-sleep-one-lane", using file as initial value: "file1" in "space1" space

    And user of browser clicks on "Ongoing" tab in automation subpage
    And user of browser sees "workflow-with-sleep-one-lane" on workflow executions list
    And user of browser clicks on "workflow-with-sleep-one-lane" menu on workflow executions list
    Then user of browser sees that "Remove" option in data row menu in automation workflows page is disabled


  Scenario: User resume workflow execution after pausing execution of created workflow while lane had preparing status
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses "Upload (json)" button from menu bar to upload workflow "automation/workflow/workflow-with-sleep-one-lane.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"
    And user of browser executes 1st revision of "workflow-with-sleep-one-lane", using file as initial value: "file1" in "space1" space

    And user of browser sees that status of "Lane1" lane in "workflow-with-sleep-one-lane" is "Preparing"
    And user of browser clicks "Pause" button on "workflow-with-sleep-one-lane" workflow status bar
    And user of browser awaits for status of "workflow-with-sleep-one-lane" workflow to be "Paused"
    And user of browser clicks "Resume" button on "workflow-with-sleep-one-lane" workflow status bar

    Then user of browser sees that status of task "20s sleep" in 1st parallel box in "Lane1" lane is "Resuming"
    And user of browser sees that status of task "15s sleep" in 2nd parallel box in "Lane1" lane is "Resuming"

    And user of browser awaits for status of "Lane1" lane to be "Active"
    And user of browser sees that status of task "20s sleep" in 1st parallel box in "Lane1" lane is "Active"
    And user of browser sees that status of task "15s sleep" in 2nd parallel box in "Lane1" lane is one of "Pending" or "Finished"
    And user of browser awaits for status of "workflow-with-sleep-one-lane" workflow to be "Finished"
    And user of browser sees that status of task "15s sleep" in 2nd parallel box in "Lane1" lane is "Finished"
    And user of browser sees that status of task "20s sleep" in 1st parallel box in "Lane1" lane is "Finished"


  Scenario: User resume workflow execution after pausing execution of uploaded workflow while first task had active status
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses "Upload (json)" button from menu bar to upload workflow "automation/workflow/workflow-with-sleep-one-lane.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"

    And user of browser executes 1st revision of "workflow-with-sleep-one-lane", using file as initial value: "file1" in "space1" space
    And user of browser awaits for status of task "20s sleep" in 1st parallel box in "Lane1" lane to be "Active"
    And user of browser clicks "Pause" button on "workflow-with-sleep-one-lane" workflow status bar
    And user of browser awaits for status of "workflow-with-sleep-one-lane" workflow to be "Paused"
    And user of browser clicks "Resume" button on "workflow-with-sleep-one-lane" workflow status bar

    Then user of browser sees that status of task "20s sleep" in 1st parallel box in "Lane1" lane is "Resuming"
    And user of browser sees that status of task "15s sleep" in 2nd parallel box in "Lane1" lane is "Resuming"

    And user of browser awaits for status of "Lane1" lane to be "Active"
    And user of browser sees that status of task "20s sleep" in 1st parallel box in "Lane1" lane is "Finished"
    And user of browser sees that status of task "15s sleep" in 2nd parallel box in "Lane1" lane is one of "Active" or "Finished"
    And user of browser awaits for status of "workflow-with-sleep-one-lane" workflow to be "Finished"
    And user of browser sees that status of task "15s sleep" in 2nd parallel box in "Lane1" lane is "Finished"
