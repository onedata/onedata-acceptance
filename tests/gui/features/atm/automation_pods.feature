Feature: Lambda`s pods

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
                    - file1: 100
                    - dir1:
                      - file1: 100
    And initial inventories configuration in "onezone" Onezone service:
        inventory1:
            owner: space-owner-user

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario: User sees desirable pods statuses after execution of uploaded "echo" workflow finishes
    When user of browser clicks on "Automation" in the main menu
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


  Scenario: User checks "Pods activity" events after checksum-counting-different-lambdas workflow execution
    When user of browser clicks on "Automation" in the main menu
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


  Scenario: User can not remove uploaded "workflow-with-sleep-one-lane.json" workflow while it is still running
    When user of browser clicks on "Automation" in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses "Upload (json)" button from menu bar to upload workflow "automation/workflow/workflow-with-sleep-one-lane.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"
    And user of browser executes 1st revision of "workflow-with-sleep-one-lane", using file as initial value: "file1" in "space1" space

    And user of browser clicks on "Ongoing" tab in automation subpage
    And user of browser sees "workflow-with-sleep-one-lane" on workflow executions list
    And user of browser clicks on "workflow-with-sleep-one-lane" menu on workflow executions list
    Then user of browser sees that "Remove" option in data row menu in automation workflows page is disabled
    And user of browser waits for all workflows to finish
