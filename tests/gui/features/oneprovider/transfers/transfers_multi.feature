Feature: Oneprovider transfers functionality using multiple browsers instances

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
    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [onezone, onezone] page
    And users of [browser1, browser2] logged as [space-owner-user, space-owner-user] to [Onezone, Onezone] service
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

    # Wait to ensure synchronization between providers
    And user of browser1 is idle for 10 seconds
    And user of browser1 sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely empty

    And user of browser2 opens oneprovider-2 Oneprovider file browser for "space1" space
    And user of browser2 replicates "large_file.txt" to provider "oneprovider-2"

    # Check that transfer appeared in transfer tab
    And user of browser1 opens oneprovider-1 Oneprovider transfers for "space1" space
    And user of browser1 waits for all transfers to start
    And user of browser1 waits for all transfers to finish
    Then user of browser1 sees file in ended transfers:
            name: large_file.txt
            replicated: 50 MiB
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
    And user of browser1 clicks and presses enter on item named "dir1" in file browser
    And user of browser1 uses upload button from file browser menu bar to upload local file "large_file.txt" to remote current dir
    And user of browser1 sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely empty

    # Wait to ensure synchronization between providers
    And user of browser2 opens oneprovider-2 Oneprovider file browser for "space1" space
    And user of browser2 clicks and presses enter on item named "dir1" in file browser
    And user of browser2 uses upload button from file browser menu bar to upload local file "large_file.txt" to remote current dir
    And user of browser2 sees file chunks for file "large_file(1).txt" as follows:
            oneprovider-1: entirely empty
            oneprovider-2: entirely filled

    # Wait to ensure synchronization between providers
    And user of browser2 is idle for 2 seconds

    And user of browser2 changes current working directory to space root using breadcrumbs
    And user of browser2 replicates "dir1" to provider "oneprovider-2"

    # Check that transfer appeared in transfer tab
    And user of browser1 opens oneprovider-1 Oneprovider transfers for "space1" space
    And user of browser1 waits for all transfers to start
    And user of browser1 waits for all transfers to finish
    Then user of browser1 sees directory in ended transfers:
            name: dir1
            replicated: 50 MiB
            type: replication
            status: completed

    # Check transfer chart
    And user of browser1 expands first transfer record
    And user of browser1 sees that there is non-zero throughput in transfer chart

    And user of browser1 clicks "Files" of "space1" space in the sidebar
    And user of browser1 sees file browser in files tab in Oneprovider page
    And user of browser1 clicks and presses enter on item named "dir1" in file browser
    And user of browser1 is idle for 10 seconds
    And user of browser1 sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely filled
    And user of browser1 sees file chunks for file "large_file(1).txt" as follows:
            oneprovider-1: entirely empty
            oneprovider-2: entirely filled


  Scenario: User migrates file from remote provider to current provider
    When user of browser1 uses upload button from file browser menu bar to upload local file "large_file.txt" to remote current dir

    # Wait to ensure synchronization between providers
    And user of browser1 is idle for 10 seconds
    And user of browser1 sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely empty

    And user of browser2 opens oneprovider-2 Oneprovider file browser for "space1" space
    And user of browser2 migrates "large_file.txt" from provider "oneprovider-1" to provider "oneprovider-2"

    # Check that transfer appeared in transfer tab
    And user of browser1 opens oneprovider-1 Oneprovider transfers for "space1" space
    And user of browser1 waits for all transfers to start
    And user of browser1 waits for all transfers to finish
    Then user of browser1 sees file in ended transfers:
            name: large_file.txt
            replicated: 50 MiB
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
    And user of browser1 clicks and presses enter on item named "dir1" in file browser
    And user of browser1 uses upload button from file browser menu bar to upload local file "large_file.txt" to remote current dir
    And user of browser1 sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely empty

    # Wait to ensure synchronization between providers
    And user of browser2 opens oneprovider-2 Oneprovider file browser for "space1" space
    And user of browser2 is idle for 10 seconds
    And user of browser2 clicks and presses enter on item named "dir1" in file browser
    And user of browser2 uses upload button from file browser menu bar to upload local file "large_file.txt" to remote current dir
    And user of browser2 sees file chunks for file "large_file(1).txt" as follows:
            oneprovider-1: entirely empty
            oneprovider-2: entirely filled

    # Wait to ensure synchronization between providers
    And user of browser2 is idle for 2 seconds

    And user of browser2 changes current working directory to space root using breadcrumbs
    And user of browser2 migrates "dir1" from provider "oneprovider-1" to provider "oneprovider-2"

    # Check that transfer appeared in transfer tab
    And user of browser1 opens oneprovider-1 Oneprovider transfers for "space1" space
    And user of browser1 waits for all transfers to start
    And user of browser1 waits for all transfers to finish
    Then user of browser1 sees directory in ended transfers:
            name: dir1
            replicated: 50 MiB
            type: migration
            status: completed

    # Check transfer chart
    And user of browser1 expands first transfer record
    And user of browser1 sees that there is non-zero throughput in transfer chart

    And user of browser1 clicks "Files" of "space1" space in the sidebar
    And user of browser1 sees file browser in files tab in Oneprovider page
    And user of browser1 clicks and presses enter on item named "dir1" in file browser
    And user of browser1 sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely empty
            oneprovider-2: entirely filled
    And user of browser1 sees file chunks for file "large_file(1).txt" as follows:
            oneprovider-1: entirely empty
            oneprovider-2: entirely filled
