Feature: Oneprovider transfers directories functionality

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


#  Scenario: User replicates directory to remote provider
#    When user of browser opens oneprovider-1 Oneprovider file browser for "space1" space
#    And user of browser creates directory "dir1"
#    And user of browser clicks and presses enter on item named "dir1" in file browser
#    And user of browser uses upload button from file browser menu bar to upload local file "large_file.txt" to remote current dir
#    And user of browser sees file chunks for file "large_file.txt" as follows:
#            oneprovider-1: entirely filled
#            oneprovider-2: entirely empty
#    And user of browser changes current working directory to space root using breadcrumbs
#
#    # Wait to ensure synchronization between providers
#    And user of browser is idle for 2 seconds
#
#    And user of browser replicates "dir1" to provider "oneprovider-2"
#
#    # Check that transfer appeared in transfer tab
#    And user of browser opens oneprovider-1 Oneprovider transfers for "space1" space
#    Then user of browser waits for all transfers to start
#    And user of browser waits for all transfers to finish
#    And user of browser sees directory in ended transfers:
#            name: dir1
#            replicated: 50 MiB
#            type: replication
#            status: completed
#
#    # Check transfer chart
#    And user of browser expands first transfer record
#    And user of browser sees that there is non-zero throughput in transfer chart
#
#    And user of browser clicks "Files" of "space1" space in the sidebar
#    And user of browser sees file browser in files tab in Oneprovider page
#    And user of browser clicks and presses enter on item named "dir1" in file browser
#    And user of browser sees file chunks for file "large_file.txt" as follows:
#            oneprovider-1: entirely filled
#            oneprovider-2: entirely filled
#
#
#  Scenario: User tries to migrate directory to too small space on remote provider
#    When user of browser opens oneprovider-1 Oneprovider file browser for "smallSpace" space
#    And user of browser creates directory "dir1"
#    And user of browser clicks and presses enter on item named "dir1" in file browser
#    And user of browser uses upload button from file browser menu bar to upload local file "large_file.txt" to remote current dir
#    And user of browser changes current working directory to space root using breadcrumbs
#
#    # Wait to ensure synchronization between providers
#    And user of browser is idle for 2 seconds
#
#    And user of browser migrates "dir1" from provider "oneprovider-1" to provider "oneprovider-2"
#
#    # Check that transfer appeared in transfer tab
#    And user of browser opens oneprovider-1 Oneprovider transfers for "smallSpace" space
#    Then user of browser waits for all transfers to start
#    And user of browser waits for all transfers to finish
#    And user of browser sees directory in ended transfers:
#            name: dir1
#            replicated: 0 B
#            type: migration
#            status: failed
#
#    And user of browser clicks "Files" of "smallSpace" space in the sidebar
#    And user of browser sees file browser in files tab in Oneprovider page
#    And user of browser clicks and presses enter on item named "dir1" in file browser
#    And user of browser sees file chunks for file "large_file.txt" as follows:
#            oneprovider-1: entirely filled
#            oneprovider-2: entirely empty
#
#
#  Scenario: User tries to replicate directory to too small space on remote provider
#    When user of browser opens oneprovider-1 Oneprovider file browser for "smallSpace" space
#    And user of browser creates directory "dir1"
#    And user of browser clicks and presses enter on item named "dir1" in file browser
#    And user of browser uses upload button from file browser menu bar to upload local file "large_file.txt" to remote current dir
#    And user of browser changes current working directory to space root using breadcrumbs
#
#    # Wait to ensure synchronization between providers
#    And user of browser is idle for 2 seconds
#
#    And user of browser replicates "dir1" to provider "oneprovider-2"
#
#    # Check that transfer appeared in transfer tab
#    And user of browser opens oneprovider-1 Oneprovider transfers for "smallSpace" space
#    Then user of browser waits for all transfers to start
#    And user of browser waits for all transfers to finish
#    And user of browser sees directory in ended transfers:
#            name: dir1
#            replicated: 0 B
#            type: replication
#            status: failed
#
#    And user of browser clicks "Files" of "smallSpace" space in the sidebar
#    And user of browser sees file browser in files tab in Oneprovider page
#    And user of browser clicks and presses enter on item named "dir1" in file browser
#    And user of browser sees file chunks for file "large_file.txt" as follows:
#            oneprovider-1: entirely filled
#            oneprovider-2: entirely empty
#
#
#  Scenario: User cannot replicates directory to the same provider with directory statistics turn on
#    When user of browser opens oneprovider-1 Oneprovider file browser for "space1" space
#    And user of browser creates directory "dir1"
#    And user of browser clicks and presses enter on item named "dir1" in file browser
#    And user of browser uses upload button from file browser menu bar to upload local file "large_file.txt" to remote current dir
#    And user of browser changes current working directory to space root using breadcrumbs
#
#    # Wait to ensure synchronization between providers
#    And user of browser is idle for 2 seconds
#
#    And user of browser clicks on menu for "dir1" directory in file browser
#    And user of browser clicks "Data distribution" option in data row menu in file browser
#    And user of browser clicks on menu button for "oneprovider-1" provider in "Data distribution" panel
#    Then user of browser cannot click "Replicate here" option in data row menu for "oneprovider-1" provider in "Data distribution" panel


  Scenario: User sees that empty transfer is created and finished after replicating directory to the same provider without directory statistics
    When user of browser opens oneprovider-1 Oneprovider file browser for "space1" space

    And user of browser clicks "Providers" of "space1" space in the sidebar
    And user of browser clicks on "oneprovider-1" provider on providers page
    And user of browser unchecks size statistics toggle on space configuration page
    And user of browser clicks on "Disable" button in modal "Disable directory statistics"

    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser creates directory "dir1"
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser uses upload button from file browser menu bar to upload local file "large_file.txt" to remote current dir
    And user of browser changes current working directory to space root using breadcrumbs

    # Wait to ensure synchronization between providers
    And user of browser is idle for 2 seconds

    And user of browser replicates "dir1" to provider "oneprovider-1"

    # Check that transfer appeared in transfer tab
    And user of browser opens oneprovider-1 Oneprovider transfers for "space1" space
    Then user of browser waits for all transfers to start
    And user of browser waits for all transfers to finish
    And user of browser sees directory in ended transfers:
            name: dir1
            replicated: 0 B
            type: replication
            status: completed

    And user of browser clicks "Files" of "space1" space in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely empty


