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
                    - dir1:
                      - file1: 100
                    - dir2:
                      - file1: 100
                      - file2: 1000
                      - file3: 10000
                      - file4: 100
                      - file5: 100000
    And initial inventories configuration in "onezone" Onezone service:
        inventory1:
            owner: space-owner-user

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario: User sees desirable pods statuses after execution of uploaded "echo" workflow finishes
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads "echo" workflow from automation-examples repository to "inventory1" inventory
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Automation Workflows" of "space1" space in the sidebar
    And user of browser clicks "Run workflow" in the automation tab bar
    And user of browser chooses to run 1st revision of "echo" workflow
    And user of browser chooses "dir1" file as initial value for workflow in "Select files" modal
    And user of browser confirms workflow execution by clicking "Run workflow" button
    And user of browser waits for all workflows to start
    And user of browser waits for all workflows to finish
    And user of browser clicks on first executed workflow
    Then user of browser sees "Finished" status in status bar in workflow visualizer

    # User tests openfaas-pods-activity-monitor
    And user of browser clicks on task "echo" in 1st parallel box in "lane 1" lane in workflow visualizer
    And user of browser clicks on link "Pods activity" in "echo" task in 1st parallel box in "lane 1" lane in workflow visualizer
    And user of browser waits for all pods to finish execution in modal "Function pods activity"
    And user of browser clicks on first terminated pod in modal "Function pods activity"
    And user of browser sees events in modal "Function pods activity" with following reasons:
         - "Terminated"
         - "Running"
         - "Scheduled"


  Scenario: User sees finished state and output store content of executed "in-out" workflow created using GUI
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" lambdas subpage

    # User manually creates inout lambda
    And user of browser creates lambda with following configuration:
        name: "echo"
        docker image: "onedata/lambda-echo:v3"
        mount space: False
        configuration parameters:
          - name: "sleepDurationSec"
            type: Number
          - name: "exceptionProbability"
            type: Number
          - name: "streamResults"
            type: Boolean
        arguments:
          - name: "data"
            type: Object
        results:
           - name: "data"
             type: Object

    And user of browser sees "echo" in lambdas list in inventory lambdas subpage

    # User manually creates workflow using echo lambda
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser creates workflow "Workflow1"

    # User creates input store for workflow
    And user of browser creates input store for workflow "Workflow1" with following configuration:
        name: "input"
        type dropdown: List
        data type dropdown: File
        user input: True

    # User creates Lane
    And user of browser clicks on create lane button in the middle of workflow visualizer
    And user of browser writes "Lane1" into lane name text field in modal "Create new lane"
    And user of browser clicks on "Create" button in modal "Create new lane"

    And user of browser creates output store for workflow "Workflow1" with following configuration:
        name: "output"
        type dropdown: List
        data type dropdown: Object

    And user of browser creates task using 1st revision of "echo" lambda in "Lane1" lane with following configuration:
        results:
            data:
              target store: "output"

    # User changes details of workflow revision
    And user of browser changes workflow view to "Details" tab
    And user of browser writes "Workflow1_revision1" in description textfield in workflow Details tab
    And user of browser saves workflow edition by clicking "Save" button from menu bar

    And user of browser executes 1st revision of "Workflow1" and waits extended time for workflow to finish, using directory as initial value: "dir1" in "space1" space
    And user of browser sees "Finished" status in status bar in workflow visualizer
    Then user of browser sees that "fileId" in "output" store is the same as in "input" store


  Scenario: User creates checksum-counting-oneclient workflow through GUI and executes it
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" lambdas subpage

    And user of browser creates lambda with following configuration:
        name: "checksum-counting-oneclient"
        docker image: "onedata/lambda-calculate-checksum-mounted:v2"
        read-only: False
        configuration parameters:
          - name: "metadataKey"
            type: String
          - name: "algorithm"
            type: String
        arguments:
          - name: "file"
            type: File
        results:
          - name: "result"
            type: Object

    And user of browser sees "checksum-counting-oneclient" in lambdas list in inventory lambdas subpage

    # User manually creates workflow using checksum-counting-oneclient lambda
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser creates workflow "Workflow1"

    And user of browser creates input store for workflow "Workflow1" with following configuration:
        name: "input-files"
        type dropdown: Tree forest
        data type dropdown: File
        user input: True

    And user of browser clicks on create lane button in the middle of workflow visualizer
    And user of browser writes "Lane1" into lane name text field in modal "Create new lane"
    And user of browser clicks on "Create" button in modal "Create new lane"

    # User creates checksums output store for workflow
    And user of browser creates output store for workflow "Workflow1" with following configuration:
        name: "output-store"
        type dropdown: List
        data type dropdown: Object

    # User creates task using previously created lambda
    And user of browser creates task using 1st revision of "checksum-counting-oneclient" lambda in "Lane1" lane with following configuration:
        configuration parameters:
            metadataKey:
              value builder: "Custom value"
              value: "md5_key"
            algorithm:
              value builder: "Custom value"
              value: "md5"
        arguments:
            file:
              value builder: "Iterated item"
        results:
            result:
              target store: "output-store"

    And user of browser sees task named "checksum-counting-oneclient" in "Lane1" lane
    And user of browser creates another task using 1st revision of "checksum-counting-oneclient" lambda in "Lane1" lane with following configuration:
        where parallel box: "below"
        task name: "Second lambda task"
        configuration parameters:
            metadataKey:
              value builder: "Custom value"
              value: "sha256_key"
            algorithm:
              value builder: "Custom value"
              value: "sha256"
        arguments:
            file:
              value builder: "Iterated item"
        results:
            result:
              target store: "output-store"
    And user of browser saves workflow edition by clicking "Save" button from menu bar

    And user of browser executes 1st revision of "Workflow1" and waits extended time for workflow to finish, using file as initial value: "dir1/file1" in "space1" space
    And if workflow status is "Failed" user of browser saves audit logs for all tasks to logs
    Then user of browser sees "Finished" status in status bar in workflow visualizer


  Scenario: User sees that different checksums are well counted after execution of uploaded "counting-different-checksums" workflow
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses "Upload (json)" button from menu bar to upload workflow "automation/workflow/counting-different-checksums.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"

    And user of browser executes 1st revision of "counting-different-checksums" and waits extended time for workflow to finish, using directory as initial value: "dir2" in "space1" space
    And if workflow status is "Failed" user of browser saves audit logs for all tasks to logs

    And user of browser sees "Finished" status in status bar in workflow visualizer
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks and presses enter on item named "dir2" in file browser

    Then user of browser sees that counted checksums ["md5", "sha512", "sha256", "adler32"] for "file1" are alike to those counted in workflow
    And user of browser sees that counted checksums ["md5", "sha512", "sha256", "adler32"] for "file2" are alike to those counted in workflow
    And user of browser sees that counted checksums ["md5", "sha512", "sha256", "adler32"] for "file3" are alike to those counted in workflow
    And user of browser sees that counted checksums ["md5", "sha512", "sha256", "adler32"] for "file4" are alike to those counted in workflow
    And user of browser sees that counted checksums ["md5", "sha512", "sha256", "adler32"] for "file5" are alike to those counted in workflow


  Scenario: User checks "Pods activity" events after checksum-counting-different-lambdas workflow execution
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses "Upload (json)" button from menu bar to upload workflow "automation/workflow/checksum-counting-different-lambdas.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"
    And user of browser executes 1st revision of "checksum-counting-different-lambdas", using directory as initial value: "dir1" in "space1" space

    Then user of browser sees that name of first pod in tab "Current" for task "md5" in 1st parallel box in "calculate-checksums" lane contains lambda name "calculate-checksum-rest"

    And user of browser sees following "Pods activity" messages for task "md5" in 1st parallel box in "calculate-checksums" lane after workflow execution is finished:
         - 'Created container result-streamer'
         - 'Started container result-streamer'
         - 'Pod initialized, containers ready'
         - 'Stopping container result-streamer'
         - 'The pod has been terminated'
         - 'message that contains: "calculate-checksum-rest" + "Started container"'
         - 'message that contains: "calculate-checksum-rest" + "Created container"'
    And user of browser sees that numer of events on "Pods activity" list for task "md5" in 1st parallel box in "calculate-checksums" lane is about 15

    And user of browser sees that name of first pod in tab "All" for task "sha256" in 1st parallel box in "calculate-checksums" lane contains lambda name "calculate-checksum-rest-no-stats"

    And user of browser sees following "Pods activity" messages for task "sha256" in 1st parallel box in "calculate-checksums" lane after workflow execution is finished:
         - 'Pod initialized, containers ready'
         - 'The pod has been terminated'
         - 'message that contains: "calculate-checksum-rest-no-stats" + "Started container"'
         - 'message that contains: "calculate-checksum-rest-no-stats" + "Created container"'
         - 'message that contains: "calculate-checksum-rest-no-stats" + "Stopping container"'
    And user of browser sees that numer of events on "Pods activity" list for task "sha256" in 1st parallel box in "calculate-checksums" lane is about 11

    And user of browser sees that name of first pod in tab "All" for task "adler32" in 2nd parallel box in "calculate-checksums" lane contains lambda name "calculate-checksum-mounted"
    And user of browser sees following "Pods activity" messages for task "adler32" in 2nd parallel box in "calculate-checksums" lane after workflow execution is finished:
         - "Created container oneclient-sidecar"
         - "Started container oneclient-sidecar"
         - "Pod initialized, containers ready"
         - "Stopping container oneclient-sidecar"
         - "The pod has been terminated"
         - 'message that contains: "calculate-checksum-mounted" + "Started container"'
         - 'message that contains: "calculate-checksum-mounted" + "Created container"'
    And user of browser sees that numer of events on "Pods activity" list for task "adler32" in 2nd parallel box in "calculate-checksums" lane is about 14

    And user of browser sees that name of first pod in tab "All" for task "sha512" in 1st parallel box in "calculate-checksums-lane2" lane contains lambda name "calculate-checksum-mounted"
    And user of browser sees following "Pods activity" messages for task "sha512" in 1st parallel box in "calculate-checksums-lane2" lane after workflow execution is finished:
         - "Created container result-streamer"
         - "Started container result-streamer"
         - "Stopping container result-streamer"
         - "Created container oneclient-sidecar"
         - "Started container oneclient-sidecar"
         - "Pod initialized, containers ready"
         - "Stopping container oneclient-sidecar"
         - "The pod has been terminated"
         - 'message that contains: "calculate-checksum-mounted" + "Started container"'
         - 'message that contains: "calculate-checksum-mounted" + "Created container"'
    And user of browser sees that numer of events on "Pods activity" list for task "sha512" in 1st parallel box in "calculate-checksums-lane2" lane is about 18
