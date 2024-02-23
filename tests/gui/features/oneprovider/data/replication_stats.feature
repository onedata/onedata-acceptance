Feature: Directories and files replications stats


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial spaces configuration in "onezone" Onezone service:
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
                    - file1: 1111111111
                    - dir1:
                        - file1: 1111111111
                        - file2: 1111111111
                        - file3: 1111111111
                        - file4: 1111111111
                    - dir2
    And directory tree structure on local file system:
          browser:
            dir2: 101
    And user opened browser window
    And user of browser opened onezone page
    And user of browser logged as user1 to Onezone service


  Scenario: User sees actual file replication rate for a file replicated to another provider
    When user of browser opens file browser for "space1" space
    And user of browser enables only ["Size", "Replication"] columns in columns configuration popover in file browser table
    Then user of browser sees that item named "file1" has 100% replication rate in file browser
    And user of browser clicks on "Choose other Oneprovider" on file browser page
    And user of browser clicks on "oneprovider-2" provider on file browser page
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that item named "file1" has 0% replication rate in file browser

    And user of browser replicates "file1" to provider "oneprovider-2"
    And user of browser opens oneprovider-1 Oneprovider transfers for "space1" space
    And user of browser waits for all transfers to start
    And user of browser waits for all transfers to finish
    And user of browser opens file browser for "space1" space
    And user of browser sees that item named "file1" has 100% replication rate in file browser
    And user of browser clicks on "Choose other Oneprovider" on file browser page
    And user of browser clicks on "oneprovider-1" provider on file browser page
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that item named "file1" has 100% replication rate in file browser


  Scenario: User sees actual file replication rate for a directory distributed between providers
    When user of browser opens file browser for "space1" space
    And user of browser enables only ["Size", "Replication"] columns in columns configuration popover in file browser table
    And user of browser sees that item named "dir1" has 100% replication rate in file browser
    And user of browser clicks and presses enter on item named "dir1" in file browser
    And user of browser migrates "file1" from provider "oneprovider-1" to provider "oneprovider-2"
    And user of browser opens oneprovider-1 Oneprovider transfers for "space1" space
    And user of browser waits for all transfers to start
    And user of browser waits for all transfers to finish
    And user of browser opens file browser for "space1" space
    Then user of browser sees that item named "dir1" has 75% replication rate in file browser
    And user of browser clicks on "Choose other Oneprovider" on file browser page
    And user of browser clicks on "oneprovider-2" provider on file browser page
    And user of browser sees file browser in files tab in Oneprovider page
    And user of browser sees that item named "dir1" has 25% replication rate in file browser


  Scenario: User sees actual file replication rate that is lower than 1%
    When user of browser opens file browser for "space1" space
    And user of browser enables only ["Size", "Replication"] columns in columns configuration popover in file browser table
    And user of browser clicks and presses enter on item named "dir2" in file browser
    And user of browser uses upload button from file browser menu bar to upload files from local directory "dir2" to remote current dir
    And user of browser migrates "file10.txt" from provider "oneprovider-1" to provider "oneprovider-2"
    And user of browser opens oneprovider-1 Oneprovider transfers for "space1" space
    And user of browser waits for all transfers to start
    And user of browser waits for all transfers to finish
    And user of browser opens file browser for "space1" space
    And user of browser clicks on "Choose other Oneprovider" on file browser page
    And user of browser clicks on "oneprovider-2" provider on file browser page
    And user of browser sees file browser in files tab in Oneprovider page
    Then user of browser sees that item named "dir2" has < 1% replication rate in file browser
