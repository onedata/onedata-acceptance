Feature: Oneprovider transfers functionality

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 100000000
                - oneprovider-2:
                    storage: posix
                    size: 100000000
        smallSpace:
            owner: user1
            providers:
                - oneprovider-1:
                    storage: posix
                    size: 100000000
                - oneprovider-2:
                    storage: posix
                    size: 1000000
    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service
    And opened oneprovider-1 Oneprovider view in web GUI by user of browser


  Scenario: User replicates file to remote provider
    When user of browser uses spaces select to change data space to "space1"
    And user of browser uses upload button in toolbar to upload file "large_file.txt" to current dir

    # Wait to ensure synchronization between providers
    And user of browser is idle for 2 seconds
    And user of browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: never synchronized
    And user of browser replicates "large_file.txt" to provider "oneprovider-2"

    # Check that transfer appeared in transfer tab
    And user of browser clicks on the "transfers" tab in main menu sidebar
    And user of browser selects "space1" space in transfers tab

    Then user of browser waits for all transfers to start
    And user of browser waits for all transfers to finish
    And user of browser sees file in ended transfers:
            name: large_file.txt
            destination: oneprovider-2
            username: user1
            total files: 1
            transferred: 50 MiB
            type: replication
            status: completed

    # Check transfer chart
    And user of browser expands first transfer record
    And user of browser sees that there is non-zero throughput in transfer chart

    And user of browser clicks on the "data" tab in main menu sidebar
    And user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely filled


  Scenario: User replicates directory to remote provider
    When user of browser uses spaces select to change data space to "space1"
    And user of browser creates directory "dir1"
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser uses upload button in toolbar to upload file "large_file.txt" to current dir
    And user of browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: never synchronized
    And user of browser changes current working directory to space1 using breadcrumbs
    # Wait to ensure synchronization between providers
    And user of browser is idle for 2 seconds
    And user of browser replicates "dir1" to provider "oneprovider-2"

    # Check that transfer appeared in transfer tab
    And user of browser clicks on the "transfers" tab in main menu sidebar
    And user of browser selects "space1" space in transfers tab

    Then user of browser waits for all transfers to start
    And user of browser waits for all transfers to finish
    And user of browser sees directory in ended transfers:
            name: dir1
            destination: oneprovider-2
            username: user1
            total files: 1
            transferred: 50 MiB
            type: replication
            status: completed

    # Check transfer chart
    And user of browser expands first transfer record
    And user of browser sees that there is non-zero throughput in transfer chart

    And user of browser clicks on the "data" tab in main menu sidebar
    And user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely filled


  Scenario: User tries to migrate file to too small space on remote provider
    When user of browser uses spaces select to change data space to "smallSpace"
    And user of browser uses upload button in toolbar to upload file "large_file.txt" to current dir

    # Wait to ensure synchronization between providers
    And user of browser is idle for 2 seconds
    And user of browser migrates "large_file.txt" from provider "oneprovider-1" to provider "oneprovider-2"

    # Check that transfer appeared in transfer tab
    And user of browser clicks on the "transfers" tab in main menu sidebar
    And user of browser selects "smallSpace" space in transfers tab

    Then user of browser waits for all transfers to start
    And user of browser waits for all transfers to finish
    And user of browser sees file in ended transfers:
            name: large_file.txt
            destination: oneprovider-2
            username: user1
            total files: 1
            transferred: 0 B
            type: migration
            status: failed

    And user of browser clicks on the "data" tab in main menu sidebar
    And user of browser uses spaces select to change data space to "smallSpace""
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely empty


  Scenario: User tries to migrate directory to too small space on remote provider
    When user of browser uses spaces select to change data space to "smallSpace"
    And user of browser creates directory "dir1"
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser uses upload button in toolbar to upload file "large_file.txt" to current dir
    And user of browser changes current working directory to smallSpace using breadcrumbs

    # Wait to ensure synchronization between providers
    And user of browser is idle for 2 seconds
    And user of browser migrates "dir1" from provider "oneprovider-1" to provider "oneprovider-2"

    # Check that transfer appeared in transfer tab
    And user of browser clicks on the "transfers" tab in main menu sidebar
    And user of browser selects "smallSpace" space in transfers tab

    Then user of browser waits for all transfers to start
    And user of browser waits for all transfers to finish
    And user of browser sees directory in ended transfers:
            name: dir1
            destination: oneprovider-2
            username: user1
            total files: 1
            transferred: 0 B
            type: migration
            status: failed

    And user of browser clicks on the "data" tab in main menu sidebar
    And user of browser uses spaces select to change data space to "smallSpace"
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely empty


  Scenario: User tries to replicate file to too small space on remote provider
    When user of browser uses spaces select to change data space to "smallSpace"
    And user of browser uses upload button in toolbar to upload file "large_file.txt" to current dir

    # Wait to ensure synchronization between providers
    And user of browser is idle for 2 seconds
    And user of browser replicates "large_file.txt" to provider "oneprovider-2"

    # Check that transfer appeared in transfer tab
    And user of browser clicks on the "transfers" tab in main menu sidebar
    And user of browser selects "smallSpace" space in transfers tab

    Then user of browser waits for all transfers to start
    And user of browser waits for all transfers to finish
    And user of browser sees file in ended transfers:
            name: large_file.txt
            destination: oneprovider-2
            username: user1
            total files: 1
            transferred: 0 B
            type: replication
            status: failed

    And user of browser clicks on the "data" tab in main menu sidebar
    And user of browser uses spaces select to change data space to "smallSpace"
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely empty


  Scenario: User tries to replicate directory to too small space on remote provider
    When user of browser uses spaces select to change data space to "smallSpace"
    And user of browser creates directory "dir1"
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser uses upload button in toolbar to upload file "large_file.txt" to current dir
    And user of browser changes current working directory to smallSpace using breadcrumbs

    # Wait to ensure synchronization between providers
    And user of browser is idle for 2 seconds
    And user of browser replicates "dir1" to provider "oneprovider-2"

    # Check that transfer appeared in transfer tab
    And user of browser clicks on the "transfers" tab in main menu sidebar
    And user of browser selects "smallSpace" space in transfers tab

    Then user of browser waits for all transfers to start
    And user of browser waits for all transfers to finish
    And user of browser sees directory in ended transfers:
            name: dir1
            destination: oneprovider-2
            username: user1
            total files: 1
            transferred: 0 B
            type: replication
            status: failed

    And user of browser clicks on the "data" tab in main menu sidebar
    And user of browser uses spaces select to change data space to "smallSpace"
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely empty


  Scenario: User replicates directory with file on current provider to the same provider
    When user of browser uses spaces select to change data space to "space1"
    And user of browser creates directory "dir1"
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser uses upload button in toolbar to upload file "large_file.txt" to current dir
    And user of browser changes current working directory to space1 using breadcrumbs

    # Wait to ensure synchronization between providers
    And user of browser is idle for 2 seconds
    And user of browser replicates "dir1" to provider "oneprovider-1"

    # Check that transfer appeared in transfer tab
    And user of browser clicks on the "transfers" tab in main menu sidebar
    And user of browser selects "space1" space in transfers tab

    Then user of browser waits for all transfers to start
    And user of browser waits for all transfers to finish
    And user of browser sees directory in ended transfers:
            name: dir1
            destination: oneprovider-1
            username: user1
            total files: 0
            transferred: 0 B
            type: replication
            status: completed

    And user of browser clicks on the "data" tab in main menu sidebar
    And user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: never synchronized


  Scenario: User migrates file to remote provider
    When user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser uses upload button in toolbar to upload file "large_file.txt" to current dir

    # Wait to ensure synchronization between providers
    And user of browser is idle for 2 seconds
    And user of browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: never synchronized

    And user of browser migrates "large_file.txt" from provider "oneprovider-1" to provider "oneprovider-2"

    # Check that transfer appeared in transfer tab
    And user of browser clicks on the "transfers" tab in main menu sidebar
    And user of browser selects "space1" space in transfers tab

    Then user of browser waits for all transfers to start
    And user of browser waits for all transfers to finish
    And user of browser sees file in ended transfers:
            name: large_file.txt
            destination: oneprovider-2
            username: user1
            total files: 2
            transferred: 50 MiB
            type: migration
            status: completed

    # Check transfer chart
    And user of browser expands first transfer record
    And user of browser sees that there is non-zero throughput in transfer chart

    And user of browser clicks on the "data" tab in main menu sidebar
    And user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely empty
            oneprovider-2: entirely filled


  Scenario: User migrates directory to remote provider
    When user of browser uses spaces select to change data space to "space1"
    And user of browser creates directory "dir1"
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser uses upload button in toolbar to upload file "large_file.txt" to current dir
    And user of browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: never synchronized
    And user of browser changes current working directory to space1 using breadcrumbs

    # Wait to ensure synchronization between providers
    And user of browser is idle for 2 seconds
    And user of browser migrates "dir1" from provider "oneprovider-1" to provider "oneprovider-2"

    # Check that transfer appeared in transfer tab
    And user of browser clicks on the "transfers" tab in main menu sidebar
    And user of browser selects "space1" space in transfers tab

    Then user of browser waits for all transfers to start
    And user of browser waits for all transfers to finish
    And user of browser sees directory in ended transfers:
            name: dir1
            destination: oneprovider-2
            username: user1
            total files: 2
            transferred: 50 MiB
            type: migration
            status: completed

    And user of browser clicks on the "data" tab in main menu sidebar
    And user of browser uses spaces select to change data space to "space1"
    And user of browser sees file browser in data tab in Oneprovider page
    And user of browser double clicks on item named "dir1" in file browser
    And user of browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely empty
            oneprovider-2: entirely filled
