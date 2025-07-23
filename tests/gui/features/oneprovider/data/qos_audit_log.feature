Feature: QoS Audit Logs


  Background:
    Given initial users configuration in "onezone" Onezone service:
        - user1


  Scenario: User can see entries about replicated files and desired audit logs in QoS audit log, after adding QoS requirement
    Given initial spaces configuration in "onezone" Onezone service:
            space1:
                owner: user1
                providers:
                    - oneprovider-1:
                        storage: posix
                        size: 1000000
                    - oneprovider-2:
                        storage: posix
                        size: 1000000
                storage:
                    defaults:
                        provider: oneprovider-1
                    directory tree:
                        - dir1:
                            - file1
                            - file2

    And opened browser with user1 signed in to "onezone" service
    When user of browser clicks on Providers in the main menu
    And user of browser clicks on provider "oneprovider-2" in providers sidebar
    And user of browser opens file browser for "space1" space

    And user of browser clicks on "Choose other Oneprovider" on file browser page
    And user of browser clicks on "oneprovider-2" provider on file browser page
    And user of browser sees file browser in files tab in Oneprovider page

    And user of browser opens "File details" modal on "QoS" tab for "dir1" file using context menu
    And user of browser clicks on "Add Requirement" button in QoS panel

    And user of browser clicks on add query block icon in QoS panel
    And user of browser chooses "provider" property in "Add QoS condition" popup

    And user of browser sees ["oneprovider-1", "oneprovider-2"] provider on values list in "Add QoS condition" popup
    And user of browser chooses value of "oneprovider-2" provider in "Add QoS condition" popup
    And user of browser clicks "Add" in "Add QoS condition" popup
    And user of browser clicks on "Save" button in QoS panel

    And user of browser sees that all QoS requirements are fulfilled
    And user of browser selects "Show details audit log" option in QoS info type button

    And user of browser sees the following logs in audit log files list in given order for "[file1, file2]" files:
        - Required: Local replica reconciled.
        - Optional: Remote replica differs, reconciliation already in progress.
        - Required: Remote replica differs, reconciliation started.

    And user of browser sees that all logs in audit log files list are ordered from newest to oldest

    # clicking on file1 displays modal with warning similar to this: this link points to non existent location
    # Also while clicking "open in new tab" it works fine
    # TODO: VFS-12968
    
    # And user of browser clicks on "file1" link in audit log browser
    # And user of browser sees that current working directory displayed in breadcrumbs on file browser is "space1/dir1"
    # Then user of browser sees that ["file1"] items are selected in file browser


  Scenario: User sees logs from the replication of a single file, only on the target replication provider
    Given initial spaces configuration in "onezone" Onezone service:
            space1:
                owner: user1
                providers:
                    - oneprovider-1:
                        storage: posix
                        size: 1000000
                    - oneprovider-2:
                        storage: posix
                        size: 1000000
                storage:
                    defaults:
                        provider: oneprovider-1
                    directory tree:
                        - file1

    And opened browser with user1 signed in to "onezone" service
    When user of browser clicks on Providers in the main menu
    And user of browser clicks on provider "oneprovider-2" in providers sidebar
    And user of browser opens file browser for "space1" space

    And user of browser clicks on "Choose other Oneprovider" on file browser page
    And user of browser clicks on "oneprovider-2" provider on file browser page
    And user of browser sees file browser in files tab in Oneprovider page

    And user of browser opens "File details" modal on "QoS" tab for "file1" file using context menu
    And user of browser clicks on "Add Requirement" button in QoS panel

    And user of browser clicks on add query block icon in QoS panel
    And user of browser chooses "provider" property in "Add QoS condition" popup

    And user of browser sees ["oneprovider-1", "oneprovider-2"] provider on values list in "Add QoS condition" popup
    And user of browser chooses value of "oneprovider-1" provider in "Add QoS condition" popup
    And user of browser clicks "Add" in "Add QoS condition" popup
    And user of browser clicks on "Save" button in QoS panel

    And user of browser sees that all QoS requirements are fulfilled
    And user of browser selects "Show details audit log" option in QoS info type button
    And user of browser sees that there are no logs in audit log files list with following information: "No log entries — consider switching to another Oneprovider."

    And user of browser opens file browser for "space1" space
    And user of browser clicks on "oneprovider-1" provider on file browser page

    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser opens "File details" modal on "QoS" tab for "file1" file using context menu
    And user of browser selects "Show details audit log" option in QoS info type button

    And user of browser sees the following logs in audit log files list in given order for "[file1]" files:
        - Required: Local replica reconciled.
        - Optional: Remote replica differs, reconciliation already in progress.
        - Required: Remote replica differs, reconciliation started.


    



    
