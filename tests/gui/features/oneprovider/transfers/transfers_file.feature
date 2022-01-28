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
            oneprovider-2: never synchronized
    And user of browser replicates "large_file.txt" to provider "oneprovider-2"

    # Check that transfer appeared in transfer tab
    And user of browser clicks Transfers of "space1" in the sidebar
    And user of browser waits for Transfers page to load
    Then user of browser waits for all transfers to start
    And user of browser waits for all transfers to finish
    And user of browser sees file in ended transfers:
            name: large_file.txt
            destination: oneprovider-2
            username: space-owner-user
            transferred: 50 MiB
            type: replication
            status: completed

    # Check transfer chart
    And user of browser expands first transfer record
    And user of browser sees that there is non-zero throughput in transfer chart

    And user of browser clicks Data of "space1" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely filled


  Scenario: User tries to migrate file to too small space on remote provider
    When user of browser opens oneprovider-1 Oneprovider file browser for "smallSpace" space
    And user of browser uses upload button from file browser menu bar to upload local file "large_file.txt" to remote current dir

    # Wait to ensure synchronization between providers
    And user of browser is idle for 2 seconds

    And user of browser migrates "large_file.txt" from provider "oneprovider-1" to provider "oneprovider-2"

    # Check that transfer appeared in transfer tab
    And user of browser opens oneprovider-1 Oneprovider transfers for "smallSpace" space
    Then user of browser waits for all transfers to start
    And user of browser waits for all transfers to finish
    And user of browser sees file in ended transfers:
            name: large_file.txt
            destination: oneprovider-2
            username: space-owner-user
            transferred: 0 B
            type: migration
            status: failed

    And user of browser clicks Data of "smallSpace" in the sidebar
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely empty

