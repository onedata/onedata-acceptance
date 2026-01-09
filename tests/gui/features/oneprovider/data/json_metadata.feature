Feature: Basic data tab operations on directory JSON metadata in file browser


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
          space1:
            owner: space-owner-user
            providers:
              - oneprovider-1:
                  storage: posix
                  size: 1000000
            storage:
              defaults:
                provider: oneprovider-1
              directory tree:
                - dir1:
                    - file2: 11111
                - file1: 11111

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario Outline: Add valid metadata in JSON format
    When user of browser opens file browser for "space1" space

    And user of browser clicks on "Metadata" in context menu for "<item>"
    And user of browser sees that "<details_modal>" modal is opened on "Metadata" tab
    And user of browser clicks on "JSON" navigation tab in metadata panel
    And user of browser types '{"id": 1}' to JSON textarea in metadata panel
    And user of browser clicks on "Save" button in metadata panel
    And user of browser clicks on "X" button in modal "<details_modal>"
    Then user of browser sees metadata status tag for "<item>" in file browser
    And user of browser opens metadata panel on JSON tab for "<item>"
    And user of browser sees that JSON textarea in metadata panel contains '{"id": 1}'

    Examples:
    | details_modal      | item  |
    | File details       | file1 |
    | Directory details  | dir1  |


  Scenario Outline: User doesn't see JSON metadata and metadata status tag after deleting JSON metadata
    When user of browser opens file browser for "space1" space

    And user of browser adds and saves '{"id": 1}' JSON metadata for "<item>"
    And user of browser opens metadata panel on JSON tab for "<item>"

    # remove JSON metadata
    And user of browser sees that JSON textarea in metadata panel contains '{"id": 1}'
    And user of browser cleans JSON textarea in metadata panel
    And user of browser clicks on "Save" button in metadata panel
    And user of browser clicks on "X" button in modal "<details_modal>"

    Then user of browser does not see metadata status tag for "<item>" in file browser
    And user of browser opens metadata panel on JSON tab for "<item>"
    And user of browser sees that JSON textarea in metadata panel is empty

    Examples:
    | details_modal      | item  |
    | File details       | file1 |
    | Directory details  | dir1  |


  Scenario Outline: Discard changes while entering metadata in JSON format
    When user of browser opens file browser for "space1" space

    And user of browser opens metadata panel on JSON tab for "<item>"
    And user of browser types '{"id": 1}' to JSON textarea in metadata panel
    And user of browser clicks on "Discard changes" button in metadata panel
    And user of browser clicks on "X" button in modal "<details_modal>"

    And user of browser opens metadata panel on JSON tab for "<item>" directory
    Then user of browser sees that JSON textarea in metadata panel is empty

    Examples:
    | details_modal      | item  |
    | File details       | file1 |
    | Directory details  | dir1  |


  Scenario Outline: User creates new json column of mode Whole document and sees that its content is truncated in browser row
    When user of browser opens file browser for "space1" space
    And user of browser enables only [] column in columns configuration popover in file browser table

    And user of browser adds and saves '{"key1":"val1", "key2": {"key1":"val1", "key2":{"key1":"val1"}}}' JSON metadata for "<item>"

    And user of browser creates new json column with "Whole document" mode in file browser table

    Then user of browser sees that item named "<item>" has '{"key2":{"key2":{"key1":"val1"}, "key1":"val1"},…' value in json column in file browser
    And user of browser copies content of json column for item "<item>" and sees that it is equal to '{"key1":"val1","key2": {"key1":"val1","key2":{"key1":"val1"}}}' in file browser

    Examples:
    | item  |
    | file1 |
    | dir1  |


  Scenario Outline: User enters nested metadata for item and creates column for outer key, then changes it to other one
    When user of browser opens file browser for "space1" space
    And user of browser enables only [] column in columns configuration popover in file browser table

    And user of browser adds and saves '{"key1":"val", "key2": {"nested_key1":"nested_val1", "nested_key2":{"nested_key3":"nested_val2"}}}' JSON metadata for "<item>"

    And user of browser creates new json column with "Extract key" mode for "key2" key and with "test" custom label in file browser table

    Then user of browser copies content of json column for item "<item>" and sees that it is equal to '{"nested_key1":"nested_val1", "nested_key2":{"nested_key3":"nested_val2"}}' in file browser
    And user of browser modifies json column with name "test" in file browser table by changing it as follows:
      key: key1
    And user of browser copies content of json column for item "<item>" and sees that it is equal to '"val"' in file browser
    
    Examples:
    | item  |
    | file1 |
    | dir1  |
  

  Scenario Outline: User creates json column of mode query
    When user of browser opens file browser for "space1" space
    And user of browser enables only [] column in columns configuration popover in file browser table

    And user of browser adds and saves '[{"key1": {"nested_key1":"nested_val1"}, "key2":"val"}, {"key1":{"nested_key1":"nested_val2"}}]' JSON metadata for "<item>"
    And user of browser creates new json column with "Query" mode for "key1.nested_key1" query in file browser table
    Then user of browser copies content of json column for item "<item>" and sees that it is equal to '["nested_val1", "nested_val2"]' in file browser

    Examples:
    | item  |
    | file1 |
    | dir1  |


  Scenario Outline: User creates json column with custom label and changes its label
    When user of browser opens file browser for "space1" space
    And user of browser enables only [] column in columns configuration popover in file browser table

    And user of browser adds and saves '{"id": 1}' JSON metadata for "<item>"
    And user of browser creates new json column with "Whole document" mode and "test" custom label in file browser table

    And user of browser modifies json column with name "test" in file browser table by changing it as follows:
      label: apple

    Then user of browser sees json column named "apple" in columns configuration popover in file browser table
    And user of browser does not see json column named "test" in columns configuration popover in file browser table

    Examples:
    | item  |
    | file1 |
    | dir1  |

  
  Scenario Outline: User creates json column and hides its visibility
    When user of browser opens file browser for "space1" space
    And user of browser enables only [] column in columns configuration popover in file browser table

    And user of browser adds and saves '{"id": 1}' JSON metadata for "<item>"
    And user of browser creates new json column with "Whole document" mode and "test" custom label in file browser table
    And user of browser enables only ["test"] column in columns configuration popover in file browser table
    And user of browser sees json column named "test" in columns configuration popover in file browser table

    And user of browser enables only [] column in columns configuration popover in file browser table
    Then user of browser sees that item named "<item>" has no json column in file browser

    Examples:
    | item  |
    | file1 |
    | dir1  |
  

  Scenario Outline: User creates json column with mode Whole document, changes its mode to Extract key, and then to Query
    When user of browser opens file browser for "space1" space
    And user of browser enables only [] column in columns configuration popover in file browser table

    And user of browser adds and saves '{"key1":"val1", "key2": {"key1":"val1", "key2":{"key1":"val2"}}}' JSON metadata for "<item>"

    And user of browser creates new json column with "Whole document" mode and "test" custom label in file browser table
    And user of browser enables only ["test"] column in columns configuration popover in file browser table

    Then user of browser modifies json column with name "test" in file browser table by changing it as follows:
      mode: Extract key
      key: key1
      label: apple

    And user of browser copies content of json column for item "<item>" and sees that it is equal to '"val1"' in file browser

    And user of browser modifies json column with name "apple" in file browser table by changing it as follows:
      mode: Query
      query: key2.key2.key1
      label: banana

    And user of browser sees json column named "banana" in columns configuration popover in file browser table
    And user of browser copies content of json column for item "<item>" and sees that it is equal to '"val2"' in file browser

    Examples:
    | item  |
    | file1 |
    | dir1  |