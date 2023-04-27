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
    And user of browser modifies "md5" task in 1st parallel box in "calculate-checksums" lane by adding following:
        results:
          - result: "Current task system audit log"
          - result: "Workflow system audit log"
    And user of browser saves workflow edition by clicking "Save" button from menu bar

    And user of browser executes 1st revision of "calculate-checksums-rest" and waits extended time for workflow to finish, using file as initial value: "file1" in "space1" space
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

    And user of browser executes 1st revision of "calculate-checksums-rest" and waits extended time for workflow to finish, using file as initial value: "<files>" in "space1" space
    Then user of browser sees that number of elements in content in "results" store details modal is <elem_num>
    And user of browser sees that each element with "file_id" in "results" store details modal corresponds to id of file from "<files_to_check_id>" in "space1" space

    Examples:
    | storage_type | files                                          | elem_num | files_to_check_id                                               |
    | Single value | file1                                          | 1        | file1                                                           |
    | List         | [file1, dir1, dir1/file2, dir1/dir2/file3]     | 4        | [file1, dir1, dir1/file2, dir1/dir2/file3]                      |
    | Tree forest  | dir1                                           | 5        | [dir1, dir1/file2, dir1/dir2, dir1/dir2/file3, dir1/dir2/file4] |


  Scenario Outline: User sees <store_type> of <store_data_type> in result store after modifying input store and lambda data type to <store_data_type> and executing uploaded echo workflow
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses "Upload (json)" button from menu bar to upload workflow "echo.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"

    And user of browser opens inventory "inventory1" lambdas subpage
    And user of browser clicks on "Create new revision" in "echo"
    And user of browser changes 1st argument named "value" to be "<output_store_data_type>" type
    And user of browser changes 1st result named "value" to be "<output_store_data_type>" type
    And user of browser confirms edition of lambda using "Modify" button

    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser clicks on 2nd revision of "echo" in workflows list in inventory workflows subpage
    And user of browser modifies data type in "input" store to be "<input_store_data_type>" for "echo" workflow
    And user of browser modifies type in "input" store to be "<input_store_type>" for "echo" workflow
    And user of browser modifies data type in "output" store to be "<output_store_data_type>" for "echo" workflow
    And user of browser modifies type in "output" store to be "<output_store_type>" for "echo" workflow
    And user of browser modifies "echo" task in 1st parallel box in "lane 1" lane by changing following:
        lambda:
          - revision: 2nd
        results:
          - value: output
    And user of browser saves workflow edition by clicking "Save" button from menu bar
    And user of browser executes 2nd revision of "echo" and waits extended time for workflow to finish, using <input_type> as initial value: "<initial_value>" in "space1" space
    Then user of browser sees following <output_type> "<output_value>" in content in "output" store details modal

    Examples:
    | input_store_type | input_store_data_type | output_store_type | output_store_data_type | input_type | output_type   | initial_value                       | output_value                            |
    | List             | Number                | List              | Number                 | number     | numbers       | [1, 2, 3]                           | [1, 2, 3]                               |
    | Single Value     | Number                | Single Value      | Number                 | number     | number        | 111                                 | 111                                     |
    | Range            | Number                | List              | Number                 | range      | numbers       | {'start': 1, 'end': 100,'step': 10} | [1, 11, 21, 31, 41, 51, 61, 71, 81, 91] |
    | Single Value     | String                | Single Value      | String                 | string     | string        | Sample string                       | Sample string                           |
    | List             | Boolean               | List              | Boolean                | booleans   | booleans      | [true, false, true, true]           | [true, false, true, true]               |
    | Single Value     | Array (Number)        | Single Value      | Array (Number)         | numbers    | array         | [11, 22, 33]                        | [11, 22, 33]                            |
    | Range            | Number                | Single Value      | Number                 | range      | number        | {'start': 5, 'end': 50,'step': 5}   | 45                                      |
    | List             | Boolean               | Single Value      | Boolean                | booleans   | boolean       | [true, true, true]                  | true                                    |
    | Single Value     | String                | List              | String                 | string     | strings       | Sample string                       | ["Sample string"]                       |
    | Single Value     | Range                 | Range             | Range                  | range      | range         | {'start': 5, 'end': 50,'step': 5}   | {'start': 5, 'end': 50,'step': 5}       |
    | Tree forest      | File                  | List              | File                   | files      | files         | dir1                                | [ /space1/dir1, /space1/dir1/file2, /space1/dir1/dir2, /space1/dir1/dir2/file3, /space1/dir1/dir2/file4]     |
    | List             | Range                 | List              | Object                 | ranges     | range_objects | [{'start': 5, 'end': 50,'step': 5}, {'start': 1, 'end': 100,'step': 10}] | [{'start': 5, 'end': 50,'step': 5},{'start': 1, 'end': 100,'step': 10}] |
    | List             | Range                 | List              | Range                  | ranges     | ranges        | [{'start': 5, 'end': 50,'step': 5}, {'start': 1, 'end': 100,'step': 10}] | [{'start': 5, 'end': 50,'step': 5},{'start': 1, 'end': 100,'step': 10}] |



  Scenario: User sees list of datasets in result store after modifying input store data type to Dataset and executing uploaded echo workflow
    When user of browser creates dataset for item "file1" in "space1"
    And user of browser creates dataset for item "dir1/file2" in "space1"
    And user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses "Upload (json)" button from menu bar to upload workflow "echo.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"
    And user of browser modifies data type in "input" store to be "Dataset" for "echo" workflow
    And user of browser modifies data type in "output" store to be "Dataset" for "echo" workflow

    And user of browser saves workflow edition by clicking "Save" button from menu bar
    And user of browser executes 2nd revision of "echo" and waits extended time for workflow to finish, using datasets as initial value: "["file1", "file2"]" in "space1" space

    Then user of browser sees "["file1", "file2"]" datasets in Store details modal for "output" store
    And user of browser sees dataset browser after clicking "file1" in Store details modal for "output" store


  Scenario: User sees file in result store after modifying input store and lambda data type to file and executing uploaded echo workflow
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uses "Upload (json)" button from menu bar to upload workflow "echo.json" to current dir without waiting for upload to finish
    And user of browser clicks on "Apply" button in modal "Upload workflow"

    And user of browser opens inventory "inventory1" lambdas subpage
    And user of browser clicks on "Create new revision" in "echo"
    And user of browser changes 1st argument named "value" to be "File" type
    And user of browser changes 1st result named "value" to be "File" type
    And user of browser confirms edition of lambda using "Modify" button

    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser clicks on 2nd revision of "echo" in workflows list in inventory workflows subpage
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
    And user of browser executes 2nd revision of "echo" and waits extended time for workflow to finish, using file as initial value: "file1" in "space1" space

    Then user of browser sees "file1" file in Store details modal for "output" store
    And user of browser sees file browser after clicking "file1" in Store details modal for "output" store

