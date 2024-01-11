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
                    - dir1
    And initial inventories configuration in "onezone" Onezone service:
        inventory1:
            owner: space-owner-user

    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service


  Scenario Outline: User sees successful execution of uploaded "bagit-uploader" workflow and input file <example_file_name>
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads "bagit-uploader" workflow from automation-examples repository to "inventory1" inventory

    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload file "<example_file_name>" to current dir
    And user of browser sees that item named <example_file_name> has appeared in file browser
    And user of browser clicks "Automation Workflows" of "space1" space in the sidebar
    And user of browser clicks "Run workflow" in the automation tab bar
    And user of browser chooses to run 1st revision of "bagit-uploader" workflow
    And user of browser chooses <example_file_name> file as initial value of "input-bagit-archives" store for workflow in "Select files" modal
    And user of browser chooses "dir1" file as initial value of "destination-directory" store for workflow in "Select files" modal
    And user of browser confirms workflow execution by clicking "Run workflow" button
    And user of browser waits for all workflows to start
    And user of browser waits for all workflows to finish
    And user of browser clicks on first executed workflow

    Then user of browser sees "Finished" status in status bar in workflow visualizer


    Examples:
    | example_file_name                  |
    | bagit_archive_fetch_xrootd.zip     |
    | bagit_archive_unpack.tar           |
    # TODO uncomment after workflow fix or implement exception checking
    #| bagit_archive_5gbfile.zip          |
    #| bagit_archive_fetch.zip            |
    #| bagit_archive_unpack_and_fetch.zip |


  Scenario Outline: User sees desirable information in file metadata after execution of uploaded "detect-file-formats" workflow and input file <example_file_name>
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads "detect-file-formats" workflow from automation-examples repository to "inventory1" inventory
    And user of browser uploads "bagit-uploader" workflow from automation-examples repository to "inventory1" inventory

    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload file "<example_file_name>" to current dir
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
    And user of browser clicks on "Metadata" in context menu for "<example_file_name>"
    And user of browser sees basic metadata entry with attribute named "format.mime-type" and value "<meta_entry_val1>"
    And user of browser sees basic metadata entry with attribute named "format.is-extension-matching-format" and value "True"
    And user of browser sees basic metadata entry with attribute named "format.format-name" and value "<meta_entry_val2>"


    Examples:
    | example_file_name     | meta_entry_val1      | meta_entry_val2                      |
    | example_cpp_script    | text/x-c++           | C++ source, ASCII text               |
    | example_python_script | text/x-script.python | Python script, ASCII text executable |


  Scenario Outline: User sees desirable information in file metadata after execution of uploaded "detect-file-mime-formats" workflow and input file <example_file_name>
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads "detect-file-mime-formats" workflow from automation-examples repository to "inventory1" inventory

    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload file "<example_file_name>" to current dir
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
    And user of browser clicks on "Metadata" in context menu for "<example_file_name>"
    And user of browser sees basic metadata entry with attribute named "format.mime-type" and value "<meta_entry_val1>"


    Examples:
    | example_file_name        | meta_entry_val1      |
    | example_image.jpg        | image/jpeg           |
    | example_python_script.py | text/x-python        |


  Scenario Outline: User sees successful execution of uploaded "download-files" workflow and input file <example_file_name>
    When user of browser clicks on Automation in the main menu
    And user of browser opens inventory "inventory1" workflows subpage
    And user of browser uploads "download-files" workflow from automation-examples repository to "inventory1" inventory

    And user of browser clicks "space1" on the spaces list in the sidebar
    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser uses upload button from file browser menu bar to upload file "<example_file_name>" to current dir
    And user of browser sees that item named <example_file_name> has appeared in file browser
    And user of browser clicks "Automation Workflows" of "space1" space in the sidebar
    And user of browser clicks "Run workflow" in the automation tab bar
    And user of browser chooses to run 1st revision of "download-files" workflow
    And user of browser chooses <example_file_name> file as initial value of "fetch-files" store for workflow in "Select files" modal
    And user of browser chooses "dir1" file as initial value of "destination" store for workflow in "Select files" modal
    And user of browser confirms workflow execution by clicking "Run workflow" button
    And user of browser waits for all workflows to start
    And user of browser waits for all workflows to finish
    And user of browser clicks on first executed workflow

    Then user of browser sees "Finished" status in status bar in workflow visualizer


    Examples:
    | example_file_name        |
    | fetch_xrootd.txt         |
    # TODO uncomment after workflow fix or implement exception checking
    #| fetch_multiple_files.txt |
