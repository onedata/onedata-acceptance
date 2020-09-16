Feature: Onepanel features auto-cleaning

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - space-owner-user
    And initial spaces configuration in "onezone" Onezone service:
        space2:
            owner: space-owner-user
            providers:
                - oneprovider-2:
                    storage: posix
                    size: 10000000000

    And users opened [browser1, space_owner_browser] browsers' windows
    And users of [browser1, space_owner_browser] opened [Onezone, Onezone] page
    And user of [browser1, space_owner_browser] logged as [admin, space-owner-user] to [Onezone, Onezone] service

    And directory tree structure on local file system:
          space_owner_browser:
              large_file.txt:
                size: 50 MiB


  Scenario: User uses auto-cleaning
    Given there are no spaces supported in Onepanel used by user of browser1
    When user of space_owner_browser sends support token for "space2" to user of browser1
    And user of browser1 supports "space2" space in "oneprovider-1" Oneprovider panel service with following configuration:
           storage: posix
           size: 1
           unit: GiB

    # enable file popularity
    And user of browser1 opens "space2" record on spaces list in Spaces page in Onepanel
    And user of browser1 clicks on File popularity navigation tab in space "space2"
    And user of browser1 enables file-popularity in "space2" space in Onepanel

    # upload files to created directory
    And user of space_owner_browser opens oneprovider-1 Oneprovider file browser for "space2" space
    And user of space_owner_browser creates directory "dir1"
    And user of space_owner_browser double clicks on item named "dir1" in file browser
    And user of space_owner_browser uses upload button from file browser menu bar to upload local file "large_file.txt" to remote current dir
    And user of space_owner_browser uses upload button from file browser menu bar to upload local file "large_file.txt" to remote current dir
    And user of space_owner_browser waits for file upload to finish
    And user of space_owner_browser uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
    And user of space_owner_browser changes current working directory to home using breadcrumbs
    And user of space_owner_browser is idle for 10 seconds

    # replicate data
    And user of space_owner_browser replicates "dir1" to provider "oneprovider-2"
    And user of space_owner_browser opens oneprovider-1 Oneprovider transfers for "space2" space
    And user of space_owner_browser waits for all transfers to start
    And user of space_owner_browser waits for all transfers to finish
    And user of space_owner_browser sees directory in ended transfers:
            name: dir1
            destination: oneprovider-2
            username: space-owner-user
            transferred: 100 MiB
            type: replication
            status: completed

    # check data distribution
    And user of space_owner_browser clicks Data of "space2" in the sidebar
    And user of space_owner_browser sees file browser in data tab in Oneprovider page
    And user of space_owner_browser double clicks on item named "dir1" in file browser
    And user of space_owner_browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely filled
    And user of space_owner_browser sees file chunks for file "large_file(1).txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely filled

    # enable auto-cleaning
    And user of browser1 is idle for 8 seconds
    And user of browser1 clicks on "Auto cleaning" navigation tab in space "space2"
    And user of browser1 enables auto-cleaning in "space2" space in Onepanel

    # set soft quota
    And user of browser1 clicks change soft quota button in auto-cleaning tab in Onepanel
    And user of browser1 types "0.05" to soft quota input field in auto-cleaning tab in Onepanel
    And user of browser1 confirms changing value of soft quota in auto-cleaning tab in Onepanel

    # set hard quota
    And user of browser1 clicks change hard quota button in auto-cleaning tab in Onepanel
    And user of browser1 types "0.06" to hard quota input field in auto-cleaning tab in Onepanel
    And user of browser1 confirms changing value of hard quota in auto-cleaning tab in Onepanel

    And user of browser1 clicks on "Start cleaning now" button in auto-cleaning tab in Onepanel
    And user of browser1 is idle for 5 seconds
    Then user of browser1 sees 100 MiB released size in cleaning report in Onepanel

    # check data distribution
    And user of space_owner_browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely empty
            oneprovider-2: entirely filled
    And user of space_owner_browser sees file chunks for file "large_file(1).txt" as follows:
            oneprovider-1: entirely empty
            oneprovider-2: entirely filled

    # revoke space support
    And user of browser1 revokes "space2" space support in "oneprovider-1" provider in Onepanel


  Scenario: User uses auto-cleaning with lower size limit which skips too small files
    Given there are no spaces supported in Onepanel used by user of browser1
    When user of space_owner_browser sends support token for "space2" to user of browser1
    And user of browser1 supports "space2" space in "oneprovider-1" Oneprovider panel service with following configuration:
            storage: posix
            size: 1
            unit: GiB

    # enable file popularity
    And user of browser1 opens "space2" record on spaces list in Spaces page in Onepanel
    And user of browser1 clicks on File popularity navigation tab in space "space2"
    And user of browser1 enables file-popularity in "space2" space in Onepanel

    # upload files to created directory
    And user of space_owner_browser opens oneprovider-1 Oneprovider file browser for "space2" space
    And user of space_owner_browser creates directory "dir1"
    And user of space_owner_browser double clicks on item named "dir1" in file browser
    And user of space_owner_browser uses upload button from file browser menu bar to upload local file "large_file.txt" to remote current dir
    And user of space_owner_browser uses upload button from file browser menu bar to upload local file "large_file.txt" to remote current dir
    And user of space_owner_browser waits for file upload to finish
    And user of space_owner_browser changes current working directory to home using breadcrumbs
    And user of space_owner_browser is idle for 10 seconds

    # replicate data
    And user of space_owner_browser replicates "dir1" to provider "oneprovider-2"
    And user of space_owner_browser opens oneprovider-1 Oneprovider transfers for "space2" space
    And user of space_owner_browser waits for all transfers to start
    And user of space_owner_browser waits for all transfers to finish
    And user of space_owner_browser sees directory in ended transfers:
            name: dir1
            destination: oneprovider-2
            username: space-owner-user
            transferred: 100 MiB
            type: replication
            status: completed

    # check data distribution
    And user of space_owner_browser clicks Data of "space2" in the sidebar
    And user of space_owner_browser sees file browser in data tab in Oneprovider page
    And user of space_owner_browser double clicks on item named "dir1" in file browser
    And user of space_owner_browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely filled
    And user of space_owner_browser sees file chunks for file "large_file(1).txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely filled

    # enable auto-cleaning and set selective cleaning
    And user of browser1 is idle for 8 seconds
    And user of browser1 clicks on "Auto cleaning" navigation tab in space "space2"
    And user of browser1 enables auto-cleaning in "space2" space in Onepanel
    And user of browser1 enables selective cleaning in auto-cleaning tab in Onepanel
    And user of browser1 enables Lower size limit in auto-cleaning tab in Onepanel
    And user of browser1 clicks GiB on dropdown Lower size limit rule in auto-cleaning tab in Onepanel
    And user of browser1 is idle for 8 seconds

    And user of browser1 sets soft quota to 0.05 value in auto-cleaning tab in Onepanel
    And user of browser1 sets hard quota to 0.06 value in auto-cleaning tab in Onepanel

    And user of browser1 clicks on "Start cleaning now" button in auto-cleaning tab in Onepanel
    And user of browser1 is idle for 5 seconds
    Then user of browser1 sees 0 B released size in cleaning report in Onepanel

    # check data distribution
    And user of space_owner_browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely filled
    And user of space_owner_browser sees file chunks for file "large_file(1).txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely filled

    # revoke space support
    And user of browser1 revokes "space2" space support in "oneprovider-1" provider in Onepanel


  Scenario: User uses auto-cleaning with upper size limit which skips too big files
    Given there are no spaces supported in Onepanel used by user of browser1
    When user of space_owner_browser sends support token for "space2" to user of browser1
    And user of browser1 supports "space2" space in "oneprovider-1" Oneprovider panel service with following configuration:
            storage: posix
            size: 1
            unit: GiB

    # enable file popularity
    And user of browser1 opens "space2" record on spaces list in Spaces page in Onepanel
    And user of browser1 clicks on File popularity navigation tab in space "space2"
    And user of browser1 enables file-popularity in "space2" space in Onepanel

    # upload files to created directory
    And user of space_owner_browser opens oneprovider-1 Oneprovider file browser for "space2" space
    And user of space_owner_browser creates directory "dir1"
    And user of space_owner_browser double clicks on item named "dir1" in file browser
    And user of space_owner_browser uses upload button from file browser menu bar to upload local file "large_file.txt" to remote current dir
    And user of space_owner_browser uses upload button from file browser menu bar to upload local file "large_file.txt" to remote current dir
    And user of space_owner_browser waits for file upload to finish
    And user of space_owner_browser uses upload button from file browser menu bar to upload file "20B-0.txt" to current dir
    And user of space_owner_browser is idle for 10 seconds
    And user of space_owner_browser changes current working directory to home using breadcrumbs

    # replicate data
    And user of space_owner_browser replicates "dir1" to provider "oneprovider-2"
    And user of space_owner_browser opens oneprovider-1 Oneprovider transfers for "space2" space
    And user of space_owner_browser waits for all transfers to start
    And user of space_owner_browser waits for all transfers to finish
    And user of space_owner_browser sees directory in ended transfers:
            name: dir1
            destination: oneprovider-2
            username: space-owner-user
            transferred: 100 MiB
            type: replication
            status: completed

    # check data distribution
    And user of space_owner_browser clicks Data of "space2" in the sidebar
    And user of space_owner_browser sees file browser in data tab in Oneprovider page
    And user of space_owner_browser double clicks on item named "dir1" in file browser
    And user of space_owner_browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely filled
    And user of space_owner_browser sees file chunks for file "large_file(1).txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely filled
    And user of space_owner_browser sees file chunks for file "20B-0.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely filled

    # enable auto-cleaning and set selective cleaning
    And user of browser1 is idle for 8 seconds
    And user of browser1 clicks on "Auto cleaning" navigation tab in space "space2"
    And user of browser1 enables auto-cleaning in "space2" space in Onepanel
    And user of browser1 enables selective cleaning in auto-cleaning tab in Onepanel
    And user of browser1 enables Upper size limit in auto-cleaning tab in Onepanel
    And user of browser1 clicks MiB on dropdown Upper size limit rule in auto-cleaning tab in Onepanel
    And user of browser1 is idle for 8 seconds

    And user of browser1 sets soft quota to 0.05 value in auto-cleaning tab in Onepanel
    And user of browser1 sets hard quota to 0.06 value in auto-cleaning tab in Onepanel

    And user of browser1 clicks on "Start cleaning now" button in auto-cleaning tab in Onepanel
    And user of browser1 is idle for 5 seconds
    Then user of browser1 sees 20 B released size in cleaning report in Onepanel

    # check data distribution
    And user of space_owner_browser sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely filled
    And user of space_owner_browser sees file chunks for file "large_file(1).txt" as follows:
            oneprovider-1: entirely filled
            oneprovider-2: entirely filled
    And user of space_owner_browser sees file chunks for file "20B-0.txt" as follows:
            oneprovider-1: entirely empty
            oneprovider-2: entirely filled

    # revoke space support
    And user of browser1 revokes "space2" space support in "oneprovider-1" provider in Onepanel

