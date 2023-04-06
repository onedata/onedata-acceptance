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
    And user of browser uses "Upload (json)" button from menu bar to upload workflow "calculate-checksums-rest.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"

    And user of browser removes "sha256" task from 1st parallel box in "calculate-checksums" lane
    And user of browser modifies "md5" task in 1st parallel box in "calculate-checksums" lane by adding following results:
        result:
          - target store: "Current task system audit log"
          - target store: "Workflow system audit log"
    And user of browser saves workflow edition by clicking "Save" button from menu bar

    And user of browser executes 1st revision of "calculate-checksums-rest", using "file1" as initial value, in "space1" space and waits extended time for workflow to finish
    Then user of browser sees file_id, checksum and algorithm information in audit log in "results" store details
    And user of browser sees that audit logs in task "md5" in 1st parallel box in lane "calculate-checksums" contains same information like audit log in "results" store details
    And user of browser sees that audit logs for "calculate-checksums-rest" workflow contains the same information like audit log in "results" store details


  Scenario Outline: User sees expected results in result store after modifying input store type to <storage_type> and executing uploaded counting checksums workflow
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses "Upload (json)" button from menu bar to upload workflow "calculate-checksums-rest.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"
    And user of browser removes "sha256" task from 1st parallel box in "calculate-checksums" lane

    And user of browser modifies type in "input-files" store to be "<storage_type>" for "calculate-checksums-rest" workflow
    And user of browser saves workflow edition by clicking "Save" button from menu bar

    And user of browser executes 1st revision of "calculate-checksums-rest", using "<files>" as initial value, in "space1" space and waits extended time for workflow to finish
    Then user of browser sees that number of elements in content in "results" store details modal is <elem_num>
    And user of browser sees that each element with "file_id" in "results" store details modal corresponds to id of file from "<files_to_check_id>" in "space1" space

    Examples:
    | storage_type | files                                          | elem_num | files_to_check_id                                               |
    | Single value | file1                                          | 1        | file1                                                           |
    | List         | [file1, dir1, dir1/file2, dir1/dir2/file3]     | 4        | [file1, dir1, dir1/file2, dir1/dir2/file3]                      |
    | Tree forest  | dir1                                           | 5        | [dir1, dir1/file2, dir1/dir2, dir1/dir2/file3, dir1/dir2/file4] |


  Scenario: User sees list of ranges in result store after modifying input store data type to range and executing uploaded echo workflow
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses "Upload (json)" button from menu bar to upload workflow "echo.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"
    And user of browser modifies data type in "input" store to be "Range" for "echo" workflow
    And user of browser modifies data type in "output" store to be "Range" for "echo" workflow

    And user of browser saves workflow edition by clicking "Save" button from menu bar
    And user of browser executes 2nd revision of "echo", using "[{'start': 5, 'end': 50,'step': 5},{'start': 1, 'end': 100,'step': 10}]" as initial value, in "space1" space and waits extended time for workflow to finish

    Then user of browser sees following ranges "[{'start': 5, 'end': 50,'step': 5},{'start': 1, 'end': 100,'step': 10}]" in content in "output" store details modal


