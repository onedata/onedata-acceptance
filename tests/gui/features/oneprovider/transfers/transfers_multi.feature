Feature: Oneprovider transfers functionality using multiple browser instances

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
    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [onezone, onezone] page
    And users of [browser1, browser2] logged as [user1, user1] to Onezone service
    And opened [oneprovider-1, oneprovider-2] Oneprovider view in web GUI by users of [browser1, browser2]


  Scenario: User replicates file from remote provider to current provider
    When user of browser1 uses spaces select to change data space to "space1"
    And user of browser1 uses upload button in toolbar to upload file "large_file.txt" to current dir

    # Wait to ensure synchronization between providers
    And user of browser1 is idle for 10 seconds
    And user of browser1 sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: never synchronized

    And user of browser2 uses spaces select to change data space to "space1"
    And user of browser2 refreshes site
    And user of browser2 replicates "large_file.txt" to provider "oneprovider-2"

    # Check that transfer appeared in transfer tab
    And user of browser1 clicks on the "transfers" tab in main menu sidebar
    And user of browser1 selects "space1" space in transfers tab
    And user of browser1 waits for all transfers to start
    And user of browser1 waits for all transfers to finish
    Then user of browser1 sees file in ended transfers:
            name: large_file.txt
            destination: oneprovider-2
            username: user1
            total files: 1
            transferred: 50 MiB
            type: replication
            status: completed

    # Check transfer chart
    And user of browser1 expands first transfer record
    And user of browser1 sees that there is non-zero throughput in transfer chart

    And user of browser2 clicks on the "data" tab in main menu sidebar
    And user of browser2 uses spaces select to change data space to "space1"
    And user of browser2 sees file browser in data tab in Oneprovider page
    And user of browser2 sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely filled


  Scenario: User replicates directory with 2 files on different providers to current provider
    When user of browser1 uses spaces select to change data space to "space1"
    And user of browser1 creates directory "dir1"
    And user of browser1 double clicks on item named "dir1" in file browser
    And user of browser1 uses upload button in toolbar to upload file "large_file.txt" to current dir
    And user of browser1 sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: never synchronized

    And user of browser2 uses spaces select to change data space to "space1"
    # Wait to ensure synchronization between providers
    And user of browser2 is idle for 2 seconds
    And user of browser2 refreshes site
    And user of browser2 sees file browser in data tab in Oneprovider page
    And user of browser2 double clicks on item named "dir1" in file browser
    And user of browser2 uses upload button in toolbar to upload file "large_file.txt" to current dir
    And user of browser2 is idle for 2 seconds
    And user of browser2 refreshes site
    And user of browser2 sees file chunks for file "large_file(1).txt" as follows:
            oneprovider-1: never synchronized
            oneprovider-2: entirely filled

    # Wait to ensure synchronization between providers
    And user of browser2 is idle for 2 seconds

    And user of browser2 changes current working directory to space1 using breadcrumbs
    And user of browser2 replicates "dir1" to provider "oneprovider-2"
    
    # Check that transfer appeared in transfer tab
    And user of browser1 clicks on the "transfers" tab in main menu sidebar
    And user of browser1 selects "space1" space in transfers tab
    And user of browser1 waits for all transfers to start
    And user of browser1 waits for all transfers to finish
    Then user of browser1 sees directory in ended transfers:
            name: dir1
            destination: oneprovider-2
            username: user1
            total files: 1
            transferred: 50 MiB
            type: replication
            status: completed

    # Check transfer chart
    And user of browser1 expands first transfer record
    And user of browser1 sees that there is non-zero throughput in transfer chart

    And user of browser1 clicks on the "data" tab in main menu sidebar
    And user of browser1 uses spaces select to change data space to "space1"
    And user of browser1 sees file browser in data tab in Oneprovider page
    And user of browser1 double clicks on item named "dir1" in file browser
    And user of browser1 is idle for 10 seconds
    And user of browser1 refreshes site
    And user of browser1 sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely filled
    And user of browser1 sees file chunks for file "large_file(1).txt" as follows:
            oneprovider-1: never synchronized
            oneprovider-2: entirely filled


  Scenario: User migrates file from remote provider to current provider
    When user of browser1 uses spaces select to change data space to "space1"
    And user of browser1 uses upload button in toolbar to upload file "large_file.txt" to current dir
    # Wait to ensure synchronization between providers
    And user of browser1 is idle for 10 seconds
    And user of browser1 sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: never synchronized

    And user of browser2 uses spaces select to change data space to "space1"
    And user of browser2 refreshes site
    And user of browser2 migrates "large_file.txt" from provider "oneprovider-1" to provider "oneprovider-2"

    # Check that transfer appeared in transfer tab
    And user of browser1 clicks on the "transfers" tab in main menu sidebar
    And user of browser1 selects "space1" space in transfers tab
    And user of browser1 waits for all transfers to start
    And user of browser1 waits for all transfers to finish
    Then user of browser1 sees file in ended transfers:
            name: large_file.txt
            destination: oneprovider-2
            username: user1
            total files: 2
            transferred: 50 MiB
            type: migration
            status: completed

    # Check transfer chart
    And user of browser1 expands first transfer record
    And user of browser1 sees that there is non-zero throughput in transfer chart

    And user of browser2 clicks on the "data" tab in main menu sidebar
    And user of browser2 uses spaces select to change data space to "space1"
    And user of browser2 sees file browser in data tab in Oneprovider page
    And user of browser2 sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely empty
            oneprovider-2: entirely filled


  Scenario: User migrates directory with 2 files on different providers to current provider
    When user of browser1 uses spaces select to change data space to "space1"
    And user of browser1 creates directory "dir1"
    And user of browser1 double clicks on item named "dir1" in file browser
    And user of browser1 uses upload button in toolbar to upload file "large_file.txt" to current dir
    And user of browser1 sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: never synchronized

    And user of browser2 uses spaces select to change data space to "space1"
    # Wait to ensure synchronization between providers
    And user of browser2 is idle for 10 seconds
    And user of browser2 refreshes site
    And user of browser2 sees file browser in data tab in Oneprovider page
    And user of browser2 double clicks on item named "dir1" in file browser
    And user of browser2 uses upload button in toolbar to upload file "large_file.txt" to current dir
    And user of browser2 is idle for 2 seconds
    And user of browser2 sees file chunks for file "large_file(1).txt" as follows:
            oneprovider-1: never synchronized
            oneprovider-2: entirely filled

    # Wait to ensure synchronization between providers
    And user of browser2 is idle for 2 seconds

    And user of browser2 changes current working directory to space1 using breadcrumbs
    And user of browser2 migrates "dir1" from provider "oneprovider-1" to provider "oneprovider-2"
    
    # Check that transfer appeared in transfer tab
    And user of browser1 clicks on the "transfers" tab in main menu sidebar
    And user of browser1 selects "space1" space in transfers tab
    And user of browser1 waits for all transfers to start
    And user of browser1 waits for all transfers to finish
    Then user of browser1 sees directory in ended transfers:
            name: dir1
            destination: oneprovider-2
            username: user1
            total files: 3
            transferred: 50 MiB
            type: migration
            status: completed

    # Check transfer chart
    And user of browser1 expands first transfer record
    And user of browser1 sees that there is non-zero throughput in transfer chart

    And user of browser1 clicks on the "data" tab in main menu sidebar
    And user of browser1 uses spaces select to change data space to "space1"
    And user of browser1 sees file browser in data tab in Oneprovider page
    And user of browser1 double clicks on item named "dir1" in file browser
    And user of browser1 refreshes site
    And user of browser1 sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely empty
            oneprovider-2: entirely filled
    And user of browser1 sees file chunks for file "large_file(1).txt" as follows:
            oneprovider-1: entirely empty
            oneprovider-2: entirely filled
