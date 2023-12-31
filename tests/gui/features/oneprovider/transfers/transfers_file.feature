Feature: Oneprovider transfers files functionality

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: space-owner-user
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 100000000
                - oneprovider-2:
                    storage: posix
                    size: 100000000
        smallSpace:
            owner: space-owner-user
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 100000000
                - oneprovider-2:
                    storage: posix
                    size: 1000000
    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as space-owner-user to Onezone service
    And directory tree structure on local file system:
          browser:
            large_file.txt:
              size: 50 MiB


  Scenario: User replicates file to remote provider
    When user of browser opens oneprovider-1 Oneprovider file browser for "space1" space
    And user of browser uses upload button from file browser menu bar to upload local file "large_file.txt" to remote current dir

    # Wait to ensure synchronization between providers
    And user of browser is idle for 2 seconds

    And user of browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely empty
    And user of browser replicates "large_file.txt" to provider "oneprovider-2"

    # Check that transfer appeared in transfer tab
    And user of browser clicks "Transfers" of "space1" space in the sidebar
    And user of browser waits for Transfers page to load
    Then user of browser waits for all transfers to start
    And user of browser waits for all transfers to finish
    And user of browser sees file in ended transfers:
            name: large_file.txt
            replicated: 50 MiB
            type: replication
            status: completed

    # Check transfer chart
    And user of browser expands first transfer record
    And user of browser sees that there is non-zero throughput in transfer chart

    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely filled


  Scenario: User tries to migrate file to too small space on remote provider
    When user of browser opens oneprovider-1 Oneprovider file browser for "smallSpace" space
    And user of browser uses upload button from file browser menu bar to upload local file "large_file.txt" to remote current dir

    # Wait to ensure synchronization between providers
    And user of browser is idle for 2 seconds

    And user of browser fails to migrate "large_file.txt" from provider "oneprovider-1" to provider "oneprovider-2"
    Then user of browser sees that error modal with text "Starting migration failed!" appeared
    And user of browser clicks on "Close" button in modal "Error"

    And user of browser clicks "Files" of "smallSpace" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely empty


  Scenario: User tries to replicate file to too small space on remote provider
    When user of browser opens oneprovider-1 Oneprovider file browser for "smallSpace" space
    And user of browser uses upload button from file browser menu bar to upload local file "large_file.txt" to remote current dir
    And user of browser fails to replicate "large_file.txt" to provider "oneprovider-2"

    Then user of browser sees that error modal with text "Starting replication failed!" appeared
    And user of browser clicks on "Close" button in modal "Error"

    And user of browser clicks "Files" of "smallSpace" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely empty


  Scenario: User migrates file to remote provider
    When user of browser opens oneprovider-1 Oneprovider file browser for "space1" space
    And user of browser uses upload button from file browser menu bar to upload local file "large_file.txt" to remote current dir

    # Wait to ensure synchronization between providers
    And user of browser is idle for 2 seconds
    And user of browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely empty

    And user of browser migrates "large_file.txt" from provider "oneprovider-1" to provider "oneprovider-2"

    # Check that transfer appeared in transfer tab
    And user of browser opens oneprovider-1 Oneprovider transfers for "space1" space
    Then user of browser waits for all transfers to start
    And user of browser waits for all transfers to finish
    And user of browser sees file in ended transfers:
            name: large_file.txt
            replicated: 50 MiB
            type: migration
            status: completed

    # Check transfer chart
    And user of browser expands first transfer record
    And user of browser sees that there is non-zero throughput in transfer chart

    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely empty
            oneprovider-2: entirely filled


  Scenario: User sees that there are no file blocks on provider from which file was downloaded and then evicted
    When user of browser opens oneprovider-1 Oneprovider file browser for "smallSpace" space
    And user of browser uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
    And user of browser sees file chunks for file "20B-0.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely empty

    # download file to other provider
    And user of browser clicks on "oneprovider-2" provider on file browser page
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees file chunks for file "20B-0.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely empty

    And user of browser clicks and presses enter on item named "20B-0.txt" in file browser
    And user of browser is idle for 5 seconds
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees file chunks for file "20B-0.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely filled

    # evict file from oneprovider-1
    And user of browser evicts file "20B-0.txt" from provider oneprovider-1
    And user of browser sees file browser in files tab in Oneprovider page
    Then user of browser sees file chunks for file "20B-0.txt" as follows:
            oneprovider-1: entirely empty
            oneprovider-2: entirely filled


