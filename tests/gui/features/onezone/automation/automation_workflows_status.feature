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


  Scenario: User sees workflow status "Finished" after execution of created "inout" workflow finishes
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
              # sleep do 120s
              value: {"sleep": 30}
            data:
              value builder: "Iterated item"
    And user of browser saves workflow edition by clicking "Save" button from menu bar
    And user of browser executes 1st revision of "Workflow1", using "file1" as initial value, in "space1" space

    And user of browser is idle for 30 seconds

    And trace

