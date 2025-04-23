Feature: File Details API tests

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 1000000
            storage:
              defaults:
                provider: oneprovider-1
              directory tree:
                - file1: 11111
    And opened browser with user1 signed in to "onezone" service


  Scenario Outline: User reads file details using the command from "<command_label>" from API section in file details modal
    When user of browser copies token "access token" from tokens page
    And user of browser opens file browser for "space1" space
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Information" option in data row menu in file browser
    And user of browser sees that "File details" modal has appeared
    And user of browser clicks on "API" navigation tab in "File Details" modal
    And user of browser sees that "File details" modal is opened on "API" tab

    And user of browser copies command "<command_label>" in API section from file details modal
    And user of browser executes copied command with environment variables:
      TOKEN: $(resolve_token "access token")
    Then user of browser sees that executed curl command returned successful http code

  Examples:
    | command_label |
    | Download file content |
    | Get file hard links   |
    | Get data distribution |
    | Remove file           |
    | Get attributes        |


  Scenario: User updates file content using the command from "Update file content" from API section in file details modal
    When user of browser copies token "access token" from tokens page
    And user of browser opens file browser for "space1" space
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Information" option in data row menu in file browser
    And user of browser sees that "File details" modal has appeared
    And user of browser clicks on "API" navigation tab in "File Details" modal
    And user of browser sees that "File details" modal is opened on "API" tab

    And user of browser copies command "Update file content" in API section from file details modal
    And user of browser executes copied command with environment variables:
      TOKEN: $(resolve_token "access token")
      NEW_CONTENT: ABCD
    Then user of browser sees that executed curl command returned successful http code


  Scenario: User adds, gets and removes JSON metadata using the commands from API section in file details modal
    When user of browser copies token "access token" from tokens page
    And user of browser opens file browser for "space1" space
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Information" option in data row menu in file browser
    And user of browser sees that "File details" modal has appeared
    And user of browser clicks on "API" navigation tab in "File Details" modal
    And user of browser sees that "File details" modal is opened on "API" tab

    And user of browser copies command "Set JSON metadata" in API section from file details modal
    And user of browser executes copied command with environment variables:
      TOKEN: $(resolve_token "access token")
      METADATA: $(resolve_compose_json "license","CC-0")
    Then user of browser sees that executed curl command returned successful http code
    And user of browser copies command "Get JSON metadata" in API section from file details modal
    And user of browser executes copied command with environment variables:
      TOKEN: $(resolve_token "access token")
    And user of browser sees that executed curl command returned successful http code
    And user of browser copies command "Remove JSON metadata" in API section from file details modal
    And user of browser executes copied command with environment variables:
      TOKEN: $(resolve_token "access token")
    And user of browser sees that executed curl command returned successful http code


  Scenario: User adds, gets and removes RDF metadata using the commands from API section in file details modal
    When user of browser copies token "access token" from tokens page
    And user of browser opens file browser for "space1" space
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Information" option in data row menu in file browser
    And user of browser sees that "File details" modal has appeared
    And user of browser clicks on "API" navigation tab in "File Details" modal
    And user of browser sees that "File details" modal is opened on "API" tab

    And user of browser copies command "Set RDF metadata" in API section from file details modal
    And user of browser executes copied command with environment variables:
      TOKEN: $(resolve_token "access token")
      METADATA: <rdf:XML xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"></rdf:XML>
    Then user of browser sees that executed curl command returned successful http code
    And user of browser copies command "Get RDF metadata" in API section from file details modal
    And user of browser executes copied command with environment variables:
      TOKEN: $(resolve_token "access token")
    And user of browser sees that executed curl command returned successful http code
    And user of browser copies command "Remove RDF metadata" in API section from file details modal
    And user of browser executes copied command with environment variables:
      TOKEN: $(resolve_token "access token")
    And user of browser sees that executed curl command returned successful http code


  Scenario: User adds, gets and removes xattrs metadata using the commands from API section in file details modal
    When user of browser copies token "access token" from tokens page
    And user of browser opens file browser for "space1" space
    And user of browser clicks on menu for "file1" file in file browser
    And user of browser clicks "Information" option in data row menu in file browser
    And user of browser sees that "File details" modal has appeared
    And user of browser clicks on "API" navigation tab in "File Details" modal
    And user of browser sees that "File details" modal is opened on "API" tab

    And user of browser copies command "Set extended attribute (xattr)" in API section from file details modal
    And user of browser executes copied command with environment variables:
      TOKEN: $(resolve_token "access token")
      XATTRS: $(resolve_compose_json "license","CC-0")
    Then user of browser sees that executed curl command returned successful http code
    And user of browser copies command "Get extended attributes (xattrs)" in API section from file details modal
    And user of browser executes copied command with environment variables:
      TOKEN: $(resolve_token "access token")
    And user of browser sees that executed curl command returned successful http code
    And user of browser copies command "Remove extended attributes (xattrs)" in API section from file details modal
    And user of browser executes copied command with environment variables:
      TOKEN: $(resolve_token "access token")
      KEY_LIST: $(resolve_compose_list "license")
    And user of browser sees that executed curl command returned successful http code