#  Scenario: User migrates directory to remote provider
#    When user of browser opens oneprovider-1 Oneprovider file browser for "space1" space
#    And user of browser creates directory "dir1"
#    And user of browser clicks and presses enter on item named "dir1" in file browser
#    And user of browser uses upload button from file browser menu bar to upload local file "large_file.txt" to remote current dir
#    And user of browser sees file chunks for file "large_file.txt" as follows:
#            oneprovider-1: entirely filled
#            oneprovider-2: entirely empty
#    And user of browser changes current working directory to space root using breadcrumbs
#
#    # Wait to ensure synchronization between providers
#    And user of browser is idle for 2 seconds
#
#    And user of browser migrates "dir1" from provider "oneprovider-1" to provider "oneprovider-2"
#
#    # Check that transfer appeared in transfer tab
#    And user of browser opens oneprovider-1 Oneprovider transfers for "space1" space
#    Then user of browser waits for all transfers to start
#    And user of browser waits for all transfers to finish
#    And user of browser sees directory in ended transfers:
#            name: dir1
#            replicated: 50 MiB
#            type: migration
#            status: completed
#
#    And user of browser clicks "Files" of "space1" space in the sidebar
#    And user of browser sees file browser in files tab in Oneprovider page
#    And user of browser clicks and presses enter on item named "dir1" in file browser
#    And user of browser sees file chunks for file "large_file.txt" as follows:
#            oneprovider-1: entirely empty
#            oneprovider-2: entirely filled
#
