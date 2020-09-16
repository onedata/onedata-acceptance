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
    And users of [browser1, browser2] logged as [user1, user1] to [Onezone, Onezone] service
    And opened oneprovider-1 Oneprovider file browser for "space1" space in web GUI by users of browser1

    And directory tree structure on local file system:
          browser1:
            large_file.txt:
              size: 50 MiB
          browser2:
            large_file.txt:
              size: 50 MiB


  Scenario: User replicates file from remote provider to current provider
    When user of browser1 uses upload button from file browser menu bar to upload local file "large_file.txt" to remote current dir
    And user of browser1 waits for file upload to finish

    # Wait to ensure synchronization between providers
    And user of browser1 is idle for 10 seconds
    And user of browser1 sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: never synchronized

    And user of browser2 opens oneprovider-2 Oneprovider file browser for "space1" space
    And user of browser2 replicates "large_file.txt" to provider "oneprovider-2"

    # Check that transfer appeared in transfer tab
    And user of browser1 opens oneprovider-1 Oneprovider transfers for "space1" space
    And user of browser1 waits for all transfers to start
    And user of browser1 waits for all transfers to finish
    Then user of browser1 sees file in ended transfers:
            name: large_file.txt
            destination: oneprovider-2
            username: user1
            transferred: 50 MiB
            type: replication
            status: completed

    # Check transfer chart
    And user of browser1 expands first transfer record
    And user of browser1 sees that there is non-zero throughput in transfer chart

    And user of browser2 sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely filled


  Scenario: User replicates directory with 2 files on different providers to current provider
    When user of browser1 creates directory "dir1"
    And user of browser1 double clicks on item named "dir1" in file browser
    And user of browser1 uses upload button from file browser menu bar to upload local file "large_file.txt" to remote current dir
    And user of browser1 waits for file upload to finish
    And user of browser1 sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: never synchronized

    # Wait to ensure synchronization between providers
    And user of browser2 opens oneprovider-2 Oneprovider file browser for "space1" space
    And user of browser2 double clicks on item named "dir1" in file browser
    And user of browser2 uses upload button from file browser menu bar to upload local file "large_file.txt" to remote current dir
    And user of browser2 waits for file upload to finish
    And user of browser2 is idle for 2 seconds
    And user of browser2 sees file chunks for file "large_file(1).txt" as follows:
            oneprovider-1: never synchronized
            oneprovider-2: entirely filled

    # Wait to ensure synchronization between providers
    And user of browser2 is idle for 2 seconds

    And user of browser2 changes current working directory to home using breadcrumbs
    And user of browser2 replicates "dir1" to provider "oneprovider-2"

    # Check that transfer appeared in transfer tab
    And user of browser1 opens oneprovider-1 Oneprovider transfers for "space1" space
    And user of browser1 waits for all transfers to start
    And user of browser1 waits for all transfers to finish
    Then user of browser1 sees directory in ended transfers:
            name: dir1
            destination: oneprovider-2
            username: user1
            transferred: 50 MiB
            type: replication
            status: completed

    # Check transfer chart
    And user of browser1 expands first transfer record
    And user of browser1 sees that there is non-zero throughput in transfer chart

    And user of browser1 clicks Data of "space1" in the sidebar
    And user of browser1 sees file browser in data tab in Oneprovider page
    And user of browser1 double clicks on item named "dir1" in file browser
    And user of browser1 is idle for 10 seconds
    And user of browser1 sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely filled
    And user of browser1 sees file chunks for file "large_file(1).txt" as follows:
            oneprovider-1: never synchronized
            oneprovider-2: entirely filled


  Scenario: User migrates file from remote provider to current provider
    When user of browser1 uses upload button from file browser menu bar to upload local file "large_file.txt" to remote current dir

    # Wait to ensure synchronization between providers
    And user of browser1 is idle for 10 seconds
    And user of browser1 sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: never synchronized

    And user of browser2 opens oneprovider-2 Oneprovider file browser for "space1" space
    And user of browser2 migrates "large_file.txt" from provider "oneprovider-1" to provider "oneprovider-2"

    # Check that transfer appeared in transfer tab
    And user of browser1 opens oneprovider-1 Oneprovider transfers for "space1" space
    And user of browser1 waits for all transfers to start
    And user of browser1 waits for all transfers to finish
    Then user of browser1 sees file in ended transfers:
            name: large_file.txt
            destination: oneprovider-2
            username: user1
            transferred: 50 MiB
            type: migration
            status: completed

    # Check transfer chart
    And user of browser1 expands first transfer record
    And user of browser1 sees that there is non-zero throughput in transfer chart

    And user of browser2 sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely empty
            oneprovider-2: entirely filled


  Scenario: User migrates directory with 2 files on different providers to current provider
    When user of browser1 creates directory "dir1"
    And user of browser1 double clicks on item named "dir1" in file browser
    And user of browser1 uses upload button from file browser menu bar to upload local file "large_file.txt" to remote current dir
    And user of browser1 waits for file upload to finish
    And user of browser1 sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: never synchronized

    # Wait to ensure synchronization between providers
    And user of browser2 opens oneprovider-2 Oneprovider file browser for "space1" space
    And user of browser2 is idle for 10 seconds
    And user of browser2 double clicks on item named "dir1" in file browser
    And user of browser2 uses upload button from file browser menu bar to upload local file "large_file.txt" to remote current dir
    And user of browser2 waits for file upload to finish
    And user of browser2 is idle for 2 seconds
    And user of browser2 sees file chunks for file "large_file(1).txt" as follows:
            oneprovider-1: never synchronized
            oneprovider-2: entirely filled

    # Wait to ensure synchronization between providers
    And user of browser2 is idle for 2 seconds

    And user of browser2 changes current working directory to home using breadcrumbs
    And user of browser2 migrates "dir1" from provider "oneprovider-1" to provider "oneprovider-2"

    # Check that transfer appeared in transfer tab
    And user of browser1 opens oneprovider-1 Oneprovider transfers for "space1" space
    And user of browser1 waits for all transfers to start
    And user of browser1 waits for all transfers to finish
    Then user of browser1 sees directory in ended transfers:
            name: dir1
            destination: oneprovider-2
            username: user1
            transferred: 50 MiB
            type: migration
            status: completed

    # Check transfer chart
    And user of browser1 expands first transfer record
    And user of browser1 sees that there is non-zero throughput in transfer chart

    And user of browser1 clicks Data of "space1" in the sidebar
    And user of browser1 sees file browser in data tab in Oneprovider page
    And user of browser1 double clicks on item named "dir1" in file browser
    And user of browser1 sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely empty
            oneprovider-2: entirely filled
    And user of browser1 sees file chunks for file "large_file(1).txt" as follows:
            oneprovider-1: entirely empty
            oneprovider-2: entirely filled
