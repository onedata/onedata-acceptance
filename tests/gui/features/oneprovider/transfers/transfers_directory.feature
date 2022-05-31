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
                    size: 4000000000
                - oneprovider-2:
                    storage: posix
                    size: 4000000000
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
            larger_file.txt:
              size: 3000 MiB

    And user of browser replicates "dir1" to provider "oneprovider-1"

    # Check that transfer appeared in transfer tab
    And user of browser opens oneprovider-1 Oneprovider transfers for "space1" space
    Then user of browser waits for all transfers to start
    And user of browser waits for all transfers to finish
    And user of browser sees directory in ended transfers:
            name: dir1
            destination: oneprovider-1
            username: space-owner-user
            transferred: 0 B
            type: replication
            status: completed

    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely empty


  Scenario: User migrates directory to remote provider
    When user of browser opens oneprovider-1 Oneprovider file browser for "space1" space
    And user of browser creates directory "dir1"
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser uses upload button from file browser menu bar to upload local file "large_file.txt" to remote current dir
    And user of browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely empty
    And user of browser changes current working directory to space root using breadcrumbs

    # Wait to ensure synchronization between providers
    And user of browser is idle for 2 seconds

    And user of browser migrates "dir1" from provider "oneprovider-1" to provider "oneprovider-2"

    # Check that transfer appeared in transfer tab
    And user of browser opens oneprovider-1 Oneprovider transfers for "space1" space
    Then user of browser waits for all transfers to start
    And user of browser waits for all transfers to finish
    And user of browser sees directory in ended transfers:
            name: dir1
            destination: oneprovider-2
            username: space-owner-user
            transferred: 50 MiB
            type: migration
            status: completed

    And user of browser clicks Files of "space1" in the sidebar
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely empty
            oneprovider-2: entirely filled


  Scenario: User reruns directory transfer to remote provider after canceling it
    When user of browser opens oneprovider-1 Oneprovider file browser for "space1" space
    And user of browser creates directory "dir1"
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser uses upload button from file browser menu bar to upload local file "larger_file.txt" to remote current dir
    And user of browser changes current working directory to space root using breadcrumbs

    # Wait to ensure synchronization between providers
    And user of browser is idle for 2 seconds
    And user of browser replicates "dir1" to provider "oneprovider-2"

    # Check that transfer appeared in transfer tab
    And user of browser opens oneprovider-1 Oneprovider transfers for "space1" space
    And user of browser cancels transfer in waiting transfers
    And user of browser waits for all transfers to start
    And user of browser waits for all transfers to finish
    And user of browser sees directory in ended transfers:
            name: dir1
            destination: oneprovider-2
            transferred: <= 2.9 GB
            type: replication
            status: cancelled
    Then user of browser reruns transfer in ended transfers
    And user of browser waits for all transfers to start
    And user of browser waits for all transfers to finish
    And user of browser sees directory in ended transfers:
            name: dir1
            destination: oneprovider-2
            transferred: <= 2.9 GB
            type: replication
            status: completed


