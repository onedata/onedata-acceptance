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


  Scenario: User executes inout workflow and checks pod statuses in "Function pods activity" modal
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses Upload (json) button from menu bar to upload workflow "workflow_upload.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Automation of "space1" in the sidebar
    And user of browser clicks Run workflow in the navigation bar
    And user of browser chooses to run "Workflow1" revision of "Workflow1" workflow
    And user of browser chooses "dir1" file as initial value for workflow in "Select files" modal
    And user of browser confirms Workflow deployment by clicking Run workflow button
    And user of browser waits for all workflows to start
    And user of browser waits for all workflows to finish
    And user of browser clicks on first executed workflow
    Then user of browser sees Finished status in status bar in workflow visualizer

    # User tests Function pods activity modal
    And user of browser clicks on "inout" task in "Lane1" lane in workflow visualizer
    And user of browser clicks on "Pods activity" link in "inout" task in "Lane1" lane in workflow visualizer
#    And user of browser waits for all pods to finish execution in modal "Function pods activity"
#    And user of browser sees pod in all pods in modal "Function pods activity":
#            readiness: 0/1
#            status: Terminated
#
#    And user of browser clicks on first terminated pod in modal "Function pods activity"
#    And user of browser sees event with following reason: Scheduled in modal "Function pods activity"


  Scenario: User creates in-out workflow through GUI and executes it
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" lambdas subpage

    # User manually creates inout lambda
    And user of browser uses Add new lambda button from menu bar in lambdas subpage
    And user of browser writes "inout" into lambda name text field
    And user of browser writes "docker.onedata.org/in-out:v1" into docker image text field
    And user of browser disables lambdas Mount space toggle
    And user of browser adds argument named "data" of "Object" type
    And user of browser adds result named "data" of "Object" type
    And user of browser confirms create new lambda using Create buttonn
    And user of browser sees "inout" in lambdas list in inventory lambdas subpage

    # User manually creates workflow using inout lambda
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser creates workflow "Workflow1"

    # User creates input store for workflow
    And user of browser clicks Add store button in workflow visualizer
    And user of browser writes "input" into store name text field in modal "Create new store"
    And user of browser chooses "Tree forest" in type dropdown menu in modal "Create new store"
    And user of browser chooses "Any file" in data type dropdown menu in modal "Create new store"
    And user of browser enables User input toggle in modal "Create new store"
    And user of browser clicks on "Create" button in modal "Create new store"

    # User creates Lane
    And user of browser clicks on create lane button in the middle of workflow visualizer
    And user of browser writes "Lane1" into lane name text field in modal "Create new lane"
    And user of browser clicks on "Create" button in modal "Create new lane"

    # User creates output store for workflow
    And user of browser clicks Add store button in workflow visualizer
    And user of browser writes "output" into store name text field in modal "Create new store"
    And user of browser chooses "List" in type dropdown menu in modal "Create new store"
    And user of browser chooses "Object" in data type dropdown menu in modal "Create new store"
    And user of browser clicks on "Create" button in modal "Create new store"

    # User creates task using previously created lambda
    And user of browser clicks on add parallel box button in the middle of "Lane1" lane
    And user of browser clicks create task button in empty parallel box in "Lane1" lane
    And user of browser chooses "inout" revision of "inout" lambda to add to workflow
    And user of browser chooses "output" in target store dropdown menu in create task page
    And user of browser confirms create new task using Create button
    And user of browser sees task named "inout" in "Lane1" lane

    # User changes details of workflow revision
    And user of browser changes workflow view to "Details" tab
    And user of browser writes "inout1" in description textfield in workflow Details tab
    And user of browser Saves workflow edition by clicking Save button from menu bar

    # User executes created workflow and checks if output value is correct
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks Automation of "space1" in the sidebar
    And user of browser clicks Run workflow in the navigation bar
    And user of browser chooses to run "inout1" revision of "Workflow1" workflow
    And user of browser chooses "dir1" file as initial value for workflow in "Select files" modal
    And user of browser confirms Workflow deployment by clicking Run workflow button
    And user of browser waits for all workflows to start
    And user of browser waits for all workflows to finish
    And user of browser clicks on first executed workflow
    And user of browser sees Finished status in status bar in workflow visualizer
    Then user of browser compares content of "input" store and "output" store

