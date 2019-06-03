Feature: Storage management using onepanel


  Background:
    Given initial users configuration in "onezone" Onezone service:
            - user1

    And users opened [browser1, browser2] browsers' windows
    And users of [browser1, browser2] opened [Onezone, oneprovider-1 provider panel] page
    And user of [browser1, browser2] logged as [admin, admin] to [Onezone, emergency interface of Onepanel] service
    And directory tree structure on local file system:
          browser1:
              - dir1: 70


  Scenario Outline: User uploads files on freshly supported space on newly created storage
    Given there are no spaces supported in Onepanel used by user of browser1

    # create new_storage POSIX storage
    When user of browser1 clicks on Clusters in the main menu
    And user of browser1 clicks on "oneprovider-1" in clusters menu
    And user of <client> clicks on Storages item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of <client> clicks on Add storage button in storages page in Onepanel
    And user of <client> selects POSIX from storage selector in storages page in Onepanel
    And user of <client> types "<storage_name>" to Storage name field in POSIX form in storages page in Onepanel
    And user of <client> types "/volumes/storage" to Mount point field in POSIX form in storages page in Onepanel
    And user of <client> clicks on Add button in add storage form in storages page in Onepanel
    And user of <client> sees an info notify with text matching to: .*[Ss]torage.*added.*
    And user of <client> expands "<storage_name>" record on storages list in storages page in Onepanel
    And user of <client> sees that "<storage_name>" Storage type is posix in storages page in Onepanel
    And user of <client> sees that "<storage_name>" Mount point is /volumes/storage in storages page in Onepanel

    # create space
    And user of browser1 clicks on Create space button in spaces sidebar
    And user of browser1 writes "hello_world1" into space name text field
    And user of browser1 clicks on Create new space button
    And user of browser1 sees that "hello_world1" has appeared on the spaces list in the sidebar

    # receive support token
    And user of browser1 clicks Providers of "hello_world1" in the sidebar
    And user of browser1 clicks Add support button on providers page
    And user of browser1 clicks Copy button on Add support page
    And user of browser1 sends copied token to user of <client>

    # support space
    And user of browser1 clicks on Clusters in the main menu
    And user of browser1 clicks on "oneprovider-1" in clusters menu
    And user of <client> clicks on Spaces item in submenu of "oneprovider-1" item in CLUSTERS sidebar in Onepanel
    And user of <client> clicks on Support space button in spaces page in Onepanel if there are some spaces already supported
    And user of <client> selects "<storage_name>" from storage selector in support space form in Onepanel
    And user of <client> types received token to Support token field in support space form in Onepanel
    And user of <client> types "1" to Size input field in support space form in Onepanel
    And user of <client> selects GiB radio button in support space form in Onepanel
    And user of <client> clicks on Support space button in support space form in Onepanel
    And user of <client> sees an info notify with text matching to: .*[Aa]dded.*support.*space.*
    And user of <client> sees that space support record for "hello_world1" has appeared in Spaces page in Onepanel

    # go to provider
    And user of browser1 is idle for 2 seconds
    And user of browser1 refreshes site
    And user of browser1 clicks Providers of "hello_world1" in the sidebar
    And user of browser1 opens oneprovider-1 Oneprovider view in web GUI

    # create tmp dir and upload there 70 files
    And user of browser1 uses spaces select to change data space to "hello_world1"
    And user of browser1 sees file browser in data tab in Oneprovider page
    And user of browser1 sees that current working directory displayed in breadcrumbs is hello_world1
    And user of browser1 clicks the button from top menu bar with tooltip "Create directory"
    And user of browser1 sees that "New directory" modal has appeared
    And user of browser1 clicks on input box in active modal
    And user of browser1 types "dir100" on keyboard
    And user of browser1 presses enter on keyboard
    And user of browser1 sees that the modal has disappeared
    And user of browser1 sees that item named "dir100" has appeared in file browser
    And user of browser1 double clicks on item named "dir100" in file browser
    And user of browser1 sees that current working directory displayed in breadcrumbs is hello_world1/dir100
    And user of browser1 uses upload button in toolbar to upload files from local directory "dir1" to remote current dir
    And user of browser1 waits for file upload to finish

    Then user of browser1 sees that there are 70 items in file browser

    And user of browser1 clicks on the "spaces" tab in main menu sidebar
    And user of browser1 clicks "hello_world1" on the spaces list in the sidebar
    And user of browser1 clicks on "Leave space" button in space menu
    And user of browser1 clicks on yes button

    Examples:
    | client   | storage_name |
    | browser1 | new_storage1 |
    | browser2 | new_storage2 |

