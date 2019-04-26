Feature: Onepanel features auto-cleaning

  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1
    And initial spaces configuration in "onezone" Onezone service:
        space1:
            owner: user1
            providers:
                - oneprovider-2:
                    storage: posix
                    size: 100000000

    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, Onezone] page
    And user of [browser1, browser2] logged as [admin, user1] to [Onezone, Onezone] service


  Scenario: User uses auto-cleaning
    Given there are no spaces supported in Onepanel used by user of browser1

    # receive support token
    When user of browser2 clicks "space1" on the spaces list in the sidebar
    And user of browser2 clicks Providers of "space1" in the sidebar
    And user of browser2 clicks Get support button on providers page
    And user of browser2 clicks Copy button on Get support page
    And user of browser2 sees an info notify with text matching to: .*copied.*
    And user of browser2 sends copied token to user of browser1

    # support space
    And user of browser1 selects "posix" from storage selector in support space form in Onepanel
    And user of browser1 types received token to Support token field in support space form in Onepanel
    And user of browser1 types "1" to Size input field in support space form in Onepanel
    And user of browser1 selects GiB radio button in support space form in Onepanel
    And user of browser1 clicks on Support space button in support space form in Onepanel
    And user of browser1 sees an info notify with text matching to: .*[Aa]dded.*support.*space.*
    And user of browser1 sees that space support record for "space1" has appeared in Spaces page in Onepanel

    # enable file popularity
    And user of browser1 expands "space1" record on spaces list in Spaces page in Onepanel
    And user of browser1 clicks on File popularity navigation tab in space "space1"
    And user of browser1 enables file-popularity in "space1" space in Onepanel

    # confirm support of space and go to provider
    And user of browser2 clicks "space1" on the spaces list in the sidebar
    And user of browser2 clicks Providers of "space1" in the sidebar
    And user of browser2 sees "oneprovider-1" is on the providers list
    And user of browser2 opens oneprovider-1 Oneprovider view in web GUI
    And user of browser2 sees that Oneprovider session has started
    And user of browser2 uses spaces select to change data space to "space1"

    And user of browser2 creates directory "dir1"
    And user of browser2 double clicks on item named "dir1" in file browser
    And user of browser2 uses upload button in toolbar to upload file "large_file.txt" to current dir
    And user of browser2 uses upload button in toolbar to upload file "large_file.txt" to current dir
    And user of browser2 uses upload button in toolbar to upload file "20B-0.txt" to current dir
    And user of browser2 is idle for 10 seconds
    And user of browser2 refreshes site
    And user of browser2 sees file browser in data tab in Oneprovider page
    And user of browser2 changes current working directory to space1 using breadcrumbs

    # replicate data
    And user of browser2 replicates "dir1" to provider "oneprovider-2"
    And user of browser2 clicks on the "transfers" tab in main menu sidebar
    And user of browser2 selects "space1" space in transfers tab
    And user of browser2 waits for all transfers to start
    And user of browser2 waits for all transfers to finish
    And user of browser2 sees directory in ended transfers:
            name: dir1
            destination: oneprovider-2
            username: user1
            total files: 3
            transferred: 100 MiB
            type: replication
            status: completed

    And user of browser1 is idle for 8 seconds
    And user of browser1 clicks on "Auto cleaning" navigation tab in space "space1"
    And user of browser1 enables auto-cleaning in "space1" space in Onepanel

    And user of browser1 clicks change soft quota button in auto-cleaning tab in Onepanel
    And user of browser1 types "0.05" to soft quota input field in auto-cleaning tab in Onepanel
    And user of browser1 confirms changing value of soft quota in auto-cleaning tab in Onepanel

    And user of browser1 clicks change hard quota button in auto-cleaning tab in Onepanel
    And user of browser1 types "0.06" to hard quota input field in auto-cleaning tab in Onepanel
    And user of browser1 confirms changing value of hard quota in auto-cleaning tab in Onepanel

    And user of browser1 clicks on "Start cleaning now" button in auto-cleaning tab in Onepanel
    And user of browser1 is idle for 5 seconds
    Then user of browser1 sees 100 MiB released size in cleaning report in Onepanel

    And user of browser2 clicks on the "data" tab in main menu sidebar
    And user of browser2 uses spaces select to change data space to "space1"
    And user of browser2 sees file browser in data tab in Oneprovider page
    And user of browser2 double clicks on item named "dir1" in file browser
    And user of browser2 sees file chunks for file "large_file.txt" as follows:
            oneprovider-1: entirely empty
            oneprovider-2: entirely filled
    And user of browser2 sees file chunks for file "large_file(1).txt" as follows:
            oneprovider-1: entirely empty
            oneprovider-2: entirely filled

    # revoke space support
    And user of browser1 clicks on Spaces item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of browser1 expands toolbar for "space1" space record in Spaces page in Onepanel
    And user of browser1 clicks on Revoke space support option in space's toolbar in Onepanel
    And user of browser1 clicks on Yes, revoke button in REVOKE SPACE SUPPORT modal in Onepanel
    And user of browser1 sees an info notify with text matching to: .*[Ss]upport.*revoked.*


