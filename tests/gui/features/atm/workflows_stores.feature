Feature: Workflows stores tests


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
                    - dir1:
                        - file2
                        - dir2:
                            - file3: 11111
                            - file4: 1111
    And initial inventories configuration in "onezone" Onezone service:
        inventory1:
            owner: space-owner-user

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario: User sees results for task, workflow and in result store after modifying task by adding result mapping in uploaded workflow
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads "calculate-checksums-rest" workflow from automation-examples repository to "inventory1" inventory
    And user of browser clicks on 1st revision of "calculate-checksums-rest" in workflows list in inventory workflows subpage

    And user of browser removes "sha256" task from 1st parallel box in "calculate-checksums" lane
    And user of browser modifies "md5" task in 1st parallel box in "calculate-checksums" lane by adding following:
        results:
          - result: "Current task system audit log"
          - result: "Workflow system audit log"
    And user of browser saves workflow edition by clicking "Save" button from menu bar

    And user of browser executes 1st revision of "calculate-checksums-rest" and waits extended time for workflow to finish, using file as initial value: "file1" in "space1" space
    Then user of browser sees file_id, checksum and algorithm information in audit log in "results" store details
    And user of browser sees that audit log in task "md5" in 1st parallel box in lane "calculate-checksums" contains same entries like audit log in "results" store details
    And user of browser sees that audit log for "calculate-checksums-rest" workflow contains the same entries like audit log in "results" store details


  Scenario Outline: User sees expected results in result store after modifying input store type to <storage_type> and executing uploaded counting checksums workflow
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads "calculate-checksums-rest" workflow from automation-examples repository to "inventory1" inventory
    And user of browser clicks on 1st revision of "calculate-checksums-rest" in workflows list in inventory workflows subpage
    And user of browser removes "sha256" task from 1st parallel box in "calculate-checksums" lane

    And user of browser modifies type in "input-files" store to be "<storage_type>" for "calculate-checksums-rest" workflow
    And user of browser saves workflow edition by clicking "Save" button from menu bar

    And user of browser executes 1st revision of "calculate-checksums-rest" and waits extended time for workflow to finish, using file as initial value: "<files>" in "space1" space
    Then user of browser sees that number of elements in the content of the "results" store details modal is <elem_num>
    And user of browser sees that each element with "file_id" in "results" store details modal corresponds to id of file from "<files_to_check_id>" in "space1" space

    Examples:
    | storage_type | files                                          | elem_num | files_to_check_id                                               |
    | Single value | file1                                          | 1        | file1                                                           |
    | List         | [file1, dir1, dir1/file2, dir1/dir2/file3]     | 4        | [file1, dir1, dir1/file2, dir1/dir2/file3]                      |
    | Tree forest  | dir1                                           | 5        | [dir1, dir1/file2, dir1/dir2, dir1/dir2/file3, dir1/dir2/file4] |


  Scenario: User sees list of datasets in result store after modifying input store data type to Dataset and executing uploaded echo workflow
    When user of browser creates dataset for item "file1" in "space1"
    And user of browser creates dataset for item "dir1/file2" in "space1"
    And user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads "echo" workflow from automation-examples repository to "inventory1" inventory
    And user of browser clicks on 1st revision of "echo" in workflows list in inventory workflows subpage

    And user of browser modifies data type in "input" store to be "Dataset" for "echo" workflow
    And user of browser modifies data type in "output" store to be "Dataset" for "echo" workflow

    And user of browser saves workflow edition by clicking "Save" button from menu bar
    And user of browser executes 1st revision of "echo" and waits extended time for workflow to finish, using datasets as initial value: "["file1", "file2"]" in "space1" space

    Then user of browser sees ["file1", "file2"] datasets in Store details modal for "output" store
    And user of browser clicks on "file1" dataset link in Store details modal for "output" store
    And user of browser sees "file1" item selected in the dataset browser opened in new web browser tab


  Scenario: User sees file in result store after modifying input store and lambda data type to file and executing uploaded echo workflow
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads "echo" workflow from automation-examples repository to "inventory1" inventory
    And user of browser clicks on 1st revision of "echo" in workflows list in inventory workflows subpage

    And user of browser opens inventory "inventory1" lambdas subpage
    And user of browser clicks on "Create new revision" in "echo"
    And user of browser changes 1st argument named "value" to be "File" type
    And user of browser changes 1st result named "value" to be "File" type
    And user of browser confirms edition of lambda using "Modify" button

    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser clicks on 1st revision of "echo" in workflows list in inventory workflows subpage
    And user of browser modifies type in "input" store to be "Single Value" for "echo" workflow
    And user of browser modifies data type in "input" store to be "File" for "echo" workflow
    And user of browser modifies type in "output" store to be "Single Value" for "echo" workflow
    And user of browser modifies data type in "output" store to be "File" for "echo" workflow
    And user of browser modifies "echo" task in 1st parallel box in "lane 1" lane by changing following:
        lambda:
          - revision: 2nd
        results:
          - value: output
    And user of browser saves workflow edition by clicking "Save" button from menu bar
    And user of browser executes 1st revision of "echo" and waits extended time for workflow to finish, using file as initial value: "file1" in "space1" space

    Then user of browser sees "file1" file in Store details modal for "output" store
    And user of browser clicks on "file1" file link in Store details modal for "output" store
    And user of browser sees "file1" item selected in the file browser opened in new web browser tab


  Scenario: User runs workflow with "Debug" logging level and can see entry with severity "Debug" in audit log
    When user of browser uploads "echo" workflow from automation-examples repository to "inventory1" inventory
    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Automation Workflows" of "space1" space in the sidebar
    And user of browser clicks "Run workflow" in the automation tab bar
    And user of browser chooses to run 1st revision of "echo" workflow
    And user of browser chooses "dir1" file as initial value for workflow in "Select files" modal
    And user of browser chooses "Debug" logging level
    And user of browser confirms workflow execution by clicking "Run workflow" button
    And user of browser waits for all workflows to start
    And user of browser waits for all workflows to finish
    And user of browser clicks on first executed workflow
    Then user of browser sees "Finished" status in status bar in workflow visualizer
    And user of browser clicks "Audit log" button on "Echo" workflow status bar
    And user of browser sees that workflow audit log contains following system debug entries with description:
        - "[Lane: 1, Run: 1] Starting..."
        - "[Lane: 1, Run: 1] Created."
        - "[Lane: 1, Run: 1] Parallel boxes created."
        - "[Lane: 1, Run: 1, PBox: 1, Task: 1] Created."
        - "[Lane: 1, Run: 1, PBox: 1, Task: 1] Audit log created."
        - "[Lane: 1, Run: 1, PBox: 1, Task: 1] Executor created."
        - "[Lane: 1, Run: 1] Exception store created."
        - "[Lane: 1, Run: 1] Creating..."
        - "[Lane: 1, Run: 1] Preparing..."
