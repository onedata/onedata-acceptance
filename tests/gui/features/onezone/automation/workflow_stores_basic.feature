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


  Scenario Outline: User sees <output_store_type> of <output_type> in result store after modifying input store and lambda data type and executing uploaded echo workflow
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