#  Scenario: User uses auto-cleaning with lower size limit which skips too small files
#    Given there are no spaces supported in Onepanel used by user of browser1
#
#    # receive support token
#    When user of browser2 clicks "space1" on the spaces list in the sidebar
#    And user of browser2 clicks Providers of "space1" in the sidebar
#    And user of browser2 clicks Get support button on providers page
#    And user of browser2 clicks Copy button on Get support page
#    And user of browser2 sees an info notify with text matching to: .*copied.*
#    And user of browser2 sends copied token to user of browser1
#
#    # support space
#    And user of browser1 selects "posix" from storage selector in support space form in Onepanel
#    And user of browser1 types received token to Support token field in support space form in Onepanel
#    And user of browser1 types "1" to Size input field in support space form in Onepanel
#    And user of browser1 selects GiB radio button in support space form in Onepanel
#    And user of browser1 clicks on Support space button in support space form in Onepanel
#    And user of browser1 sees an info notify with text matching to: .*[Aa]dded.*support.*space.*
#    And user of browser1 sees that space support record for "space1" has appeared in Spaces page in Onepanel
#
#    # enable files popularity
#    And user of browser1 expands "space1" record on spaces list in Spaces page in Onepanel
#    And user of browser1 clicks on File popularity navigation tab in space "space1"
#    And user of browser1 enables file-popularity in "space1" space in Onepanel
#
#    # confirm support of space and go to provider
#    And user of browser2 clicks "space1" on the spaces list in the sidebar
#    And user of browser2 clicks Providers of "space1" in the sidebar
#    And user of browser2 sees "oneprovider-1" is on the providers list
#    And user of browser2 opens oneprovider-1 Oneprovider view in web GUI
#    And user of browser2 sees that Oneprovider session has started
#    And user of browser2 uses spaces select to change data space to "space1"
#
#    And user of browser2 creates directory "dir1"
#    And user of browser2 double clicks on item named "dir1" in file browser
#    And user of browser2 uses upload button in toolbar to upload file "large_file.txt" to current dir
#    And user of browser2 uses upload button in toolbar to upload file "large_file.txt" to current dir
#    And user of browser2 is idle for 10 seconds
#    And user of browser2 refreshes site
#    And user of browser2 sees file browser in data tab in Oneprovider page
#    And user of browser2 changes current working directory to space1 using breadcrumbs
#
#    # replicate data
#    And user of browser2 replicates "dir1" to provider "oneprovider-2"
#    And user of browser2 clicks on the "transfers" tab in main menu sidebar
#    And user of browser2 selects "space1" space in transfers tab
#    And user of browser2 waits for all transfers to start
#    And user of browser2 waits for all transfers to finish
#    And user of browser2 sees directory in ended transfers:
#            name: dir1
#            destination: oneprovider-2
#            username: user1
#            total files: 2
#            transferred: 100 MiB
#            type: replication
#            status: completed
#
#    And user of browser1 is idle for 8 seconds
#    And user of browser1 clicks on "Auto cleaning" navigation tab in space "space1"
#    And user of browser1 enables auto-cleaning in "space1" space in Onepanel
#    And user of browser1 enables selective cleaning in auto-cleaning tab in Onepanel
#    And user of browser1 enables Lower size limit in auto-cleaning tab in Onepanel
#    And user of browser1 clicks GiB on dropdown Lower size limit rule in auto-cleaning tab in Onepanel
#    And user of browser1 is idle for 8 seconds
#
#    And user of browser1 clicks change soft quota button in auto-cleaning tab in Onepanel
#    And user of browser1 types "0.05" to soft quota input field in auto-cleaning tab in Onepanel
#    And user of browser1 confirms changing value of soft quota in auto-cleaning tab in Onepanel
#
#    And user of browser1 clicks change hard quota button in auto-cleaning tab in Onepanel
#    And user of browser1 types "0.06" to hard quota input field in auto-cleaning tab in Onepanel
#    And user of browser1 confirms changing value of hard quota in auto-cleaning tab in Onepanel
#
#    And user of browser1 clicks on "Start cleaning now" button in auto-cleaning tab in Onepanel
#    And user of browser1 is idle for 5 seconds
#    Then user of browser1 sees 0 B released size in cleaning report in Onepanel
#
#    And user of browser2 clicks on the "data" tab in main menu sidebar
#    And user of browser2 uses spaces select to change data space to "space1"
#    And user of browser2 sees file browser in data tab in Oneprovider page
#    And user of browser2 double clicks on item named "dir1" in file browser
#    And user of browser2 sees file chunks for file "large_file.txt" as follows:
#            oneprovider-1: entirely filled
#            oneprovider-2: entirely filled
#    And user of browser2 sees file chunks for file "large_file(1).txt" as follows:
#            oneprovider-1: entirely filled
#            oneprovider-2: entirely filled
#
#    # revoke space support
#    And user of browser1 clicks on Spaces item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
#    And user of browser1 expands toolbar for "space1" space record in Spaces page in Onepanel
#    And user of browser1 clicks on Revoke space support option in space's toolbar in Onepanel
#    And user of browser1 clicks on Yes, revoke button in REVOKE SPACE SUPPORT modal in Onepanel
#    And user of browser1 sees an info notify with text matching to: .*[Ss]upport.*revoked.*
#
#
#  Scenario: User uses auto-cleaning with upper size limit which skips too big files
#    Given there are no spaces supported in Onepanel used by user of browser1
#
#    # receive support token
#    When user of browser2 clicks "space1" on the spaces list in the sidebar
#    And user of browser2 clicks Providers of "space1" in the sidebar
#    And user of browser2 clicks Get support button on providers page
#    And user of browser2 clicks Copy button on Get support page
#    And user of browser2 sees an info notify with text matching to: .*copied.*
#    And user of browser2 sends copied token to user of browser1
#
#    # support space
#    And user of browser1 selects "posix" from storage selector in support space form in Onepanel
#    And user of browser1 types received token to Support token field in support space form in Onepanel
#    And user of browser1 types "1" to Size input field in support space form in Onepanel
#    And user of browser1 selects GiB radio button in support space form in Onepanel
#    And user of browser1 clicks on Support space button in support space form in Onepanel
#    And user of browser1 sees an info notify with text matching to: .*[Aa]dded.*support.*space.*
#    And user of browser1 sees that space support record for "space1" has appeared in Spaces page in Onepanel
#
#    # enable files popularity
#    And user of browser1 expands "space1" record on spaces list in Spaces page in Onepanel
#    And user of browser1 clicks on File popularity navigation tab in space "space1"
#    And user of browser1 enables file-popularity in "space1" space in Onepanel
#
#    # confirm support of space and go to provider
#    And user of browser2 clicks "space1" on the spaces list in the sidebar
#    And user of browser2 clicks Providers of "space1" in the sidebar
#    And user of browser2 sees "oneprovider-1" is on the providers list
#    And user of browser2 opens oneprovider-1 Oneprovider view in web GUI
#    And user of browser2 sees that Oneprovider session has started
#    And user of browser2 uses spaces select to change data space to "space1"
#
#    And user of browser2 creates directory "dir1"
#    And user of browser2 double clicks on item named "dir1" in file browser
#    And user of browser2 uses upload button in toolbar to upload file "large_file.txt" to current dir
#    And user of browser2 uses upload button in toolbar to upload file "large_file.txt" to current dir
#    And user of browser2 uses upload button in toolbar to upload file "20B-0.txt" to current dir
#    And user of browser2 is idle for 10 seconds
#    And user of browser2 refreshes site
#    And user of browser2 sees file browser in data tab in Oneprovider page
#    And user of browser2 changes current working directory to space1 using breadcrumbs
#
#    # replicate data
#    And user of browser2 replicates "dir1" to provider "oneprovider-2"
#    And user of browser2 clicks on the "transfers" tab in main menu sidebar
#    And user of browser2 selects "space1" space in transfers tab
#    And user of browser2 waits for all transfers to start
#    And user of browser2 waits for all transfers to finish
#    And user of browser2 sees directory in ended transfers:
#            name: dir1
#            destination: oneprovider-2
#            username: user1
#            total files: 3
#            transferred: 100 MiB
#            type: replication
#            status: completed
#
#    And user of browser1 is idle for 8 seconds
#    And user of browser1 clicks on "Auto cleaning" navigation tab in space "space1"
#    And user of browser1 enables auto-cleaning in "space1" space in Onepanel
#    And user of browser1 enables selective cleaning in auto-cleaning tab in Onepanel
#    And user of browser1 enables Upper size limit in auto-cleaning tab in Onepanel
#    And user of browser1 clicks MiB on dropdown Upper size limit rule in auto-cleaning tab in Onepanel
#    And user of browser1 is idle for 8 seconds
#
#    And user of browser1 clicks change soft quota button in auto-cleaning tab in Onepanel
#    And user of browser1 types "0.05" to soft quota input field in auto-cleaning tab in Onepanel
#    And user of browser1 confirms changing value of soft quota in auto-cleaning tab in Onepanel
#
#    And user of browser1 clicks change hard quota button in auto-cleaning tab in Onepanel
#    And user of browser1 types "0.06" to hard quota input field in auto-cleaning tab in Onepanel
#    And user of browser1 confirms changing value of hard quota in auto-cleaning tab in Onepanel
#
#    And user of browser1 clicks on "Start cleaning now" button in auto-cleaning tab in Onepanel
#    And user of browser1 is idle for 5 seconds
#    Then user of browser1 sees 20 B released size in cleaning report in Onepanel
#
#    And user of browser2 clicks on the "data" tab in main menu sidebar
#    And user of browser2 uses spaces select to change data space to "space1"
#    And user of browser2 sees file browser in data tab in Oneprovider page
#    And user of browser2 double clicks on item named "dir1" in file browser
#    And user of browser2 sees file chunks for file "large_file.txt" as follows:
#            oneprovider-1: entirely filled
#            oneprovider-2: entirely filled
#    And user of browser2 sees file chunks for file "large_file(1).txt" as follows:
#            oneprovider-1: entirely filled
#            oneprovider-2: entirely filled
#    And user of browser2 sees file chunks for file "20B-0.txt" as follows:
#            oneprovider-1: entirely empty
#            oneprovider-2: entirely filled
#
#
#    # revoke space support
#    And user of browser1 clicks on Spaces item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
#    And user of browser1 expands toolbar for "space1" space record in Spaces page in Onepanel
#    And user of browser1 clicks on Revoke space support option in space's toolbar in Onepanel
#    And user of browser1 clicks on Yes, revoke button in REVOKE SPACE SUPPORT modal in Onepanel
#    And user of browser1 sees an info notify with text matching to: .*[Ss]upport.*revoked.*
#
#  Scenario: User fails to enable auto-cleaning if file-popularity is disabled
#    Given there are no spaces supported in Onepanel used by user of browser1
#
#    # receive support token
#    When user of browser2 clicks "space1" on the spaces list in the sidebar
#    And user of browser2 clicks Providers of "space1" in the sidebar
#    And user of browser2 clicks Get support button on providers page
#    And user of browser2 clicks Copy button on Get support page
#    And user of browser2 sees an info notify with text matching to: .*copied.*
#    And user of browser2 sends copied token to user of browser1
#
#    # support space
#    And user of browser1 selects "posix" from storage selector in support space form in Onepanel
#    And user of browser1 types received token to Support token field in support space form in Onepanel
#    And user of browser1 types "1" to Size input field in support space form in Onepanel
#    And user of browser1 selects GiB radio button in support space form in Onepanel
#    And user of browser1 clicks on Support space button in support space form in Onepanel
#    And user of browser1 sees an info notify with text matching to: .*[Aa]dded.*support.*space.*
#    And user of browser1 sees that space support record for "space1" has appeared in Spaces page in Onepanel
#
#    And user of browser1 expands "space1" record on spaces list in Spaces page in Onepanel
#    Then user of browser1 cannot click on "Auto cleaning" navigation tab in space "space1"