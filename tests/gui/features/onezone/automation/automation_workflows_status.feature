Feature: Workflows execution


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


  Scenario: User sees that workflow, task, lane statuses are "Finished" after execution of created "Workflow1" workflow finishes
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" lambdas subpage

    # User manually creates inout lambda
    And user of browser creates lambda with following configuration:
        name: "inout"
        docker image: "docker.onedata.org/lambda-in-out:dev"
        mount space: False
        arguments:
          - name: "_config"
            type: Object
          - name: "data"
            type: Object

    # User manually creates workflow using inout lambda
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser creates workflow "Workflow1"

    # User creates input store for workflow
    And user of browser creates input store for workflow "Workflow1" with following configuration:
        name: "input"
        type dropdown: List
        data type dropdown: File
        user input: True

    And user of browser clicks on create lane button in the middle of workflow visualizer
    And user of browser writes "Lane1" into lane name text field in modal "Create new lane"
    And user of browser clicks on "Create" button in modal "Create new lane"


    And user of browser creates task using 1st revision of "inout" lambda in "Lane1" lane with following configuration:
        arguments:
            _config:
              value builder: "Constant value"
              value: {"sleep": 10}
            data:
              value builder: "Iterated item"
    And user of browser saves workflow edition by clicking "Save" button from menu bar
    And user of browser executes 1st revision of "Workflow1", using "file1" as initial value, in "space1" space

    # User waits for workflow to finish
    And user of browser is idle for 20 seconds

    Then user of browser sees that status of task "inout" in 1st parallel box in "Lane1" lane is "Finished"
    And user of browser sees that status of "Lane1" lane in "Workflow1" is "Finished"
    And user of browser sees that status of "Workflow1" workflow is "Finished"


  Scenario: User sees status "Paused" after pausing execution of created "Workflow1" workflow
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

    # this workflow is temporary, because docker image will be changed
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
        task name: "10s sleep"
        arguments:
            _config:
              value builder: "Constant value"
              value: {"sleep": 10}
            data:
              value builder: "Iterated item"
    And user of browser creates another task using 1st revision of "inout" lambda in "Lane1" lane with following configuration:
        where parallel box: "below"
        task name: "50s sleep"
        arguments:
            _config:
              value builder: "Constant value"
              value: {"sleep": 50}
            data:
              value builder: "Iterated item"

    And user of browser clicks on create lane button on the right side of latest created lane of workflow visualizer
    And user of browser writes "Lane2" into lane name text field in modal "Create new lane"
    And user of browser clicks on "Create" button in modal "Create new lane"
    And user of browser creates task using 1st revision of "inout" lambda in "Lane2" lane with following configuration:
        task name: "10s sleep"
        arguments:
            _config:
              value builder: "Constant value"
              value: {"sleep": 10}
            data:
              value builder: "Iterated item"
    And user of browser creates another task using 1st revision of "inout" lambda in "Lane2" lane with following configuration:
        where parallel box: "below"
        task name: "40s sleep"
        arguments:
            _config:
              value builder: "Constant value"
              value: {"sleep": 40}
            data:
              value builder: "Iterated item"
    And user of browser creates another task using 1st revision of "inout" lambda in "Lane2" lane with following configuration:
        where parallel box: "below"
        task name: "50s sleep"
        arguments:
            _config:
              value builder: "Constant value"
              value: {"sleep": 50}
            data:
              value builder: "Iterated item"

    And user of browser saves workflow edition by clicking "Save" button from menu bar
    And user of browser executes 1st revision of "temporary-workflow-with-sleep", using "file1" as initial value, in "space1" space

    # User waits for first tasks in to be finished
    And user of browser is idle for 25 seconds

    And user of browser sees that status of "temporary-workflow-with-sleep" workflow is "Active"
    And user of browser clicks "Pause" button on "temporary-workflow-with-sleep" workflow status bar
    Then user of browser sees that status of "temporary-workflow-with-sleep" workflow is "Stopping"

    And user of browser waits for workflow "temporary-workflow-with-sleep" to be paused
    And user of browser sees that status of "temporary-workflow-with-sleep" workflow is "Paused"

    And user of browser sees that status of "Lane1" lane in "temporary-workflow-with-sleep" is "Paused"
    And user of browser sees that status of "Lane2" lane in "temporary-workflow-with-sleep" is "Unscheduled"

    And user of browser sees that status of task "10s sleep" in 1st parallel box in "Lane1" lane is "Finished"
    And user of browser sees that status of task "50s sleep" in 2nd parallel box in "Lane1" lane is "Paused"

    And user of browser sees that status of task "10s sleep" in 1st parallel box in "Lane2" lane is "Unscheduled"
    And user of browser sees that status of task "40s sleep" in 2nd parallel box in "Lane2" lane is "Unscheduled"
    And user of browser sees that status of task "50s sleep" in 3rd parallel box in "Lane2" lane is "Unscheduled"

