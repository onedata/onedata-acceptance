Feature: Automation examples input files test


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: space-owner-user
            providers:
                - oneprovider-1:
                    storage: s3
                    size: 10000000000
            storage:
                defaults:
                    provider: oneprovider-1
                directory tree:
                    - dir1:
                      - file1
    And initial inventories configuration in "onezone" Onezone service:
        inventory1:
            owner: space-owner-user

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario Outline: User sees desirable information in file metadata after execution of uploaded "detect-file-formats" workflow and input file <example_file_name>
    When user of browser clicks on "Automation" in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads "detect-file-formats" workflow from automation-examples repository to "inventory1" inventory
    And user of browser uploads "bagit-uploader" workflow from automation-examples repository to "inventory1" inventory

    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload input file "automation/input_files/<example_file_name>" to current dir
    And user of browser sees that item named <example_file_name> has appeared in file browser
    And user of browser clicks "Automation Workflows" of "space1" space in the sidebar
    And user of browser clicks "Run workflow" in the automation tab bar
    And user of browser chooses to run 1st revision of "detect-file-formats" workflow
    And user of browser chooses <example_file_name> file as initial value of "input-files" store for workflow in "Select files" modal
    And user of browser confirms workflow execution by clicking "Run workflow" button
    And user of browser waits for all workflows to start
    And user of browser waits for all workflows to finish
    And user of browser clicks on first executed workflow

    Then user of browser sees "Finished" status in status bar in workflow visualizer
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on "Metadata" in context menu for <example_file_name> in file browser
    And user of browser sees xattr metadata entry with key "format.mime-type" and value "<meta_entry_val1>"
    And user of browser sees xattr metadata entry with key "format.is-extension-matching-format" and value "True"
    And user of browser sees xattr metadata entry with key "format.format-name" and value "<meta_entry_val2>"


    Examples:
    | example_file_name       | meta_entry_val1      | meta_entry_val2                      |
    | "example_cpp_script"    | text/x-c++           | C++ source, ASCII text               |
    | "example_python_script" | text/x-script.python | Python script, ASCII text executable |


  Scenario Outline: User sees desirable information in file metadata after execution of uploaded "detect-file-mime-formats" workflow and input file <example_file_name>
    When user of browser clicks on "Automation" in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads "detect-file-mime-formats" workflow from automation-examples repository to "inventory1" inventory

    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload input file "automation/input_files/<example_file_name>" to current dir
    And user of browser sees that item named <example_file_name> has appeared in file browser
    And user of browser clicks "Automation Workflows" of "space1" space in the sidebar
    And user of browser clicks "Run workflow" in the automation tab bar
    And user of browser chooses to run 1st revision of "detect-file-mime-formats" workflow
    And user of browser chooses <example_file_name> file as initial value of "input-files" store for workflow in "Select files" modal
    And user of browser confirms workflow execution by clicking "Run workflow" button
    And user of browser waits for all workflows to start
    And user of browser waits for all workflows to finish
    And user of browser clicks on first executed workflow

    Then user of browser sees "Finished" status in status bar in workflow visualizer
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks on "Metadata" in context menu for <example_file_name> in file browser
    And user of browser sees xattr metadata entry with key "format.mime-type" and value "<meta_entry_val1>"


    Examples:
    | example_file_name          | meta_entry_val1    |
    | "example_image.jpg"        | image/jpeg         |
    | "example_python_script.py" | text/x-python      |


  Scenario: User sees successful execution of uploaded "annotate-images" workflow
    When user of browser clicks on "Automation" in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads "annotate-images" workflow from automation-examples repository to "inventory1" inventory

    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser uses upload button from file browser menu bar to upload input file "automation/input_files/example_image.jpg" to current dir
    And user of browser sees that item named "example_image.jpg" has appeared in file browser

    And user of browser clicks "Automation Workflows" of "space1" space in the sidebar
    And user of browser executes 1st revision of "Annotate images" workflow in "space1" space with the following initial values:
      Files to process:
        - dir1
    Then user of browser sees "Finished" status in status bar in workflow visualizer
    # check correct metadata for image file
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser clicks on "Metadata" in context menu for "example_image.jpg" in file browser
    And user of browser sees xattr metadata entry with key "width" and value "115"
    And user of browser sees xattr metadata entry with key "height" and value "126"
    And user of browser sees xattr metadata entry with key "orientation" and value "vertical"
    And user of browser sees xattr metadata entry with key "dominant_colour" and value "black"
    And user of browser sees xattr metadata entry with key "average_colour" and value "dark gray"
    And user of browser clicks on "X" button in modal "File details"
    # check no metadata for no image file
    And user of browser clicks on menu for "file1" directory in file browser
    And user of browser clicks "Metadata" option in data row menu in file browser
    And user of browser sees that "File details" modal has appeared
    And user of browser sees that "File details" modal is opened on "Metadata" tab
    And user of browser sees that all metadata tabs are marked as empty
    And user of browser sees that there is no metadata in metadata panel