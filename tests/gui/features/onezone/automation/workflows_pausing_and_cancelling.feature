Feature: Workflow cancelling and pausing tests


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


  Scenario: User sees status "Paused" in "Lane1" and "Unscheduled" in "Lane2" after pausing execution of created "temporary-workflow-with-sleep" workflow
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" lambdas subpage
    And user of browser creates lambda with following configuration:
        name: "inout"
        docker image: "docker.onedata.org/lambda-in-out:dev"
        mount space: False
        arguments:
          - name: "_config"
            type: Object
          - name: "data"
            type: Object
    And user of browser opens inventory "inventory1" workflows subpage

    # TODO VFS-10436 change temporary lambda with sleep after inout lambda will be improved
    And user of browser creates workflow "temporary-workflow-with-sleep"
    And user of browser creates input store for workflow "temporary-workflow-with-sleep" with following configuration:
        name: "input"
        type dropdown: List
        data type dropdown: File
        user input: True

    And user of browser clicks on create lane button in the middle of workflow visualizer
    And user of browser writes "Lane1" into lane name text field in modal "Create new lane"
    And user of browser clicks on "Create" button in modal "Create new lane"
    And user of browser creates task using 1st revision of "inout" lambda in "Lane1" lane with following configuration:
        task name: "1s sleep"
        arguments:
            _config:
              value builder: "Constant value"
              value: {"sleep": 1}
            data:
              value builder: "Iterated item"
    And user of browser creates another task using 1st revision of "inout" lambda in "Lane1" lane with following configuration:
        where parallel box: "below"
        task name: "10s sleep"
        arguments:
            _config:
              value builder: "Constant value"
              value: {"sleep": 10}
            data:
              value builder: "Iterated item"

    And user of browser clicks on create lane button on the right side of latest created lane of workflow visualizer
    And user of browser writes "Lane2" into lane name text field in modal "Create new lane"
    And user of browser clicks on "Create" button in modal "Create new lane"
    And user of browser creates task using 1st revision of "inout" lambda in "Lane2" lane with following configuration:
        task name: "1s sleep"
        arguments:
            _config:
              value builder: "Constant value"
              value: {"sleep": 1}
            data:
              value builder: "Iterated item"
    And user of browser creates another task using 1st revision of "inout" lambda in "Lane2" lane with following configuration:
        where parallel box: "below"
        task name: "10s sleep"
        arguments:
            _config:
              value builder: "Constant value"
              value: {"sleep": 10}
            data:
              value builder: "Iterated item"
    And user of browser creates another task using 1st revision of "inout" lambda in "Lane2" lane with following configuration:
        where parallel box: "below"
        task name: "5s sleep"
        arguments:
            _config:
              value builder: "Constant value"
              value: {"sleep": 5}
            data:
              value builder: "Iterated item"

    And user of browser saves workflow edition by clicking "Save" button from menu bar
    And user of browser executes 1st revision of "temporary-workflow-with-sleep", using "file1" as initial value, in "space1" space

    And user of browser awaits for status of "temporary-workflow-with-sleep" workflow to be "Active" maximum of 15 seconds
    And user of browser awaits for status of task "1s sleep" in 1st parallel box in "Lane1" lane to be "Finished" maximum of 40 seconds
    And user of browser clicks "Pause" button on "temporary-workflow-with-sleep" workflow status bar
    And user of browser sees that status of "temporary-workflow-with-sleep" workflow is "Stopping"
    And user of browser waits for workflow "temporary-workflow-with-sleep" to be paused

    Then user of browser sees that status of "temporary-workflow-with-sleep" workflow is "Paused"
    And user of browser sees that status of "Lane1" lane in "temporary-workflow-with-sleep" is "Paused"
    And user of browser sees that status of "Lane2" lane in "temporary-workflow-with-sleep" is "Unscheduled"

    And user of browser sees that status of task "1s sleep" in 1st parallel box in "Lane1" lane is "Finished"
    And user of browser sees that status of task "10s sleep" in 2nd parallel box in "Lane1" lane is "Paused"

    And user of browser sees that status of task "1s sleep" in 1st parallel box in "Lane2" lane is "Unscheduled"
    And user of browser sees that status of task "10s sleep" in 2nd parallel box in "Lane2" lane is "Unscheduled"
    And user of browser sees that status of task "5s sleep" in 3rd parallel box in "Lane2" lane is "Unscheduled"


  Scenario Outline: User sees status "<status>" in "Lane2" after stopping execution of uploaded "temporary-workflow-with-sleep" workflow
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses "Upload (json)" button from menu bar to upload workflow "temporary-workflow-with-sleep.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"
    And user of browser executes 1st revision of "temporary-workflow-with-sleep", using "file1" as initial value, in "space1" space

    And user of browser awaits for status of "temporary-workflow-with-sleep" workflow to be "Active" maximum of 15 seconds
    And user of browser awaits for status of "Lane1" lane to be "Finished" maximum of 80 seconds
    And user of browser awaits for status of "Lane2" lane to be "Active" maximum of 30 seconds

    And user of browser clicks "<stop_button>" button on "temporary-workflow-with-sleep" workflow status bar
    And user of browser sees that status of "temporary-workflow-with-sleep" workflow is "Stopping"
    And user of browser waits for workflow "temporary-workflow-with-sleep" to be stopped

    Then user of browser sees that status of "temporary-workflow-with-sleep" workflow is "<status>"
    And user of browser sees that status of "Lane1" lane in "temporary-workflow-with-sleep" is "Finished"
    And user of browser sees that status of "Lane2" lane in "temporary-workflow-with-sleep" is "<status>"
    And user of browser sees that status of task "1s sleep" in 1st parallel box in "Lane1" lane is "Finished"
    And user of browser sees that status of task "10s sleep" in 2nd parallel box in "Lane1" lane is "Finished"
    And user of browser sees that status of task "1s sleep" in 1st parallel box in "Lane2" lane is one of "Finished" or "<status>"
    And user of browser sees that status of task "10s sleep" in 2nd parallel box in "Lane2" lane is "<status>"
    And user of browser sees that status of task "5s sleep" in 3rd parallel box in "Lane2" lane is "<status>"

    Examples:
    | status       | stop_button |
    | Paused       | Pause       |
    | Cancelled    | Cancel      |


  Scenario Outline: User sees status "<status>" in "Lane1" after stopping execution of uploaded "temporary-workflow-with-sleep" workflow while "Lane1" had "Preparing" status
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses "Upload (json)" button from menu bar to upload workflow "temporary-workflow-with-sleep.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"
    And user of browser executes 1st revision of "temporary-workflow-with-sleep", using "file1" as initial value, in "space1" space

    And user of browser sees that status of "Lane1" lane in "temporary-workflow-with-sleep" is "Preparing"
    And user of browser clicks "<stop_button>" button on "temporary-workflow-with-sleep" workflow status bar

    And user of browser waits for workflow "temporary-workflow-with-sleep" to be stopped

    Then user of browser sees that status of "temporary-workflow-with-sleep" workflow is "<status>"
    And user of browser sees that status of "Lane1" lane in "temporary-workflow-with-sleep" is "<status>"
    And user of browser sees that status of "Lane2" lane in "temporary-workflow-with-sleep" is "Unscheduled"
    And user of browser sees that status of task "1s sleep" in 1st parallel box in "Lane1" lane is "<status>"
    And user of browser sees that status of task "10s sleep" in 2nd parallel box in "Lane1" lane is "<status>"
    And user of browser sees that status of task "1s sleep" in 1st parallel box in "Lane2" lane is "Unscheduled"
    And user of browser sees that status of task "10s sleep" in 2nd parallel box in "Lane2" lane is "Unscheduled"
    And user of browser sees that status of task "5s sleep" in 3rd parallel box in "Lane2" lane is "Unscheduled"


    Examples:
    | status       | stop_button |
    | Paused       | Pause       |
    | Cancelled    | Cancel      |


  Scenario: User sees status "Cancelled" in "Lane1" and "Unscheduled" in "Lane2" after cancelling execution of uploaded "temporary-workflow-with-sleep" workflow
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses "Upload (json)" button from menu bar to upload workflow "temporary-workflow-with-sleep.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"

    And user of browser executes 1st revision of "temporary-workflow-with-sleep", using "file1" as initial value, in "space1" space

    And user of browser awaits for status of "temporary-workflow-with-sleep" workflow to be "Active" maximum of 15 seconds
    And user of browser awaits for status of task "1s sleep" in 1st parallel box in "Lane1" lane to be "Finished" maximum of 30 seconds

    And user of browser sees that status of "temporary-workflow-with-sleep" workflow is "Active"
    And user of browser clicks "Cancel" button on "temporary-workflow-with-sleep" workflow status bar
    And user of browser sees that status of "temporary-workflow-with-sleep" workflow is "Stopping"
    And user of browser waits for workflow "temporary-workflow-with-sleep" to be cancelled

    Then user of browser sees that status of "temporary-workflow-with-sleep" workflow is "Cancelled"
    And user of browser sees that status of "Lane1" lane in "temporary-workflow-with-sleep" is "Cancelled"
    And user of browser sees that status of "Lane2" lane in "temporary-workflow-with-sleep" is "Unscheduled"

    And user of browser sees that status of task "1s sleep" in 1st parallel box in "Lane1" lane is "Finished"
    And user of browser sees that status of task "10s sleep" in 2nd parallel box in "Lane1" lane is "Cancelled"

    And user of browser sees that status of task "1s sleep" in 1st parallel box in "Lane2" lane is "Unscheduled"
    And user of browser sees that status of task "10s sleep" in 2nd parallel box in "Lane2" lane is "Unscheduled"
    And user of browser sees that status of task "5s sleep" in 3rd parallel box in "Lane2" lane is "Unscheduled"


  Scenario: User sees that workflow is cancelled after cancelling workflow that is paused
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses "Upload (json)" button from menu bar to upload workflow "temporary-workflow-with-one-box.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"
    And user of browser executes 1st revision of "temporary-workflow-with-one-box", using "file1" as initial value, in "space1" space

    And user of browser clicks "Pause" button on "temporary-workflow-with-one-box" workflow status bar
    And user of browser awaits for status of task "10s sleep" in 1st parallel box in "Lane1" lane to be "Paused" maximum of 10 seconds
    And user of browser sees that status of "Lane1" lane in "Workflow1" is "Paused"
    And user of browser sees that status of "temporary-workflow-with-one-box" workflow is "Paused"

    And user of browser clicks on "Suspended" tab in automation subpage
    And user of browser sees "temporary-workflow-with-one-box" on workflow executions list
    And user of browser clicks on "temporary-workflow-with-one-box" menu on workflow executions list
    And user of browser clicks "Cancel" option in data row menu in automation workflows page

    Then user of browser clicks on "Ended" tab in automation subpage
    And user of browser sees "temporary-workflow-with-one-box" on workflow executions list
    And user of browser clicks on "temporary-workflow-with-one-box" on workflow executions list
    And user of browser sees that status of task "10s sleep" in 1st parallel box in "Lane1" lane is "Cancelled"
    And user of browser sees that status of task "20s sleep" in 1st parallel box in "Lane1" lane is "Cancelled"
    And user of browser sees that status of "Lane1" lane in "Workflow1" is "Cancelled"
    And user of browser sees that status of "temporary-workflow-with-one-box" workflow is "Cancelled"


  Scenario: User sees that tasks are cancelled after cancelling workflow while task was pausing
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses "Upload (json)" button from menu bar to upload workflow "temporary-workflow-with-one-box.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"
    And user of browser executes 1st revision of "temporary-workflow-with-one-box", using "file1" as initial value, in "space1" space

    And user of browser awaits for status of task "10s sleep" in 1st parallel box in "Lane1" lane to be "Active" maximum of 10 seconds
    And user of browser clicks "Pause" button on "temporary-workflow-with-one-box" workflow status bar
    And user of browser awaits for status of task "10s sleep" in 1st parallel box in "Lane1" lane to be "Paused" maximum of 10 seconds
    And user of browser awaits for status of task "20s sleep" in 1st parallel box in "Lane1" lane to be "Stopping" maximum of 10 seconds
    And user of browser clicks "Cancel" button on "temporary-workflow-with-one-box" workflow status bar

    Then user of browser awaits for status of task "10s sleep" in 1st parallel box in "Lane1" lane to be "Cancelled" maximum of 10 seconds
    And user of browser awaits for status of task "20s sleep" in 1st parallel box in "Lane1" lane to be "Cancelled" maximum of 10 seconds
    And user of browser sees that status of "Lane1" lane in "Workflow1" is "Cancelled"
    And user of browser sees that status of "temporary-workflow-with-one-box" workflow is "Cancelled"