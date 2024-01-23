Feature: Automation examples tests


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
                      - file2: 1000
                      - file3: 10000
                      - file4: 100
                      - file5: 100000
                    - dir2:
                      - file1: 100
    And initial inventories configuration in "onezone" Onezone service:
        inventory1:
            owner: space-owner-user

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario: User sees desirable information about "test.py" in "files-format" store after execution of uploaded "detect-file-formats" workflow finishes
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload file "automation/test.py" to current dir
    And user of browser sees that item named "test.py" has appeared in file browser

    And user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads "detect-file-formats" workflow from automation-examples repository to "inventory1" inventory

    And user of browser executes 1st revision of "detect-file-formats" workflow in "space1" space with the following initial values:
        input-files:
          - test.py

    Then user of browser sees that status of "detect-file-formats" workflow is "Finished"

    And user of browser sees that content of "formats" store is:
        mimeType: text/plain
        formatName: Python script, ASCII text executable
        isExtensionMatchingFormat: false
        fileName: test.py
        fileId: $(resolve_id space1/test.py)
        extensions: [".txt", ".bat", ".c", ".h", ".ksh", ".pl"]


  Scenario: User sees desirable information about "lorem_ipsum.enl" in "files-format" store after execution of uploaded "detect-file-formats" workflow finishes
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload file "automation/lorem_ipsum.enl" to current dir
    And user of browser sees that item named "lorem_ipsum.enl" has appeared in file browser

    And user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads "detect-file-formats" workflow from automation-examples repository to "inventory1" inventory

    And user of browser executes 1st revision of "detect-file-formats" workflow in "space1" space with the following initial values:
        input-files:
          - lorem_ipsum.enl

    Then user of browser sees that status of "detect-file-formats" workflow is "Finished"
    And user of browser sees that content of "formats" store is:
        mimeType: text/plain
        formatName: ASCII text
        isExtensionMatchingFormat: false
        fileName: lorem_ipsum.enl
        fileId: $(resolve_id space1/lorem_ipsum.enl)
        extensions: [".txt", ".bat", ".c", ".h", ".ksh", ".pl"]


  Scenario: User sees desirable error message in modal after trying to choose directory as initial value for "detect-file-formats" workflow
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads "detect-file-formats" workflow from automation-examples repository to "inventory1" inventory

    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Automation Workflows" of "space1" space in the sidebar
    And user of browser clicks "Run workflow" in the automation tab bar
    And user of browser chooses to run 1st revision of "detect-file-formats" workflow
    Then user of browser sees "Only files are allowed to be selected." message while choosing "dir1" directory as initial value for workflow in "Select files" modal


  Scenario: User sees desirable information about "test.py" in "files-format" store after execution of uploaded "detect-file-mime-formats" workflow finishes
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload file "automation/test.py" to current dir
    And user of browser sees that item named "test.py" has appeared in file browser

    And user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads "detect-file-mime-formats" workflow from automation-examples repository to "inventory1" inventory

    And user of browser executes 1st revision of "detect-file-mime-formats" workflow in "space1" space with the following initial values:
        input-files:
          - test.py

    Then user of browser sees that status of "detect-file-mime-formats" workflow is "Finished"
    And user of browser sees that content of "files-format" store is:
        fileName: test.py
        mimeType: text/x-python
        fileId: $(resolve_id space1/test.py)


  Scenario: User sees desirable information about "lorem_ipsum.enl" in "files-format" store after execution of uploaded "detect-file-mime-formats" workflow finishes
    When user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload file "automation/lorem_ipsum.enl" to current dir
    And user of browser sees that item named "lorem_ipsum.enl" has appeared in file browser

    And user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads "detect-file-mime-formats" workflow from automation-examples repository to "inventory1" inventory

    And user of browser executes 1st revision of "detect-file-mime-formats" workflow in "space1" space with the following initial values:
        input-files:
          - lorem_ipsum.enl

    Then user of browser sees that status of "detect-file-mime-formats" workflow is "Finished"
    And user of browser sees that content of "files-format" store is:
        fileName: lorem_ipsum.enl
        mimeType: unknown
        fileId: $(resolve_id space1/lorem_ipsum.enl)


  Scenario: User sees desirable error message in modal after trying to choose directory as initial value for "detect-file-mime-formats" workflow
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads "detect-file-mime-formats" workflow from automation-examples repository to "inventory1" inventory

    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Automation Workflows" of "space1" space in the sidebar
    And user of browser clicks "Run workflow" in the automation tab bar
    And user of browser chooses to run 1st revision of "detect-file-mime-formats" workflow
    Then user of browser sees "Only files are allowed to be selected." message while choosing "dir1" directory as initial value for workflow in "Select files" modal


  Scenario: User sees desirable files in file browser after execution of uploaded "download-files" workflow finishes
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads "download-files" workflow from automation-examples repository to "inventory1" inventory
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload file "automation/fetch/fetch.txt" to current dir
    And user of browser sees that item named "fetch.txt" has appeared in file browser

    And user of browser executes 1st revision of "download-files" workflow in "space1" space with the following initial values:
        fetch-files:
          - fetch.txt
        destination:
          - dir1

    Then user of browser opens file browser for "space1" space
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that the file structure in file browser is as follow:
           - dir1:
               - data:
                  - googlelogo_color_272x92dp.png
           - fetch.txt

    And user of browser clicks "Automation Workflows" of "space1" space in the sidebar
    And user of browser clicks on first executed workflow
    And user of browser sees that status of "download-files" workflow is "Finished"
    And user of browser sees that audit log in task "parse-fetch-file-mounted" in 1st parallel box in lane "collect-download-info" contains following entry:
        timestamp: today
        source: user
        severity: info
        content:
            status: Found  1 files to be downloaded.
            fetchFileName: fetch.txt
    And user of browser sees that content of "files-to-download" store is:
      sourceUrl: https://www.google.pl/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png
    And user of browser opens "sourceUrl" URL from "files-to-download" store in browser's location bar
    And user of browser sees image named "googlelogo_color_272x92dp.png" in browser


  Scenario: User sees uploaded file in file browser after executing uploaded "download-files" workflow using xrootd fetch file
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads "download-files" workflow from automation-examples repository to "inventory1" inventory

    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload file "automation/fetch/xrootd_fetch.txt" to current dir
    And user of browser sees that item named "xrootd_fetch.txt" has appeared in file browser

    And user of browser executes 1st revision of "download-files" workflow in "space1" space with the following initial values:
        fetch-files:
          - xrootd_fetch.txt
        destination:
          - dir1

    Then user of browser sees that status of "download-files" workflow is "Finished"
    And user of browser sees that audit log in task "parse-fetch-file-mounted" in 1st parallel box in lane "collect-download-info" contains following entry:
        timestamp: today
        source: user
        severity: info
        content:
            status: Found  1 files to be downloaded.
            fetchFileName: xrootd_fetch.txt

    And user of browser opens file browser for "space1" space
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that the file structure in file browser is as follow:
           - dir1:
               - data:
                  - LHC10c_pp_ESD_120076.json
           - xrootd_fetch.txt


  Scenario: User sees exception after execution of uploaded "download-files" workflow finishes when using incorrect fetch file
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads "download-files" workflow from automation-examples repository to "inventory1" inventory
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload file "automation/fetch/incorrect_fetch.txt" to current dir
    And user of browser sees that item named "incorrect_fetch.txt" has appeared in file browser
    And user of browser executes 1st revision of "download-files" workflow in "space1" space with the following initial values:
        fetch-files:
          - incorrect_fetch.txt
        destination:
          - dir1

    Then user of browser sees that status of "download-files" workflow is "Failed"
    And user of browser sees that audit log in task "parse-fetch-file-mounted" in 1st parallel box in lane "collect-download-info" contains following entry:
        timestamp: today
        severity: Error
        source: system
        content:
          details:
            reason: $(contains ["ValueError", "not enough values to unpack (expected 3, got 1)"])
          description: Lambda exception occurred during item processing.


  Scenario: User sees exception after execution of uploaded "download-files" workflow finishes when using whitespaces fetch file
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads "download-files" workflow from automation-examples repository to "inventory1" inventory
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload file "automation/fetch/whitespaces_fetch.txt" to current dir
    And user of browser sees that item named "whitespaces_fetch.txt" has appeared in file browser
    And user of browser executes 1st revision of "download-files" workflow in "space1" space with the following initial values:
        fetch-files:
          - whitespaces_fetch.txt
        destination:
          - dir1

    Then user of browser sees that status of "download-files" workflow is "Finished"
    And user of browser sees that audit log in task "parse-fetch-file-mounted" in 1st parallel box in lane "collect-download-info" contains following entry:
        timestamp: today
        source: user
        severity: info
        content:
            status: Found  1 files to be downloaded.
            fetchFileName: whitespaces_fetch.txt
    And user of browser sees that content of "files-to-download" store is:
      sourceUrl: https://www.google.pl/images/branding/googlelogo/1x/googlelogo_color_272x92dp.png


  Scenario: User sees desirable "Active" workflow status before 10s pass in task auditlog after changing sleepDurationSec in echo lambda
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads "echo" workflow from automation-examples repository to "inventory1" inventory

    And user of browser clicks on 1st revision of "echo" in workflows list in inventory workflows subpage
    And user of browser modifies "echo" task in 1st parallel box in "lane 1" lane by changing following:
        configuration parameters:
            sleepDurationSec:
              value builder: "Custom value"
              value : "10"
    And user of browser saves workflow edition by clicking "Save" button from menu bar

    And user of browser clicks "Automation Workflows" of "space1" space in the sidebar
    And user of browser clicks "Run workflow" in the automation tab bar
    And user of browser chooses to run 1st revision of "echo" workflow
    And user of browser chooses "dir1" file as initial value for workflow in "Select files" modal

    And user of browser confirms workflow execution by clicking "Run workflow" button
    And user of browser waits for all workflows to start
    And user of browser clicks on "Ongoing" tab in automation subpage
    And user of browser clicks on "echo" on workflow executions list
    And user of browser is idle for 2 seconds
    And user of browser sees that status of "echo" workflow is "Active"
    And user of browser is idle for 8 seconds
    And user of browser sees that status of "echo" workflow is "Finished"


  Scenario: User sees desirable exception in task auditlog after changing exceptionProbability in echo lambda
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads "echo" workflow from automation-examples repository to "inventory1" inventory

    And user of browser clicks on 1st revision of "echo" in workflows list in inventory workflows subpage
    And user of browser modifies "echo" task in 1st parallel box in "lane 1" lane by changing following:
        configuration parameters:
            exceptionProbability:
              value builder: "Custom value"
              value : "1"
    And user of browser saves workflow edition by clicking "Save" button from menu bar

    And user of browser clicks "Automation Workflows" of "space1" space in the sidebar
    And user of browser clicks "Run workflow" in the automation tab bar
    And user of browser executes 1st revision of "echo" workflow in "space1" space with the following initial values:
        input:
          - dir1

    Then user of browser sees that status of "echo" workflow is "Failed"
    And user of browser sees that audit log in task "echo" in 1st parallel box in lane "lane 1" contains following entry:
        timestamp: today
        severity: Error
        content:
          details:
            reason: Random exception
          description: Lambda exception occurred during item processing.


  Scenario Outline: User checks time series charts and "results" store content after execution of uploaded "<workflow_name>" workflow
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads "<workflow_name>" workflow from automation-examples repository to "inventory1" inventory
    And user of browser executes 1st revision of "<workflow_name>" workflow in "space1" space with the following initial values:
        input-files:
          - dir1

    Then user of browser sees that status of "<workflow_name>" workflow is "Finished"

    And user of browser sees chart with processing stats after opening "Time series" link for task "md5" in 1st parallel box in "calculate-checksums" lane
    And user of browser sees that time in right corner of chart with processing stats is around actual time
    And user of browser sees that value of last column on chart with processing stats is greater than zero
    And user of browser changes time resolution to "1 hr" in modal "Task time series"
    And user of browser sees that files processing speed is greater or equal 2.5 per second on chart with processing stats
    And user of browser sees that bytes processing speed is greater or equal 10 per second on chart with processing stats
    And user of browser clicks on "X" button in modal "Task time series"
    And user of browser closes task "md5" in 1st parallel box in "calculate-checksums" lane in workflow visualizer

    And user of browser sees chart with processing stats after opening "Time series" link for task "sha256" in 1st parallel box in "calculate-checksums" lane
    And user of browser sees that time in right corner of chart with processing stats is around actual time
    And user of browser sees that value of last column on chart with processing stats is greater than zero
    And user of browser changes time resolution to "1 hr" in modal "Task time series"
    And user of browser sees that files processing speed is greater or equal 2 per second on chart with processing stats
    And user of browser sees that bytes processing speed is greater or equal 10 per second on chart with processing stats
    And user of browser clicks on "X" button in modal "Task time series"

    And user of browser sees that number of elements in the content of the "results" store details modal is 12
    And user of browser sees that each element from list "[dir1, dir1/file1, dir1/file2, dir1/file3, dir1/file4, dir1/file5]" in "space1" space corresponds to two instances of the element with "file_id" in "results" store details modal

    Examples:
    | workflow_name               |
    | calculate-checksums-rest    |
    | calculate-checksums-mounted |

#  There is more tests for the 'calculate_checksum_rest' workflow in the 'workflow_store.feature'


  Scenario: User sees desirable information in "results" store after execution of uploaded "demo" workflow finishes
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads "demo" workflow from automation-examples repository to "inventory1" inventory

    And user of browser executes 1st revision of "demo" workflow in "space1" space with the following initial values:
        input_files:
          - dir2

    Then user of browser sees that status of "demo" workflow is "Finished"
    And user of browser sees following strings represented by "["Hello - dir2", "Hello - file1"]" in content in "results" store details modal


  Scenario: User downloads audit log of executed workflow and sees that log entries in the downloaded file correspond to those visible in GUI
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads "echo" workflow from automation-examples repository to "inventory1" inventory
    And user of browser executes 1st revision of "echo", using file as initial value: "dir1/file1" in "space1" space
    And user of browser waits for all workflows to start
    And user of browser waits for all workflows to finish
    And user of browser clicks on first executed workflow
    And user of browser clicks "Audit log" button on "Echo" workflow status bar
    And user of browser clicks on "Download as JSON" button in modal "Audit log"
    Then user of browser sees that recent downloaded json file contains audit log which has the same entries as the workflow audit log in GUI
